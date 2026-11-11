"""
Evaluates anomaly detection results against known injected anomalies,
and visualizes flagged points against normal distribution.
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("reports/qc_samples_with_anomaly_flags.csv")

# These are the sample indices we know were artificially injected as anomalies
injected_indices = [33, 52, 104, 147, 196, 202, 207, 209, 259, 295, 315, 321, 471, 475, 477]
injected_ids = set(f"S{i:04d}" for i in injected_indices)

flagged_ids = set(df[df["anomaly_flag"] == -1]["sample_id"])

true_positives = injected_ids & flagged_ids
false_negatives = injected_ids - flagged_ids
false_positives = flagged_ids - injected_ids

print(f"True positives (correctly flagged): {len(true_positives)}")
print(f"False negatives (missed anomalies): {len(false_negatives)} -> {sorted(false_negatives)}")
print(f"False positives (flagged, not injected): {len(false_positives)} -> {sorted(false_positives)}")

precision = len(true_positives) / (len(true_positives) + len(false_positives))
recall = len(true_positives) / (len(true_positives) + len(false_negatives))
print(f"\nPrecision: {precision:.2%}")
print(f"Recall: {recall:.2%}")

# Visualize: scatter of ffa_percent vs peroxide_value, colored by flag
fig, ax = plt.subplots(figsize=(8, 6))
normal = df[df["anomaly_flag"] == 1]
anomaly = df[df["anomaly_flag"] == -1]

ax.scatter(normal["ffa_percent"], normal["peroxide_value"], c="steelblue", label="Normal", alpha=0.6)
ax.scatter(anomaly["ffa_percent"], anomaly["peroxide_value"], c="red", label="Flagged anomaly", edgecolor="black", s=80)

ax.set_xlabel("FFA %")
ax.set_ylabel("Peroxide Value")
ax.set_title("QC Anomaly Detection: FFA % vs Peroxide Value")
ax.legend()
plt.tight_layout()
plt.savefig("reports/anomaly_scatter.png", dpi=150)
print("\nSaved scatter plot -> reports/anomaly_scatter.png")