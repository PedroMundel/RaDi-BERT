"""Measures of the panel read from saved weights (docs/2026-11-18-gaps-da-argumentacao.md, "Gap 8"), each on a case
worked out by hand."""
import math

import numpy as np
import pytest

from radibert import painel


def probabilities(confidence: list[float], guess: list[int]) -> np.ndarray:
    """Three-label rows whose most probable label is `guess` with probability `confidence`."""
    p = np.zeros((len(guess), 3))
    for row, (c, g) in enumerate(zip(confidence, guess)):
        p[row] = (1 - c) / 2
        p[row, g] = c
    return p


def test_ece_is_the_weighted_gap_between_confidence_and_accuracy_per_bin():
    # two pairs at 0.95, both right (gap 0.05); two at 0.55, one right (gap 0.05): 0.5 * 0.05 + 0.5 * 0.05
    p = probabilities([0.95, 0.95, 0.55, 0.55], [0, 1, 2, 0])
    assert painel.ece(p, np.array([0, 1, 2, 1])) == pytest.approx(0.05)
    # a model that is always sure and always right is perfectly calibrated
    assert painel.ece(probabilities([1.0, 1.0], [0, 1]), np.array([0, 1])) == pytest.approx(0.0)


def test_confidence_auroc_ranks_right_answers_above_wrong_ones():
    # right at 0.9, 0.8 and 0.6; wrong at 0.7: two of the three right answers outrank the wrong one
    p = probabilities([0.9, 0.8, 0.7, 0.6], [0, 0, 0, 0])
    assert painel.confidence_auroc(p, np.array([0, 0, 1, 0])) == pytest.approx(2 / 3)
    assert math.isnan(painel.confidence_auroc(p, np.array([0, 0, 0, 0])))  # no wrong answer: nothing to separate


def test_coverage_is_the_largest_confident_share_that_keeps_the_accuracy():
    p = probabilities([0.9, 0.8, 0.7, 0.6], [0, 0, 0, 0])
    y = np.array([0, 0, 0, 1])  # the least confident answer is the wrong one
    assert painel.coverage_at(p, y, 0.95) == 0.75  # the three most confident are all right; all four give 0.75
    assert painel.coverage_at(p, y, 0.75) == 1.0
    assert painel.coverage_at(p, np.array([1, 0, 0, 0]), 0.95) == 0.0  # the most confident answer is wrong


def test_class_scores_give_recall_and_f1_per_label_and_the_worst_f1():
    y = np.array([0, 0, 1, 1, 2, 2])
    p = probabilities([0.9] * 6, [0, 1, 1, 1, 2, 0])
    scores = painel.class_scores(p, y)
    assert (scores["recall_entailment"], scores["recall_neutral"], scores["recall_contradiction"]) == (0.5, 1.0, 0.5)
    assert scores["f1_entailment"] == pytest.approx(0.5)  # precision 1/2, recall 1/2
    assert scores["f1_neutral"] == pytest.approx(0.8)  # precision 2/3, recall 1
    assert scores["f1_contradiction"] == pytest.approx(2 / 3)  # precision 1, recall 1/2
    assert scores["worst_f1"] == pytest.approx(0.5)


def test_churn_is_the_mean_disagreement_over_every_pair_of_seeds():
    guesses = [np.array([0, 1, 2, 0]), np.array([0, 1, 1, 0]), np.array([0, 2, 2, 0])]
    assert painel.churn(guesses) == pytest.approx((1 / 4 + 1 / 4 + 2 / 4) / 3)
    with pytest.raises(ValueError):
        painel.churn(guesses[:1])
