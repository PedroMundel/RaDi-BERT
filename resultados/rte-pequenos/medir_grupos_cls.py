"""Stage 2 of section 11.8 (plan docs/2026-11-10-plano-teste-fora-da-distribuicao.md): does a head that predicts,
from the [CLS] vector, which groups of new words the rationale uses help the classifier? Design, cut and criterion
written before this ran (Pedro, 17/11).

Student: BERT small on the 4,000 e-SNLI train pairs; teacher A as in medir_juntar.py. Arms:
  none, answers                 the two reference arms of medir_juntar.py (the baseline Pedro asked for first)
  head_all                      classification + 1.0 x the group loss, target = all 29 groups
  head_cut                      the same, target = the seven groups of the cut (CUT_GROUPS)
  head_all_swapped, head_cut_swapped
                                the control: each pair gets the group row of another pair with the same gold label
  <the four>_answers            the same four with the teacher's answers in the sum
Every student's hits are written pair by pair, on the choice pairs and on the dev: one row per (arm, seed, split)
with a string of 0/1 in the order of the pairs; medir_recorte.py reads it. The head arms also write, before and
after training, the cosine between the encoder gradient of each group's loss and of the classification loss on a
fixed batch of train pairs (descriptive only: it decides nothing).

One student is appended at a time and a rerun skips the students already there.

Usage:  uv run --frozen python resultados/rte-pequenos/medir_grupos_cls.py [--fumaca] [--bracos a,b] [--sementes 1-5]
        uv run --frozen --with umap-learn python resultados/rte-pequenos/medir_grupos_cls.py --alvos
        (--alvos writes the group row of every train pair, once, where the word -> group table is: the notebook)
"""
import argparse
import time
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import torch
import torch.nn.functional as F
from medir_destilacao import trained_teacher
from medir_juntar import ARMS, SEEDS, train_student

from radibert import esnli_dados as esnli
from radibert import rte_dados as dados
from radibert import rte_destilacao as destilacao
from radibert import rte_treino as treino
from radibert.rte_modelo import RationaleBert, classifier_only, cls_loss, logits_of, run_encoder

HERE = Path(__file__).parent
TARGETS = HERE / "grupos-alvos-treino.csv"
CUT_GROUPS = [21, 2, 3, 14, 20, 16, 4]  # Pedro, 17/11: "Seis mais gênero e idade"
SPLITS = ("choice", "dev")
SWAP_SEED, PROBE_PAIRS = 0, 256


@dataclass(frozen=True)
class HeadArm:
    cut: bool  # target = CUT_GROUPS instead of every group
    swapped: bool
    answers: bool


HEAD_ARMS = {f"head_{'cut' if cut else 'all'}{'_swapped' if swapped else ''}{'_answers' if answers else ''}":
             HeadArm(cut, swapped, answers)
             for answers in (False, True) for cut in (False, True) for swapped in (False, True)}
ALL_ARMS = ("none", "answers", *HEAD_ARMS)


def write_targets():
    """The 0/1 group row of every train pair, from the word -> group table of section 11.7."""
    from medir_grupos_dependem_do_par import group_targets  # imports umap down the chain: only here
    pairs = esnli.training_pairs()
    rows = group_targets(pairs)
    rows.insert(0, "idx", pairs["idx"].to_numpy())
    rows.to_csv(TARGETS, index=False)
    print(f"{len(rows)} pares, {rows.shape[1] - 1} grupos -> {TARGETS}")


def group_rows(arm: HeadArm, pairs: pd.DataFrame) -> tuple[list[int], torch.Tensor]:
    """The arm's groups and one 0/1 row over them per train pair, in the order of `pairs` (swapped inside the gold
    label in the control arms)."""
    table = pd.read_csv(TARGETS).set_index("idx")
    groups = CUT_GROUPS if arm.cut else [int(column) for column in table.columns]
    rows = torch.tensor(table.loc[pairs["idx"], [str(group) for group in groups]].to_numpy())
    if arm.swapped:
        rows = destilacao.swapped_within_label(rows, pairs["y"].tolist(), SWAP_SEED)
    return groups, rows


