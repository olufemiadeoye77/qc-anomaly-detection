"""
Investigates why S0052 is consistently missed by the anomaly detector.
"""

import pandas as pd

df = pd.read_csv("data/qc_lab_samples.csv")

feature_cols = ["ffa_percent", "moisture_percent", "impurity_percent", "iodine_value", "peroxide_value"]

missed_sample = df[df["sample_id"] == "S0052"]
print("S0052 values:")
print(missed_sample[feature_cols].to_string(index=False))

print("\nDataset-wide stats for comparison:")
print(df[feature_cols].describe().loc[["mean", "std", "min", "max"]])

# How many standard deviations away is S0052 on each feature?
print("\nS0052 deviation from mean (in standard deviations):")
for col in feature_cols:
    mean = df[col].mean()
    std = df[col].std()
    val = missed_sample[col].values[0]
    z_score = (val - mean) / std
    print(f"  {col}: z-score = {z_score:.2f}")