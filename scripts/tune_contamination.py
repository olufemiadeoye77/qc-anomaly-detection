"""
Tests multiple contamination values to find the best precision/recall
tradeoff on the held-out test set.
"""

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split

df = pd.read_csv("data/qc_lab_samples.csv")
feature_cols = ["ffa_percent", "moisture_percent", "impurity_percent", "iodine_value", "peroxide_value"]

injected_indices = [33, 52, 104, 147, 196, 202, 207, 209, 259, 295, 315, 321, 471, 475, 477]
df["is_true_anomaly"] = df.index.isin(injected_indices)

train_df, test_df = train_test_split(df, test_size=0.3, random_state=42, stratify=df["is_true_anomaly"])
X_train = train_df[feature_cols]
X_test = test_df[feature_cols]

print(f"{'Contamination':<15}{'Flagged':<10}{'TP':<5}{'FP':<5}{'FN':<5}{'Precision':<12}{'Recall':<10}")

for contamination in [0.02, 0.03, 0.05, 0.07, 0.10]:
    model = IsolationForest(n_estimators=200, contamination=contamination, random_state=42)
    model.fit(X_train)

    preds = model.predict(X_test)
    test_eval = test_df.copy()
    test_eval["pred"] = preds

    flagged = test_eval[test_eval["pred"] == -1]
    tp = len(flagged[flagged["is_true_anomaly"]])
    fp = len(flagged[~flagged["is_true_anomaly"]])
    fn = test_eval["is_true_anomaly"].sum() - tp

    precision = tp / len(flagged) if len(flagged) > 0 else 0
    recall = tp / test_eval["is_true_anomaly"].sum()

    print(f"{contamination:<15}{len(flagged):<10}{tp:<5}{fp:<5}{fn:<5}{precision:<12.2%}{recall:<10.2%}")