def gradient_cosines(model: RationaleBert, probe: dict) -> list[float]:
    """For each group, the cosine between the gradient of its loss and of the classification loss, both with
    respect to the encoder's weights, on the probe batch. Dropout off, fp32."""
    model.eval()
    params = [p for p in model.bert.parameters() if p.requires_grad]
    out = run_encoder(model.bert, probe)
    logits = logits_of(model.bert, model.head, out.last_hidden_state, probe["attention_mask"])

    def flat_gradient(loss: torch.Tensor) -> torch.Tensor:
        gradients = torch.autograd.grad(loss, params, retain_graph=True, allow_unused=True)
        return torch.cat([(torch.zeros_like(p) if g is None else g).flatten() for g, p in zip(gradients, params)])

    of_classification = flat_gradient(cls_loss(logits, probe["y"]))
    cosines = [F.cosine_similarity(flat_gradient(loss), of_classification, dim=0).item()
               for loss in model.distill.group_losses(model, out, probe)]
    model.train()
    return cosines


def train_head_student(name: str, seed: int, student_name: str, teacher, pairs: pd.DataFrame, train: list[dict],
                       plan, device: torch.device) -> tuple[RationaleBert, list[dict]]:
    """Trains one student of a head arm; returns it with the gradient cosines measured before and after."""
    arm = HEAD_ARMS[name]
    groups, rows = group_rows(arm, pairs)
    torch.manual_seed(seed)
    model = RationaleBert.with_mark_attention(student_name, n_labels=len(esnli.LABELS))
    model.with_group_head(destilacao.label_rate_logits(rows, pairs["y"].tolist(), len(esnli.LABELS)))
    with_answers = destilacao.Distillation(teacher, answers=True) if arm.answers else None
    model.distill = destilacao.GroupTargets(dict(zip(pairs["idx"].tolist(), rows)), with_answers)
    treino.place(model, device)
    probe = treino.to_device(dados.collate(train[:PROBE_PAIRS]), device)
    cosines = []
    for moment in ("start", "end"):
        if moment == "end":
            treino.train(model, plan, train, seed, device)
        cosines += [{"arm": name, "seed": seed, "moment": moment, "group": group, "cosine": round(cosine, 4)}
                    for group, cosine in zip(groups, gradient_cosines(model, probe))]
    return model, cosines


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fumaca", action="store_true",
                        help="CPU, 48 pairs per set, 1 seed, tiny student and small teacher")
    parser.add_argument("--alvos", action="store_true", help="only write the group row of every train pair")
    parser.add_argument("--bracos", default=",".join(ALL_ARMS), help="arms to run, comma separated (default: all)")
    parser.add_argument("--sementes", default=f"1-{SEEDS}", help="first-last seed")
    args = parser.parse_args()
    if args.alvos:
        return write_targets()
    arms = args.bracos.split(",")
    unknown = sorted(set(arms) - set(ALL_ARMS))
    if unknown:
        raise SystemExit(f"bracos desconhecidos: {unknown}; os que existem: {list(ALL_ARMS)}")
    first_seed, last_seed = (int(part) for part in args.sementes.split("-"))
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
    plans = {"last": treino.make_plan(len(train), "prop")}
    tag = "fumaca" if args.fumaca else str(len(train))
    out = HERE / f"grupos-cls-acertos-esnli-{tag}.csv"
    cosines_out = HERE / f"grupos-cls-cossenos-esnli-{tag}.csv"
    # the same teacher file medir_juntar.py loads: the teacher of sections 11.3 to 11.5
    teachers = {"trained": trained_teacher(teacher_name, plans["last"], items["teacher_a"],
                                           HERE / f"destilacao-professor-fora-{tag}.pt", device)}

    done = set()
    if out.exists():
        seen = pd.read_csv(out, dtype={"hits": str})
        done = set(zip(seen["arm"], seen["seed"]))
    for name in arms:
        for seed in seeds:
            if (name, seed) in done:
                continue
            start = time.perf_counter()
            if name in HEAD_ARMS:
                model, cosines = train_head_student(name, seed, student_name, teachers["trained"], sets["train"],
                                                    train, plans["last"], device)
            else:
                model, _ = train_student(ARMS[name], seed, student_name, teachers, train, plans, device)
                cosines = []
            classifier = classifier_only(model)
            rows = []
            for split in SPLITS:
                right = treino.predict(classifier, items[split], device).argmax(1) == sets[split]["y"].to_numpy()
                rows.append({"arm": name, "seed": seed, "split": split, "accuracy": round(float(right.mean()), 4),
                             "hits": "".join("1" if hit else "0" for hit in right)})
            treino.append_csv(cosines_out, cosines)
            treino.append_csv(out, rows)
            print(f"{name} seed {seed}: " + " ".join(f"{row['split']} {row['accuracy']:.3f}" for row in rows)
                  + f" ({round(time.perf_counter() - start)} s)", flush=True)
    print(f"completo {out}", flush=True)


if __name__ == "__main__":
    main()
