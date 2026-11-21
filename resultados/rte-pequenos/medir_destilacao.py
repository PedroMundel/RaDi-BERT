"""Attention distillation from BERT base into BERT small on e-SNLI (plan
docs/2026-11-10-plano-teste-fora-da-distribuicao.md, section 11, written before this ran; Pedro's idea, 16/11).

Teacher: BERT base trained once (seed 1) on the 4,000 e-SNLI train pairs, then frozen; its weights are saved next to
this script (teacher file, not in git) so a resumed run distils from the same teacher. Students: BERT small, the
training of medir_camadas.py, 5 seeds per arm:
  none        no distillation
  att_last    attention of the teacher's last layer -> the student's last layer (MiniLM)
  att_all     teacher layers 3, 6, 9, 12 -> student layers 1, 2, 3, 4, summed (TinyBERT's even mapping)
  pre_last    as att_last, but the teacher is BERT base with no training on the task (control 2)
  pre_all     as att_all, same untrained-on-the-task teacher
  outputs     the trained teacher's label probabilities instead of its attention (reference)
Loss of every distilled arm: classification + 1.0 x distillation, from step 1. Graded on the e-SNLI dev.

`--professor-fora` (plan, section 11.3): the trained teacher learns from 4,000 OTHER pairs of the same batch, none of
them among the student's, so the student's pairs are new to it; the students and everything else stay the same. Only
the arms with the trained teacher run. Both modes print how the trained teacher does on the student's own train
pairs (accuracy and mean probability of the label it picks): close to 100% means it memorized them.

One row is appended per trained student and a rerun skips the rows already there.

Usage:  uv run --frozen python resultados/rte-pequenos/medir_destilacao.py [--fumaca] [--professor-fora]
"""
import argparse
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch

from radibert import esnli_dados as esnli
from radibert import rte_dados as dados
from radibert import rte_destilacao as destilacao
from radibert import rte_treino as treino
from radibert.rte_modelo import Classifier, RationaleBert, classifier_only

HERE = Path(__file__).parent
SEEDS, TEACHER_SEED = 5, 1
ARMS = ("none", "att_last", "att_all", "pre_last", "pre_all", "outputs")
MEASURES = ("accuracy", "roc_auc")


def grade(classifier: Classifier, items: list[dict], y, device) -> dict:
    scores = treino.metrics(y, treino.predict(classifier, items, device), esnli.LABELS)
    return {measure: scores[measure] for measure in MEASURES}


def on_student_pairs(teacher: Classifier, train: list[dict], device) -> dict:
    """The premise of section 11.3: how well, and how sure, the teacher is on the pairs the student trains on."""
    probs = treino.predict(teacher, train, device)
    y = np.array([item["y"] for item in train])
    return {"teacher_train_accuracy": float((probs.argmax(1) == y).mean()),
            "teacher_train_confidence": float(probs.max(1).mean())}


def trained_teacher(name: str, plan, train: list[dict], path: Path, device) -> Classifier:
    """The teacher trained on the task: loaded from `path` when it is there, trained and saved otherwise."""
    model = RationaleBert.with_mark_attention(name, n_labels=len(esnli.LABELS))
    if path.exists():
        teacher = classifier_only(model)
        teacher.load_state_dict(torch.load(path, map_location="cpu"))
        print(f"professor carregado de {path.name}", flush=True)
    else:
        torch.manual_seed(TEACHER_SEED)
        model = RationaleBert.with_mark_attention(name, n_labels=len(esnli.LABELS))
        treino.train(model, plan, train, TEACHER_SEED, device)
        teacher = classifier_only(model)
        torch.save(teacher.state_dict(), path)
    return teacher.to(device).eval().requires_grad_(False)


