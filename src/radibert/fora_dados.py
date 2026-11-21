"""Test sets outside the e-SNLI distribution that are scored from saved classifier weights, and their scores
(docs/2026-11-18-gaps-da-argumentacao.md, "Gap 7"): MNLI's two validation splits and the HANS evaluation set.
Every pairs frame has idx, y, sentence1 and sentence2, as rte_dados.encode reads."""
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, roc_auc_score

from radibert import esnli_dados as esnli
from radibert.paths import HANS, MNLI

MNLI_SPLITS = ("matched", "mismatched")


def mnli_pairs() -> pd.DataFrame:
    """Matched then mismatched validation. MNLI's label ids are e-SNLI's (0 entailment, 1 neutral, 2 contradiction;
    ClassLabel names read from the Hub on 18/11)."""
    frames = [pd.read_parquet(MNLI / f"validation_{split}.parquet").assign(split=split) for split in MNLI_SPLITS]
    pairs = pd.concat(frames, ignore_index=True).rename(
        columns={"premise": "sentence1", "hypothesis": "sentence2", "label": "y"})
    if not pairs["y"].isin(list(esnli.LABELS)).all():
        raise ValueError("MNLI pair without one of the three labels")
    return pairs.assign(idx=range(len(pairs)))[["idx", "y", "sentence1", "sentence2", "split", "genre"]]


def hans_pairs() -> pd.DataFrame:
    """HANS with RTE's two labels (y 1 entailment, 0 non-entailment)."""
    pairs = pd.read_csv(HANS, sep="\t", usecols=["gold_label", "sentence1", "sentence2", "heuristic"])
    return pairs.assign(idx=range(len(pairs)), y=(pairs["gold_label"] == "entailment").astype(int))[
        ["idx", "y", "sentence1", "sentence2", "heuristic"]]


def mnli_scores(y: np.ndarray, p: np.ndarray, split: np.ndarray) -> dict:
    """Three-label accuracy on every pair (the measure Gap 7 reads) and on each split, one-vs-rest ROC-AUC beside."""
    right = p.argmax(1) == y
    return {"mnli_accuracy": float(right.mean()),
            "mnli_roc_auc": roc_auc_score(y, p, multi_class="ovr", average="macro", labels=list(esnli.LABELS)),
            "n_mnli": len(y)} | {f"mnli_{name}_accuracy": float(right[split == name].mean()) for name in MNLI_SPLITS}


def hans_scores(y: np.ndarray, p: np.ndarray) -> dict:
    """A three-label model read on two labels, as on RTE: the guess is entailment when that is the most probable
    label. Accuracy overall and within each gold label (a model that always says entailment gets 1.0 and 0.0)."""
    guess = (p.argmax(1) == esnli.ENTAILMENT).astype(int)
    return {"hans_accuracy": accuracy_score(y, guess),
            "hans_entailment_accuracy": accuracy_score(y[y == 1], guess[y == 1]),
            "hans_non_entailment_accuracy": accuracy_score(y[y == 0], guess[y == 0]), "n_hans": len(y)}
