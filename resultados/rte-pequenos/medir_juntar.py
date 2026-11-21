"""Does joining the teacher's internals with its answers beat the answers alone? (plan
docs/2026-11-10-plano-teste-fora-da-distribuicao.md, section 11.5, written before this ran; Pedro, 16 and 17/11.)

Student: BERT small on the 4,000 e-SNLI train pairs, 5 seeds. Teacher A: BERT base trained on 4,000 other pairs (the
teacher of sections 11.3 and 11.4, reloaded from its file). Every arm ends with 1,000 steps of classification +
1.0 x the sum of its losses:
  none                 no distillation
  answers              the teacher's answers: the arm to beat
  sum                  answers + attention of the 4 layers
  tiny_joint           answers + embeddings + attention and hidden states of the 4 layers (TinyBERT's losses)
  tiny_content         the same without the attention
  mini_joint           answers + attention and value relation of the last layer (MiniLM's losses)
  mini_content         the same without the attention
  sequence             first 2,500 steps (20 epochs) of the internals alone (embeddings + attention and hidden
                       states of the 4 layers, no classification, no answers), then the `answers` training
  sequence_untrained   the same, the first phase imitating a BERT base never trained on the task
  <arm>_clean          the five arms with an attention loss (sum, tiny_joint, mini_joint, sequence,
                       sequence_untrained), with the student's attention read before its dropout instead of after
  sequence_rationale   (18/11) as `sequence`, but the first phase imitates, on the pair's positions only, a teacher
                       that reads the pair AND its rationale (the file medir_professor_justificativa.py saved)
  sequence_rationale_shuffled   its control: that teacher reads the rationale of another pair of the same label
Graded on the choice pairs (4,000 pairs no student and no teacher trained on: they decide) and on the e-SNLI dev
(confirms). Each row also carries the value of every loss on one fixed batch before and after each phase.

One row is appended per trained student and a rerun skips the rows already there.

Usage:  uv run --frozen python resultados/rte-pequenos/medir_juntar.py [--fumaca] [--bracos a,b,...] [--sementes 6-15]
"""
import argparse
import json
import time
from collections.abc import Callable
from dataclasses import dataclass, replace
from pathlib import Path

import pandas as pd
import torch
from medir_destilacao import grade, trained_teacher, untrained_teacher

from radibert import esnli_dados as esnli
from radibert import rte_dados as dados
from radibert import rte_destilacao as destilacao
from radibert import rte_treino as treino
from radibert.rte_modelo import Classifier, RationaleBert, classifier_only

HERE = Path(__file__).parent
SEEDS, FIRST_PHASE_EPOCHS, PROBE_PAIRS = 5, 20, 32
ALL, LAST = destilacao.uniform_map, destilacao.last_map


@dataclass(frozen=True)
class Arm:
    """What the 1,000-step training adds to the classification (each name -> which layers), and the teacher the
    first phase imitates, when there is one ("trained" or "untrained")."""
    answers: bool = True
    attention: Callable | None = None  # last_map or uniform_map
    hidden: Callable | None = None
    values: Callable | None = None
    first_phase: str | None = None
    before_dropout: bool = False  # the attention loss, in both phases, reads the student's attention before dropout
    first_reads: str | None = None  # what the first-phase teacher reads besides the pair: a key of teacher_inputs


ARMS = {"none": Arm(answers=False), "answers": Arm(), "sum": Arm(attention=ALL),
        "tiny_joint": Arm(attention=ALL, hidden=ALL), "tiny_content": Arm(hidden=ALL),
        "mini_joint": Arm(attention=LAST, values=LAST), "mini_content": Arm(values=LAST),
        "sequence": Arm(first_phase="trained"), "sequence_untrained": Arm(first_phase="untrained")}
