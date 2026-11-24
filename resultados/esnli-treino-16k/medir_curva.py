"""Does the decoder make classification start faster? The calendar arm and the decoder arm again on the 16,000
e-SNLI pairs, with the dev scores and the probe's classification loss written at fixed steps after classification
starts. Criterion written before: docs/2026-11-18-gaps-da-argumentacao.md, "Gap 6".

    uv run --frozen python resultados/esnli-treino-16k/medir_curva.py [--bracos bert_calendar bert_decoder]
        [--sementes 1-5] [--fumaca]
A rerun skips the (arm, seed) curves already in ../esnli-treino-16k-curva/curva.csv. Trains nothing else: the
scores of today's grids are not touched.
"""
import argparse
import time
from pathlib import Path

import pandas as pd
import torch

from radibert import rte_dados as dados
from radibert import rte_treino as treino
from radibert.rte_modelo import classifier_only, cls_loss

OUT_DIR = Path(__file__).parent.with_name("esnli-treino-16k-curva")
DEFAULT_ARMS = (treino.CALENDAR_ARM, "bert_decoder")
ARMS = (*DEFAULT_ARMS, treino.SHUFFLED_ARM)  # the shuffled arm's curve: "Gap 6b", asked on 18/11
STEPS = (1225, 1250, 1300, 1400, 1500, 1750, 2000, 2500, 3000, 3500, 4000)
WARMUP = "500"


@torch.no_grad()
def probe_loss(classifier, probe_batch: dict, device: torch.device) -> float:
    """Mean classification loss on the probe's train pairs, in evaluation mode (as rte_gradientes measures l_cls)."""
    classifier.to(device).eval()
    with treino.autocast(device):
        logits = classifier(probe_batch).float()
    return float(cls_loss(logits, probe_batch["y"]))


def curve(arm: str, seed: int, data: treino.Data, device: torch.device, steps: tuple[int, ...],
          encoder: str, batch_size: int, epochs: int) -> list[dict]:
    torch.manual_seed(seed)  # as run_one: head initialization
    model, _ = treino.build_model(arm, encoder, len(data.labels))
    plan = treino.make_plan(len(data.train), WARMUP, batch_size, epochs)
    items, arm_probes = treino.arm_inputs(data, arm)
    probe = arm_probes.groups.to(device)
    rows, start = [], time.perf_counter()

    def after_step(step: int):
        if step not in steps:
            return
        classifier = classifier_only(model)  # a copy: the model in training keeps its mode and its weights
        scores = treino.metrics(data.dev_y, treino.predict(classifier, data.dev, device), data.labels)
        rows.append({"arm": arm, "seed": seed, "step": step, "dev_accuracy": scores["accuracy"],
                     "dev_roc_auc": scores["roc_auc"], "probe_l_cls": probe_loss(classifier, probe.batch, device),
                     "seconds": round(time.perf_counter() - start, 1), "code": treino.code_version()})

    log = treino.train(model, plan, items, seed, device, batch_size, treino.Probes(probe), after_step=after_step)
    if [row["step"] for row in rows] != list(steps):
        raise RuntimeError(f"{arm} seed {seed}: measured {[row['step'] for row in rows]}, expected {list(steps)}")
    # the instrument check: the decoder arm's own gradient measure of L_cls on the same probe, where it has one
    measured = {row["step"]: row["l_cls"] for row in log.group_rows}
    return [row | {"gradient_measure_l_cls": measured.get(row["step"])} for row in rows]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bracos", nargs="+", choices=ARMS, default=list(DEFAULT_ARMS))
    parser.add_argument("--sementes", default="1-5", help="first-last")
    parser.add_argument("--fumaca", action="store_true", help="CPU, tiny BERT, 48 pairs, its own file")
    args = parser.parse_args()
    first, last = (int(part) for part in args.sementes.split("-"))
    treino.code_version()
    tok = dados.load_tokenizers(dados.TINY if args.fumaca else dados.BERT)
    swap = treino.SHUFFLED_ARM in args.bracos
    if args.fumaca:
        out_dir = OUT_DIR / "fumaca" / time.strftime("%Y-%m-%d-%H%M%S")  # each smoke run in its own folder
        device, encoder, batch_size, epochs = torch.device("cpu"), dados.TINY, 16, 2
        data = treino.load_data(tok, out_dir, treino.TASKS["esnli16k"], n_pairs=48, group_probe=9, word_probe=3,
                                swap_rationales=swap)
        plan = treino.make_plan(len(data.train), WARMUP, batch_size, epochs)
        steps = tuple(range(plan.phase_b + 1, plan.total + 1))
    else:
        out_dir, device, encoder = OUT_DIR, torch.device("cuda"), dados.BERT
        batch_size, epochs, steps = treino.BATCH_SIZE, treino.EPOCHS, STEPS
        data = treino.load_data(tok, out_dir, treino.TASKS["esnli16k"], swap_rationales=swap)
    out = out_dir / "curva.csv"
    done = set(zip(*(pd.read_csv(out)[c] for c in ("arm", "seed")))) if out.exists() else set()
    for arm in args.bracos:  # the cheap arm first: its curves are there after ~25 minutes
        for seed in range(first, last + 1):
            if (arm, seed) in done:
                continue
            rows = curve(arm, seed, data, device, steps, encoder, batch_size, epochs)
            treino.append_csv(out, rows)
            print(f"{arm} seed {seed}: " + " ".join(f"{r['step']}:{r['dev_accuracy']:.3f}" for r in rows), flush=True)


if __name__ == "__main__":
    main()
