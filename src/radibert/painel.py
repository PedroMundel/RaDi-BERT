"""Measures outside accuracy, read from a classifier's probabilities (docs/2026-11-18-gaps-da-argumentacao.md,
"Gap 8"): calibration, selective prediction, the worst class and the churn between seeds. `p` is always one row of
label probabilities per pair and `y` the gold label ids."""
from itertools import combinations

import numpy as np
from sklearn.metrics import f1_score, recall_score, roc_auc_score

from radibert import esnli_dados as esnli

ECE_BINS = 15
COVERAGE_ACCURACY = 0.95


def ece(p: np.ndarray, y: np.ndarray, bins: int = ECE_BINS) -> float:
    """Expected calibration error of the most probable label: over equal-width confidence bins, the gap between the
    mean confidence and the accuracy, weighted by the share of pairs in the bin. 0 is perfectly calibrated."""
    confidence, right = p.max(1), p.argmax(1) == y
    which = np.minimum((confidence * bins).astype(int), bins - 1)
    return float(sum((which == b).mean() * abs(confidence[which == b].mean() - right[which == b].mean())
                     for b in np.unique(which)))


def confidence_auroc(p: np.ndarray, y: np.ndarray) -> float:
    """How well the confidence tells right answers from wrong ones (0.5 is chance); nan when all are right or wrong."""
    right = p.argmax(1) == y
    if right.all() or not right.any():
        return float("nan")
    return float(roc_auc_score(right, p.max(1)))


def coverage_at(p: np.ndarray, y: np.ndarray, accuracy: float = COVERAGE_ACCURACY) -> float:
    """The largest share of pairs, taken from the most confident down, whose accuracy is still `accuracy` or more."""
    right = (p.argmax(1) == y)[np.argsort(-p.max(1), kind="stable")]
    running = np.cumsum(right) / np.arange(1, len(right) + 1)
    kept = np.flatnonzero(running >= accuracy)
    return float((kept[-1] + 1) / len(right)) if len(kept) else 0.0


def class_scores(p: np.ndarray, y: np.ndarray, labels: dict[int, str] = esnli.LABELS) -> dict:
    """Recall and F1 of each label, and the smallest of the F1s (the worst class)."""
    guess = p.argmax(1)
    recall = recall_score(y, guess, average=None, labels=list(labels), zero_division=0)
    f1 = f1_score(y, guess, average=None, labels=list(labels), zero_division=0)
    return ({f"recall_{name}": float(r) for name, r in zip(labels.values(), recall)}
            | {f"f1_{name}": float(f) for name, f in zip(labels.values(), f1)} | {"worst_f1": float(f1.min())})


def churn(guesses: list[np.ndarray]) -> float:
    """Share of pairs on which two seeds of the same arm answer differently, averaged over every pair of seeds."""
    if len(guesses) < 2:
        raise ValueError("churn needs the answers of at least two seeds")
    return float(np.mean([(a != b).mean() for a, b in combinations(guesses, 2)]))
