"""The two test sets read from saved weights (docs/2026-11-18-gaps-da-argumentacao.md, "Gap 7"): MNLI and HANS."""
import numpy as np
import pytest

from radibert import esnli_dados as esnli
from radibert import fora_dados as fora
from radibert.paths import HANS, MNLI

needs_mnli = pytest.mark.skipif(not MNLI.exists(), reason="dados/mnli não baixado (ver dados/README.md)")
needs_hans = pytest.mark.skipif(not HANS.exists(), reason="dados/hans não baixado (ver dados/README.md)")


@needs_mnli
def test_mnli_is_both_validation_splits_with_the_esnli_labels():
    pairs = fora.mnli_pairs()
    assert pairs["split"].value_counts().to_dict() == {"mismatched": 9832, "matched": 9815}
    assert pairs["idx"].is_unique and set(pairs["y"]) == set(esnli.LABELS)
    last = pairs.iloc[-1]  # hand-read from the mismatched file's first row, a contradiction; here it is checked last
    assert pairs.iloc[9815]["sentence1"].startswith("Your contribution helped make it possible") and \
        pairs.iloc[9815]["y"] == 2 and last["split"] == "mismatched"
    assert pairs["y"].value_counts().to_dict() == {0: 6942, 2: 6453, 1: 6252}


@needs_hans
def test_hans_has_the_rte_labels_and_half_of_each():
    pairs = fora.hans_pairs()
    assert len(pairs) == 30000 and pairs["idx"].is_unique
    assert pairs["y"].value_counts().to_dict() == {0: 15000, 1: 15000}  # 1 entailment, as in RTE
    swapped = pairs.iloc[0]  # hand-read: "The president advised the doctor ." / "The doctor advised the president ."
    assert (swapped["sentence1"], swapped["y"], swapped["heuristic"]) == (
        "The president advised the doctor .", 0, "lexical_overlap")


def test_mnli_scores_are_accuracy_overall_and_by_split():
    y = np.array([0, 1, 2, 0])
    p = np.array([[0.7, 0.2, 0.1], [0.1, 0.8, 0.1], [0.5, 0.3, 0.2], [0.2, 0.2, 0.6]])  # right, right, wrong, wrong
    split = np.array(["matched", "matched", "mismatched", "mismatched"])
    scores = fora.mnli_scores(y, p, split)
    assert (scores["mnli_accuracy"], scores["mnli_matched_accuracy"], scores["mnli_mismatched_accuracy"]) == (
        0.5, 1.0, 0.0)
    assert scores["n_mnli"] == 4 and 0.0 <= scores["mnli_roc_auc"] <= 1.0


def test_hans_scores_split_the_accuracy_by_gold_label():
    y = np.array([1, 1, 0, 0, 0])  # 1 entailment
    # a model that answers entailment for everything but the last pair
    p = np.array([[0.9, 0.05, 0.05]] * 4 + [[0.2, 0.5, 0.3]])
    scores = fora.hans_scores(y, p)
    assert scores == {"hans_accuracy": 0.6, "hans_entailment_accuracy": 1.0,
                      "hans_non_entailment_accuracy": pytest.approx(1 / 3), "n_hans": 5}
