"""
Compares unsupervised anomaly detection flags against the
ground-truth Pass/Fail label, to see how well they align.
"""

import pandas as pd
from sklearn.model_selection import train_test_split

from qc_detector.data_loader import load_qc_data, get_feature_columns
from qc_detector.detector import QCAnomalyDetector
from qc_detector.evaluator import evaluate_predictions

df = load_qc_data("data/qc_lims_sample.xlsx")
feature_cols = get_feature_columns()

df["is_true_anomaly"] = df["pass_fail"] == "Fail"

train_df, test_df = train_test_split(
    df, test_size=0.3, random_state=42, stratify=df["is_true_anomaly"]
)

X_train = train_df[feature_cols]
X_test = test_df[feature_cols]

detector = QCAnomalyDetector(contamination=0.07, random_state=42)
detector.fit(X_train)

test_df = test_df.copy()
test_df["pred"] = detector.predict(X_test)

results = evaluate_predictions(test_df, true_label_col="is_true_anomaly", pred_col="pred")

print("--- Anomaly detection vs. Pass/Fail label ---")
print(f"Flagged: {results['flagged_count']}")
print(f"True positives (flagged AND failed): {results['true_positives']}")
print(f"False positives (flagged BUT passed): {results['false_positives']} -> {results['false_positive_ids']}")
print(f"False negatives (not flagged BUT failed): {results['false_negatives']} -> {results['false_negative_ids']}")
print(f"Precision: {results['precision']:.2%}")
print(f"Recall: {results['recall']:.2%}")