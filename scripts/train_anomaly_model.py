"""
Trains an Isolation Forest model to detect anomalous QC lab samples.
"""

import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

df = pd.read_csv("data/qc_lab_samples.csv")

feature_cols = ["ffa_percent", "moisture_percent", "impurity_percent", "iodine_value", "peroxide_value"]
X = df[feature_cols]

# contamination = expected proportion of anomalies in the data
# we injected 15/500 = 3%, so we use that as a starting estimate
model = IsolationForest(
    n_estimators=200,
    contamination=0.03,
    random_state=42
)

model.fit(X)

# -1 = anomaly, 1 = normal
df["anomaly_flag"] = model.predict(X)
df["anomaly_score"] = model.decision_function(X)

flagged = df[df["anomaly_flag"] == -1].sort_values("anomaly_score")

print(f"Total samples: {len(df)}")
print(f"Flagged as anomalies: {len(flagged)}")
print("\nFlagged samples (lowest score = most anomalous):")
print(flagged[["sample_id", "ffa_percent", "peroxide_value", "anomaly_score"]].to_string(index=False))

# Save model and results
joblib.dump(model, "models/isolation_forest_qc.pkl")
df.to_csv("reports/qc_samples_with_anomaly_flags.csv", index=False)

print("\nModel saved -> models/isolation_forest_qc.pkl")
print("Results saved -> reports/qc_samples_with_anomaly_flags.csv")