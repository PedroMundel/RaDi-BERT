"""Scores the classifiers kept by `rte_treino --fora --salvar-pesos` on MNLI and HANS, with no new training
(docs/2026-11-18-gaps-da-argumentacao.md, "Gap 7"). Before reading any outside set, every classifier loaded from
its file has to repeat, on the e-SNLI dev, the accuracy its own run wrote (instrument check 2); otherwise it stops.

    uv run --frozen python resultados/esnli-treino-16k/avaliar_fora.py

One row per arm and seed goes to mnli-hans.csv in the first folder (resultados/esnli-treino-16k-fora-pesos); runs
already there are skipped. --pastas reads other folders (a smoke run's, to try the script before the weights exist).
"""
import argparse
from pathlib import Path

import pandas as pd
import torch

from radibert import esnli_dados as esnli
from radibert import fora_dados as fora
from radibert import rte_dados as dados
from radibert import rte_treino as treino
from radibert.paths import RESULTADOS
from radibert.rte_modelo import RationaleBert, classifier_only

FOLDERS = [RESULTADOS / f"esnli-treino-16k{part}-fora-pesos" for part in ("", "-calendario", "-embaralhado")]
RELOAD_TOLERANCE = 0.001  # 0.1 point of dev accuracy between the run's own row and the reloaded weights


def trained_runs(folders: list[Path]) -> pd.DataFrame:
    """Every finished run of the folders, with the file its classifier was saved to."""
    frames = []
    for folder in folders:
        path = folder / "resultados.csv"
        if path.exists():
            runs = pd.read_csv(path, dtype={"warmup": str})[["arm", "warmup", "seed", "accuracy", "bert"]]
            frames.append(runs.assign(weights=[
                folder / "pesos" / f"{r.arm}-{r.warmup}-semente-{r.seed}.pt" for r in runs.itertuples()]))
    if not frames:
        raise FileNotFoundError(f"no resultados.csv under {[str(f) for f in folders]}")
    return pd.concat(frames, ignore_index=True)


def load_classifier(weights: Path, bert_name: str):
    classifier = classifier_only(RationaleBert.from_pretrained(bert_name, None, len(esnli.LABELS)))
    classifier.load_state_dict(torch.load(weights, map_location="cpu"))
    return classifier


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pastas", nargs="+", type=Path, default=FOLDERS)
    folders = parser.parse_args().pastas
    out = folders[0] / "mnli-hans.csv"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    runs = trained_runs(folders)
    tok = dados.load_tokenizers(dados.BERT)
    dev, mnli, hans = esnli.dev_pairs(), fora.mnli_pairs(), fora.hans_pairs()
    treino.refuse_cut_text({f"{name}_{k}": v for name, pairs in (("mnli", mnli), ("hans", hans))
                            for k, v in dados.overlong_counts(pairs, tok).items()})
    dev_items, mnli_items, hans_items = (dados.encode(pairs, tok) for pairs in (dev, mnli, hans))
    done = set(map(tuple, pd.read_csv(out)[["arm", "seed"]].to_numpy())) if out.exists() else set()
    for run in runs.itertuples():
        if (run.arm, run.seed) in done:
            continue
        classifier = load_classifier(run.weights, run.bert)
        reloaded = treino.metrics(dev["y"].to_numpy(), treino.predict(classifier, dev_items, device), esnli.LABELS)
        if abs(reloaded["accuracy"] - run.accuracy) > RELOAD_TOLERANCE:
            raise ValueError(f"{run.weights}: dev accuracy {reloaded['accuracy']:.4f} after loading, the run wrote "
                             f"{run.accuracy:.4f}; these are not the weights of that row")
        row = {"arm": run.arm, "seed": run.seed, "dev_accuracy_run": run.accuracy,
               "dev_accuracy_reloaded": reloaded["accuracy"]}
        row |= fora.mnli_scores(mnli["y"].to_numpy(), treino.predict(classifier, mnli_items, device),
                                mnli["split"].to_numpy())
        row |= fora.hans_scores(hans["y"].to_numpy(), treino.predict(classifier, hans_items, device))
        treino.append_csv(out, [row])
        print(f"{run.arm} seed {run.seed}: mnli {row['mnli_accuracy']:.4f} hans non-entailment "
              f"{row['hans_non_entailment_accuracy']:.4f}", flush=True)


if __name__ == "__main__":
    main()