# Pedro, 17/11 ("Rodar dos dois jeitos"): every arm with an attention loss also runs with it read before dropout
WITH_ATTENTION = ("sum", "tiny_joint", "mini_joint", "sequence", "sequence_untrained")
ARMS |= {f"{name}_clean": replace(ARMS[name], before_dropout=True) for name in WITH_ATTENTION}
# 18/11 (docs/2026-11-18-professor-que-le-a-justificativa.md): the first phase imitates, on the pair's positions,
# a teacher that reads the pair and its rationale; the control gives it another pair's rationale of the same label
ARMS |= {"sequence_rationale": Arm(first_phase="rationale", first_reads="real"),
         "sequence_rationale_shuffled": Arm(first_phase="rationale", first_reads="shuffled")}
SWAP_SEED = 0
FIRST_PHASE = Arm(answers=False, attention=ALL, hidden=ALL)


def distillation(arm: Arm, teacher: Classifier, n_student: int) -> destilacao.Distillation:
    n_teacher = len(teacher.bert.encoder.layer)
    layers = {name: map_of(n_student, n_teacher) if map_of else None
              for name, map_of in (("layer_map", arm.attention), ("hidden_map", arm.hidden),
                                   ("value_map", arm.values))}
    return destilacao.Distillation(teacher, answers=arm.answers, before_dropout=arm.before_dropout, **layers)


@torch.no_grad()
def loss_values(model: RationaleBert, probe: dict, device: torch.device) -> str:
    """Each loss of the model's current distillation on the probe batch, as JSON; dropout off."""
    model.eval()
    with treino.autocast(device):
        _, terms = model.distill_terms(probe)
    model.train()
    return json.dumps({name: round(float(value), 4) for name, value in terms.items()})


def loaded_teacher(name: str, path: Path, device) -> Classifier:
    """The teacher that reads the rationale, from the file medir_professor_justificativa.py saved. Never trained
    here: the one distilled is the one that script measured."""
    if not path.exists():
        raise SystemExit(f"falta {path}: o professor que le a justificativa vem de medir_professor_justificativa.py")
    teacher = classifier_only(RationaleBert.with_mark_attention(name, n_labels=len(esnli.LABELS)))
    teacher.load_state_dict(torch.load(path, map_location="cpu"))
    print(f"professor carregado de {path.name}", flush=True)
    return teacher.to(device).eval().requires_grad_(False)


