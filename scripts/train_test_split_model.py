"""
Trains Isolation Forest with a proper train/test split, so evaluation
reflects performance on data the model didn't see during training.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
import joblib

df = pd.read_csv("data/qc_lab_samples.csv")

feature_cols = ["ffa_percent", "moisture_percent", "impurity_percent", "iodine_value", "peroxide_value"]
X = df[feature_cols]

# Known injected anomalies (ground truth, for evaluation only)
injected_indices = [33, 52, 104, 147, 196, 202, 207, 209, 259, 295, 315, 321, 471, 475, 477]
df["is_true_anomaly"] = df.index.isin(injected_indices)

# Split: 70% train, 30% test — stratify so anomalies are spread across both sets
train_df, test_df = train_test_split(
    df,
    test_size=0.3,
    random_state=42,
    stratify=df["is_true_anomaly"]
)

print(f"Train set: {len(train_df)} samples ({train_df['is_true_anomaly'].sum()} true anomalies)")
print(f"Test set:  {len(test_df)} samples ({test_df['is_true_anomaly'].sum()} true anomalies)")

X_train = train_df[feature_cols]
X_test = test_df[feature_cols]

# Train ONLY on training data
model = IsolationForest(
    n_estimators=200,
    contamination=0.03,
    random_state=42
)
model.fit(X_train)

# Evaluate ONLY on test data (data the model has never seen)
test_df = test_df.copy()
test_df["anomaly_flag"] = model.predict(X_test)
test_df["anomaly_score"] = model.decision_function(X_test)

flagged = test_df[test_df["anomaly_flag"] == -1]
true_positives = test_df[(test_df["anomaly_flag"] == -1) & (test_df["is_true_anomaly"])]
false_negatives = test_df[(test_df["anomaly_flag"] == 1) & (test_df["is_true_anomaly"])]
false_positives = test_df[(test_df["anomaly_flag"] == -1) & (~test_df["is_true_anomaly"])]

precision = len(true_positives) / len(flagged) if len(flagged) > 0 else 0
true_anomaly_count = test_df["is_true_anomaly"].sum()
recall = len(true_positives) / true_anomaly_count if true_anomaly_count > 0 else 0

print(f"\n--- Test set evaluation (held-out data) ---")
print(f"Flagged as anomalies: {len(flagged)}")
print(f"True positives: {len(true_positives)}")
print(f"False negatives: {len(false_negatives)} -> {false_negatives['sample_id'].tolist()}")
print(f"False positives: {len(false_positives)} -> {false_positives['sample_id'].tolist()}")
print(f"Precision: {precision:.2%}")
print(f"Recall: {recall:.2%}")

# Save model trained only on train data
joblib.dump(model, "models/isolation_forest_qc_v2.pkl")
test_df.to_csv("reports/qc_test_set_results.csv", index=False)

print("\nModel saved -> models/isolation_forest_qc_v2.pkl")
print("Test results saved -> reports/qc_test_set_results.csv")