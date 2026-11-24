"""Cheap ways of "fine-tuning the MS-MARCO BERT on RTE": does any give Agrawal's 0.4754 baseline (Table 2)?
Criterion written before running: docs/2026-11-18-gaps-da-argumentacao.md, "Gap 2b".

Same checkpoint, data and recipe as the 10/11 baseline (0.767), no decoder; one thing changes per condition:
  frozen          the encoder does not train, only the new classification head (8 epochs, warmup 500)
  one_epoch_500   1 epoch (78 steps) under the 500-step warmup: the rate never passes 16% of 5e-5
  one_epoch_prop  1 epoch, proportional warmup

    uv run --frozen python resultados/rte-msmarco/condicoes_baseline.py [--micro 8] [--fumaca]
A rerun skips the (condition, seed) rows already in condicoes-baseline.csv.
"""
import argparse
import time
from pathlib import Path

import pandas as pd
import torch

from radibert import rte_dados as dados
from radibert import rte_treino as treino

HERE = Path(__file__).parent
OUT = HERE / "condicoes-baseline.csv"
CONDITIONS = {"frozen": (treino.EPOCHS, "500", True), "one_epoch_500": (1, "500", False),
              "one_epoch_prop": (1, "prop", False)}  # epochs, warmup, encoder frozen
SEEDS = range(1, 6)


def run(condition: str, seed: int, data: treino.Data, device: torch.device, micro: int) -> dict:
    epochs, warmup, frozen = CONDITIONS[condition]
    torch.manual_seed(seed)
    model, _ = treino.build_model("bert", dados.MSMARCO)
    model.bert.requires_grad_(not frozen)
    plan = treino.make_plan(len(data.train), warmup, epochs=epochs)
    start = time.perf_counter()
    treino.train(model, plan, data.train, seed, device, micro=micro)
    scores = treino.metrics(data.dev_y, treino.predict(treino.classifier_only(model), data.dev, device))
    return {"condition": condition, "seed": seed, "roc_auc": scores["roc_auc"], "accuracy": scores["accuracy"],
            "steps": plan.total, "warmup_steps": plan.warmup_steps, "seconds": round(time.perf_counter() - start, 1),
            "device": str(device), "bert": dados.MSMARCO, "code": treino.code_version()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--micro", type=int, default=8)
    parser.add_argument("--fumaca", action="store_true", help="one seed of one_epoch_prop, written to a separate file")
    args = parser.parse_args()
    out = OUT.with_name("condicoes-baseline-fumaca.csv") if args.fumaca else OUT
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    data = treino.load_data(dados.load_tokenizers(dados.BERT), HERE / "condicoes")
    done = set(zip(*(pd.read_csv(out)[c] for c in ("condition", "seed")))) if out.exists() else set()
    todo = [("one_epoch_prop", 1)] if args.fumaca else [(c, s) for c in CONDITIONS for s in SEEDS]
    for condition, seed in todo:
        if (condition, seed) in done:
            continue
        row = run(condition, seed, data, device, args.micro)
        treino.append_csv(out, [row])
        print(f"{condition} seed {seed}: roc_auc {row['roc_auc']:.4f} acc {row['accuracy']:.4f} "
              f"({row['seconds']:.0f} s)", flush=True)


if __name__ == "__main__":
    main()
