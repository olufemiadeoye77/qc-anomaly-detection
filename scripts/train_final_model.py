"""
Trains the final Isolation Forest model using the selected
contamination value (0.07), chosen to prioritize recall for QC safety.
"""

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
import joblib

df = pd.read_csv("data/qc_lab_samples.csv")
feature_cols = ["ffa_percent", "moisture_percent", "impurity_percent", "iodine_value", "peroxide_value"]

injected_indices = [33, 52, 104, 147, 196, 202, 207, 209, 259, 295, 315, 321, 471, 475, 477]
df["is_true_anomaly"] = df.index.isin(injected_indices)

train_df, test_df = train_test_split(df, test_size=0.3, random_state=42, stratify=df["is_true_anomaly"])
X_train = train_df[feature_cols]

model = IsolationForest(n_estimators=200, contamination=0.07, random_state=42)
model.fit(X_train)

joblib.dump(model, "models/isolation_forest_qc_final.pkl")
print("Final model saved -> models/isolation_forest_qc_final.pkl")
print("Configuration: n_estimators=200, contamination=0.07")
