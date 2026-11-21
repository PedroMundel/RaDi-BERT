"""The panel outside accuracy (docs/2026-11-18-gaps-da-argumentacao.md, "Gap 8, versão final do painel"), from the
classifiers kept by `rte_treino --fora --salvar-pesos`: calibration, selective prediction and the worst class, on
the e-SNLI dev and on MNLI. Every classifier first has to repeat its run's dev accuracy, as in avaliar_fora.py.

    uv run --frozen python resultados/esnli-treino-16k/painel_pesos.py

One row per arm and seed goes to painel.csv in the first folder, and the probabilities of each classifier to
probabilidades/<arm>-semente-<seed>.npz there (what the churn between seeds is computed from, with --churn, once every
seed of an arm is scored). Runs already in painel.csv are skipped.
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from avaliar_fora import FOLDERS, RELOAD_TOLERANCE, load_classifier, trained_runs

from radibert import esnli_dados as esnli
from radibert import fora_dados as fora
from radibert import painel
from radibert import rte_dados as dados
from radibert import rte_treino as treino


def set_scores(name: str, p: np.ndarray, y: np.ndarray) -> dict:
    scores = {"accuracy": float((p.argmax(1) == y).mean()), "ece": painel.ece(p, y),
              "confidence_auroc": painel.confidence_auroc(p, y), "coverage_at_95": painel.coverage_at(p, y)}
    return {f"{name}_{key}": value for key, value in (scores | painel.class_scores(p, y)).items()}


def churn_table(folder: Path) -> pd.DataFrame:
    """Churn of each arm on each set, over the seeds whose probabilities are saved."""
    rows = []
    for arm, files in group_by_arm(folder).items():
        saved = [np.load(file) for file in files]
        rows.append({"arm": arm, "seeds": len(saved)}
                    | {f"{name}_churn": painel.churn([s[name].argmax(1) for s in saved]) for name in ("dev", "mnli")})
    return pd.DataFrame(rows)


def group_by_arm(folder: Path) -> dict[str, list[Path]]:
    files: dict[str, list[Path]] = {}
    for file in sorted((folder / "probabilidades").glob("*.npz")):
        files.setdefault(file.stem.rsplit("-semente-", 1)[0], []).append(file)
    return {arm: group for arm, group in files.items() if len(group) >= 2}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pastas", nargs="+", type=Path, default=FOLDERS)
    parser.add_argument("--churn", action="store_true", help="only print the churn between the saved seeds")
    args = parser.parse_args()
    folder = args.pastas[0]
    if args.churn:
        print(churn_table(folder).to_string(index=False))
        return
    out = folder / "painel.csv"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    runs = trained_runs(args.pastas)
    tok = dados.load_tokenizers(dados.BERT)
    dev, mnli = esnli.dev_pairs(), fora.mnli_pairs()
    treino.refuse_cut_text({f"mnli_{k}": v for k, v in dados.overlong_counts(mnli, tok).items()})
    dev_items, mnli_items = dados.encode(dev, tok), dados.encode(mnli, tok)
    dev_y, mnli_y = dev["y"].to_numpy(), mnli["y"].to_numpy()
    done = set(map(tuple, pd.read_csv(out)[["arm", "seed"]].to_numpy())) if out.exists() else set()
    (folder / "probabilidades").mkdir(parents=True, exist_ok=True)
    for run in runs.itertuples():
        if (run.arm, run.seed) in done:
            continue
        classifier = load_classifier(run.weights, run.bert)
        p_dev = treino.predict(classifier, dev_items, device)
        reloaded = float((p_dev.argmax(1) == dev_y).mean())
        if abs(reloaded - run.accuracy) > RELOAD_TOLERANCE:
            raise ValueError(f"{run.weights}: dev accuracy {reloaded:.4f} after loading, the run wrote "
                             f"{run.accuracy:.4f}; these are not the weights of that row")
        p_mnli = treino.predict(classifier, mnli_items, device)
        np.savez_compressed(folder / "probabilidades" / f"{run.arm}-semente-{run.seed}.npz", dev=p_dev, mnli=p_mnli)
        row = {"arm": run.arm, "seed": run.seed} | set_scores("dev", p_dev, dev_y) | set_scores("mnli", p_mnli, mnli_y)
        treino.append_csv(out, [row])
        print(f"{run.arm} seed {run.seed}: ece {row['dev_ece']:.4f} auroc {row['dev_confidence_auroc']:.4f} "
              f"pior classe {row['dev_worst_f1']:.4f}", flush=True)


if __name__ == "__main__":
    main()
