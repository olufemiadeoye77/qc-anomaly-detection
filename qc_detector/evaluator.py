"""
Evaluation utilities for QC anomaly detection results.
"""

import pandas as pd


def evaluate_predictions(df: pd.DataFrame, true_label_col: str, pred_col: str) -> dict:
    """
    Computes precision, recall, and flagged sample breakdown.

    Parameters
    ----------
    df : pd.DataFrame
        Data containing true labels and model predictions.
    true_label_col : str
        Column name for ground-truth anomaly labels (boolean).
    pred_col : str
        Column name for model predictions (-1 = anomaly, 1 = normal).

    Returns
    -------
    dict
        Precision, recall, and sample ID breakdowns.
    """
    flagged = df[df[pred_col] == -1]
    true_positives = flagged[flagged[true_label_col]]
    false_positives = flagged[~flagged[true_label_col]]
    false_negatives = df[(df[pred_col] == 1) & (df[true_label_col])]

    total_true_anomalies = df[true_label_col].sum()

    precision = len(true_positives) / len(flagged) if len(flagged) > 0 else 0
    recall = len(true_positives) / total_true_anomalies if total_true_anomalies > 0 else 0

    return {
        "flagged_count": len(flagged),
        "true_positives": len(true_positives),
        "false_positives": len(false_positives),
        "false_negatives": len(false_negatives),
        "precision": precision,
        "recall": recall,
        "false_negative_ids": false_negatives["sample_id"].tolist() if "sample_id" in df.columns else [],
        "false_positive_ids": false_positives["sample_id"].tolist() if "sample_id" in df.columns else [],
    }