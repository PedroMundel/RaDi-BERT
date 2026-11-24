"""Can the gain of distilling the teacher's answers go higher, and where does it come from? (plan
docs/2026-11-10-plano-teste-fora-da-distribuicao.md, section 11.4, written before this ran; Pedro, 16/11.)

Student: BERT small on the 4,000 e-SNLI train pairs, 1,000 steps, 5 seeds, loss = classification + 1.0 x target loss.
Teacher A: BERT base trained on 4,000 other pairs (the teacher of section 11.3, reloaded from its file when there).
Teacher B: BERT base trained on 8,000 pairs, teacher A's plus 4,000 more, none of them the student's.
  none        no target loss
  out_t1      teacher A's label probabilities (what passed in 11.3)
  out_t2/t4   the same with temperature 2 and 4
  big_t1/t2   teacher B's probabilities, temperature 1 and 2
  smooth      no teacher: 0.9 on the right label, 0.05 on each other
  swapped     teacher A's probabilities at temperature 1, but each pair gets those of another pair of its label
Graded on the choice pairs (4,000 pairs no student and no teacher trained on: they pick the variation) and on the
e-SNLI dev (read to confirm the pick, not to pick).

One row is appended per trained student and a rerun skips the rows already there.

Usage:  uv run --frozen python resultados/rte-pequenos/medir_respostas.py [--fumaca]
"""
import argparse
import time
from pathlib import Path

import pandas as pd
import torch
from medir_destilacao import grade, on_student_pairs, trained_teacher

from radibert import esnli_dados as esnli
from radibert import rte_dados as dados
from radibert import rte_destilacao as destilacao
from radibert import rte_treino as treino
from radibert.rte_modelo import RationaleBert, classifier_only

HERE = Path(__file__).parent
SEEDS, SMOOTHING, SWAP_SEED = 5, 0.1, 0
ARMS = {"none": None, "out_t1": ("a", 1.0), "out_t2": ("a", 2.0), "out_t4": ("a", 4.0), "big_t1": ("b", 1.0),
        "big_t2": ("b", 2.0), "smooth": "smooth", "swapped": "swapped"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fumaca", action="store_true",
                        help="CPU, 48 pairs per set, 1 seed, tiny student and small teachers")
    args = parser.parse_args()
    student_name, teacher_name = (dados.TINY, dados.SMALL) if args.fumaca else (dados.SMALL, dados.BERT)
    seeds = 1 if args.fumaca else SEEDS
    device = torch.device("cuda" if torch.cuda.is_available() and not args.fumaca else "cpu")
    tok = dados.load_tokenizers(dados.BERT)
    choice_pairs, extra_pairs = esnli.choice_split()
    sets = {"train": esnli.training_pairs(), "teacher_a": esnli.other_pairs(), "choice": choice_pairs,
            "dev": esnli.dev_pairs()}
    sets["teacher_b"] = pd.concat([sets["teacher_a"], extra_pairs]).sort_values("idx").reset_index(drop=True)
    if args.fumaca:
        sets = {name: pairs.iloc[:96 if name == "teacher_b" else 48] for name, pairs in sets.items()}
    items = {name: dados.encode(pairs, tok) for name, pairs in sets.items()}
    train, labels = items["train"], [item["y"] for item in items["train"]]
    n_labels = len(esnli.LABELS)
    plan = treino.make_plan(len(train), "prop")
    tag = "fumaca" if args.fumaca else str(len(train))
    out = HERE / f"respostas-esnli-{tag}.csv"

    # teacher A's file is the one medir_destilacao.py --professor-fora wrote: the same teacher as in section 11.3
    teachers = {"a": trained_teacher(teacher_name, plan, items["teacher_a"],
                                     HERE / f"destilacao-professor-fora-{tag}.pt", device),
                "b": trained_teacher(teacher_name, treino.make_plan(len(items["teacher_b"]), "prop"),
                                     items["teacher_b"], HERE / f"respostas-professor-b-{tag}.pt", device)}
    teacher_rows = {}
    for key, teacher in teachers.items():
        scores = {f"teacher_{split}_accuracy": grade(teacher, items[split], sets[split]["y"].to_numpy(),
                                                     device)["accuracy"] for split in ("choice", "dev")}
        teacher_rows[key] = scores | on_student_pairs(teacher, train, device)
        print(f"professor {key}: " + " ".join(f"{k} {v:.3f}" for k, v in teacher_rows[key].items()), flush=True)
    no_teacher = {k: float("nan") for k in teacher_rows["a"]}
    teacher_a_probs = torch.tensor(treino.predict(teachers["a"], train, device))
    tables = {"smooth": destilacao.smoothed_targets(labels, n_labels, SMOOTHING),
              "swapped": destilacao.swapped_within_label(teacher_a_probs, labels, SWAP_SEED)}

    done = set()
    if out.exists():
        seen = pd.read_csv(out)
        done = set(zip(seen["arm"], seen["seed"]))
    for arm, spec in ARMS.items():
        for seed in range(1, seeds + 1):
            if (arm, seed) in done:
                continue
            start = time.perf_counter()
            torch.manual_seed(seed)
            model = RationaleBert.with_mark_attention(student_name, n_labels=n_labels)
            if isinstance(spec, tuple):
                model.distill = destilacao.Distillation(teachers[spec[0]], answers=True, temperature=spec[1])
            elif spec is not None:
                model.distill = destilacao.TargetTable(dict(zip((item["idx"] for item in train), tables[spec])))
            treino.train(model, plan, train, seed, device)
            classifier = classifier_only(model)
            row = {"arm": arm, "seed": seed}
            for split in ("choice", "dev"):
                scores = grade(classifier, items[split], sets[split]["y"].to_numpy(), device)
                row |= {f"{split}_{k}": v for k, v in scores.items()}
            row |= teacher_rows[spec[0]] if isinstance(spec, tuple) else no_teacher
            row["seconds"] = round(time.perf_counter() - start)
            treino.append_csv(out, [row])
            print(f"{arm} seed {seed}: choice_accuracy {row['choice_accuracy']:.3f} "
                  f"dev_accuracy {row['dev_accuracy']:.3f} ({row['seconds']} s)", flush=True)
    print(f"completo {out}", flush=True)


if __name__ == "__main__":
    main()
