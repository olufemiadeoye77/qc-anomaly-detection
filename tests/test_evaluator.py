"""
Tests for qc_detector.evaluator
"""

import pandas as pd

from qc_detector.evaluator import evaluate_predictions


def test_evaluate_predictions_perfect_detection():
    df = pd.DataFrame({
        "sample_id": ["A", "B", "C", "D"],
        "is_anomaly": [True, False, False, True],
        "pred": [-1, 1, 1, -1],
    })

    results = evaluate_predictions(df, true_label_col="is_anomaly", pred_col="pred")

    assert results["precision"] == 1.0
    assert results["recall"] == 1.0
    assert results["false_positives"] == 0
    assert results["false_negatives"] == 0


def test_evaluate_predictions_with_false_positive_and_negative():
    df = pd.DataFrame({
        "sample_id": ["A", "B", "C", "D"],
        "is_anomaly": [True, False, True, False],
        "pred": [1, -1, -1, 1],  # missed A, false-flagged B, caught C correctly
    })

    results = evaluate_predictions(df, true_label_col="is_anomaly", pred_col="pred")

    assert results["true_positives"] == 1
    assert results["false_positives"] == 1
    assert results["false_negatives"] == 1
    assert "A" in results["false_negative_ids"]
    assert "B" in results["false_positive_ids"]


def test_evaluate_predictions_no_flags():
    df = pd.DataFrame({
        "sample_id": ["A", "B"],
        "is_anomaly": [False, False],
        "pred": [1, 1],
    })

    results = evaluate_predictions(df, true_label_col="is_anomaly", pred_col="pred")

    assert results["flagged_count"] == 0
    assert results["precision"] == 0
    assert results["recall"] == 0