def untrained_teacher(name: str, device) -> Classifier:
    """BERT base as pre-trained, never trained on the task (its head is random and never read: attention only)."""
    torch.manual_seed(TEACHER_SEED)
    model = RationaleBert.with_mark_attention(name, n_labels=len(esnli.LABELS))
    return classifier_only(model).to(device).eval().requires_grad_(False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fumaca", action="store_true",
                        help="CPU, 48 train pairs, 64 dev pairs, 1 seed, tiny student and small teacher")
    parser.add_argument("--professor-fora", action="store_true",
                        help="the trained teacher learns from 4,000 other pairs, none of them the student's")
    args = parser.parse_args()
    student_name, teacher_name = (dados.TINY, dados.SMALL) if args.fumaca else (dados.SMALL, dados.BERT)
    seeds = 1 if args.fumaca else SEEDS
    device = torch.device("cuda" if torch.cuda.is_available() and not args.fumaca else "cpu")
    tok = dados.load_tokenizers(dados.BERT)
    pairs, dev_pairs = esnli.training_pairs(), esnli.dev_pairs()
    teacher_pairs = esnli.other_pairs() if args.professor_fora else pairs
    if args.fumaca:
        pairs, teacher_pairs, dev_pairs = pairs.iloc[:48], teacher_pairs.iloc[:48], dev_pairs.iloc[:64]
    train, dev, dev_y = dados.encode(pairs, tok), dados.encode(dev_pairs, tok), dev_pairs["y"].to_numpy()
    plan = treino.make_plan(len(train), "prop")
    tag = ("fora-" if args.professor_fora else "") + ("fumaca" if args.fumaca else str(len(train)))
    out = HERE / f"destilacao-esnli-{tag}.csv"
    arms = tuple(arm for arm in ARMS if not (args.professor_fora and arm.startswith("pre_")))

    teachers = {"trained": trained_teacher(teacher_name, plan, dados.encode(teacher_pairs, tok),
                                           HERE / f"destilacao-professor-{tag}.pt", device),
                "untrained": untrained_teacher(teacher_name, device)}
    teacher_scores = {f"teacher_{k}": v for k, v in grade(teachers["trained"], dev, dev_y, device).items()}
    teacher_scores |= on_student_pairs(teachers["trained"], train, device)
    print("professor treinado: " + " ".join(f"{k} {v:.3f}" for k, v in teacher_scores.items()), flush=True)
    n_teacher = len(teachers["trained"].bert.encoder.layer)

    done = set()
    if out.exists():
        seen = pd.read_csv(out)
        done = set(zip(seen["arm"], seen["seed"]))
    for arm in arms:
        for seed in range(1, seeds + 1):
            if (arm, seed) in done:
                continue
            start = time.perf_counter()
            torch.manual_seed(seed)
            model = RationaleBert.with_mark_attention(student_name, n_labels=len(esnli.LABELS))
            n_student = len(model.bert.encoder.layer)
            if arm != "none":
                layer_map = None if arm == "outputs" else (
                    destilacao.last_map if arm.endswith("_last") else destilacao.uniform_map)(n_student, n_teacher)
                teacher = teachers["untrained" if arm.startswith("pre_") else "trained"]
                model.distill = destilacao.Distillation(teacher, layer_map, answers=arm == "outputs")
            log = treino.train(model, plan, train, seed, device)
            last_aux = sum(log.last_epoch_aux) / len(log.last_epoch_aux) if log.last_epoch_aux else float("nan")
            row = {"arm": arm, "seed": seed} | {f"dev_{k}": v for k, v in
                                                grade(classifier_only(model), dev, dev_y, device).items()}
            row |= {"last_epoch_distillation_loss": last_aux} | teacher_scores
            row["seconds"] = round(time.perf_counter() - start)
            treino.append_csv(out, [row])
            print(f"{arm} seed {seed}: dev_accuracy {row['dev_accuracy']:.3f} dev_roc_auc {row['dev_roc_auc']:.3f} "
                  f"perda de destilacao {last_aux:.3f} ({row['seconds']} s)", flush=True)
    print(f"completo {out}", flush=True)


if __name__ == "__main__":
    main()
