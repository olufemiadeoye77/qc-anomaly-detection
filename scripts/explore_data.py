"""
Exploratory analysis of synthetic QC lab data.
Visualizes distributions of each quality parameter.
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/qc_lab_samples.csv")

print("Shape:", df.shape)
print("\nSummary statistics:")
print(df.describe())

print("\nMissing values:")
print(df.isnull().sum())

# Plot distributions for each QC parameter
numeric_cols = ["ffa_percent", "moisture_percent", "impurity_percent", "iodine_value", "peroxide_value"]

fig, axes = plt.subplots(2, 3, figsize=(15, 8))
axes = axes.flatten()

for i, col in enumerate(numeric_cols):
    axes[i].hist(df[col], bins=30, edgecolor="black")
    axes[i].set_title(col)
    axes[i].set_xlabel("Value")
    axes[i].set_ylabel("Frequency")

fig.delaxes(axes[5])  # remove the unused 6th subplot
plt.tight_layout()
plt.savefig("reports/qc_distributions.png", dpi=150)
print("\nSaved distribution plots -> reports/qc_distributions.png")