def train_student(arm: Arm, seed: int, student_name: str, teachers: dict, train: list[dict], plans: dict,
                  device: torch.device, teacher_inputs: dict) -> tuple[RationaleBert, dict]:
    """Trains one student of `arm` and returns it with the loss values measured around each phase."""
    torch.manual_seed(seed)
    model = RationaleBert.with_mark_attention(student_name, n_labels=len(esnli.LABELS))
    if arm.hidden is not None or arm.first_phase is not None:
        # only where they are used: `none` and `answers` then draw the same random numbers as in medir_respostas.py
        model.with_projections(teachers["trained"].bert.config.hidden_size)
    n_student = len(model.bert.encoder.layer)
    probe = treino.to_device(dados.collate(train[:PROBE_PAIRS]), device)
    values = {"first_losses_start": "", "first_losses_end": "", "losses_start": "", "losses_end": ""}
    if arm.first_phase is not None:
        first = replace(FIRST_PHASE, before_dropout=arm.before_dropout)
        model.distill = distillation(first, teachers[arm.first_phase], n_student)
        if arm.first_reads is not None:
            model.distill.teacher_inputs = teacher_inputs[arm.first_reads]
        treino.place(model, device)
        values["first_losses_start"] = loss_values(model, probe, device)
        treino.train(model, plans["first"], train, seed, device, loss_of=treino.internal_only)
        values["first_losses_end"] = loss_values(model, probe, device)
    if arm.answers:
        model.distill = distillation(arm, teachers["trained"], n_student)
        treino.place(model, device)
        values["losses_start"] = loss_values(model, probe, device)
    treino.train(model, plans["last"], train, seed, device)
    if arm.answers:
        values["losses_end"] = loss_values(model, probe, device)
    return model, values


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fumaca", action="store_true",
                        help="CPU, 48 pairs per set, 1 seed, tiny student and small teachers, 2 first-phase epochs")
    parser.add_argument("--bracos", default=",".join(ARMS), help="arms to run, comma separated (default: all)")
    parser.add_argument("--sementes", default=f"1-{SEEDS}",
                        help="first-last seed, e.g. 6-15 for the 10 new seeds of a candidate (plan, section 11.5)")
    args = parser.parse_args()
    first_seed, last_seed = (int(part) for part in args.sementes.split("-"))
    arms = args.bracos.split(",")
    unknown = sorted(set(arms) - set(ARMS))
    if unknown:
        raise SystemExit(f"bracos desconhecidos: {unknown}; os que existem: {sorted(ARMS)}")
    student_name, teacher_name = (dados.TINY, dados.SMALL) if args.fumaca else (dados.SMALL, dados.BERT)
    seeds = range(1, 2) if args.fumaca else range(first_seed, last_seed + 1)
    device = torch.device("cuda" if torch.cuda.is_available() and not args.fumaca else "cpu")
    tok = dados.load_tokenizers(dados.BERT)
    sets = {"train": esnli.training_pairs(), "teacher_a": esnli.other_pairs(), "choice": esnli.choice_split()[0],
            "dev": esnli.dev_pairs()}
    if args.fumaca:
        sets = {name: pairs.iloc[:48] for name, pairs in sets.items()}
    items = {name: dados.encode(pairs, tok) for name, pairs in sets.items()}
    train = items["train"]
    plans = {"last": treino.make_plan(len(train), "prop"),
             "first": treino.make_plan(len(train), "prop", epochs=2 if args.fumaca else FIRST_PHASE_EPOCHS)}
    tag = "fumaca" if args.fumaca else str(len(train))
    out = HERE / f"juntar-esnli-{tag}.csv"

    # teacher A's file is the one medir_destilacao.py --professor-fora wrote: the teacher of sections 11.3 and 11.4
    teachers = {"trained": trained_teacher(teacher_name, plans["last"], items["teacher_a"],
                                           HERE / f"destilacao-professor-fora-{tag}.pt", device),
                "untrained": untrained_teacher(teacher_name, device)}
    for split in ("choice", "dev"):
        score = grade(teachers["trained"], items[split], sets[split]["y"].to_numpy(), device)["accuracy"]
        print(f"professor A, {split}: accuracy {score:.3f}", flush=True)
    teacher_inputs = {}
    if any(ARMS[name].first_reads for name in arms):
        teachers["rationale"] = loaded_teacher(teacher_name, HERE / f"professor-justificativa-{tag}.pt", device)
        reads = {"real": sets["train"], "shuffled": dados.shuffle_within_label(sets["train"], SWAP_SEED)}
        teacher_inputs = {kind: {item["idx"]: item for item in dados.encode(esnli.rationale_in_input(pairs), tok)}
                          for kind, pairs in reads.items()}

    done = set()
    if out.exists():
        try:
            seen = pd.read_csv(out)
        except pd.errors.ParserError as error:
            raise SystemExit(f"{out} tem uma linha cortada (rodada morta no meio da escrita?): {error}. "
                             "Tire a ultima linha do arquivo e rode de novo; os alunos ja gravados sao pulados.") from error
        done = set(zip(seen["arm"], seen["seed"]))
    for name in arms:
        for seed in seeds:
            if (name, seed) in done:
                continue
            start = time.perf_counter()
            model, values = train_student(ARMS[name], seed, student_name, teachers, train, plans, device,
                                                 teacher_inputs)
            classifier = classifier_only(model)
            row = {"arm": name, "seed": seed}
            for split in ("choice", "dev"):
                scores = grade(classifier, items[split], sets[split]["y"].to_numpy(), device)
                row |= {f"{split}_{k}": v for k, v in scores.items()}
            row |= values | {"seconds": round(time.perf_counter() - start)}
            treino.append_csv(out, [row])
            print(f"{name} seed {seed}: choice_accuracy {row['choice_accuracy']:.3f} "
                  f"dev_accuracy {row['dev_accuracy']:.3f} ({row['seconds']} s) "
                  f"{values['first_losses_start']} -> {values['first_losses_end']} | "
                  f"{values['losses_start']} -> {values['losses_end']}", flush=True)
    print(f"completo {out}", flush=True)


if __name__ == "__main__":
    main()
