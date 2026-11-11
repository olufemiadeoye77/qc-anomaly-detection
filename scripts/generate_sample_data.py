"""
Generates synthetic PKO/PKC quality control lab data
for anomaly detection prototyping.
"""

import pandas as pd
import numpy as np

np.random.seed(42)

n_samples = 500

# Simulate typical QC parameters for palm kernel oil/cake
data = {
    "sample_id": [f"S{i:04d}" for i in range(n_samples)],
    "ffa_percent": np.random.normal(3.5, 0.5, n_samples),       # Free Fatty Acid %
    "moisture_percent": np.random.normal(0.15, 0.03, n_samples), # Moisture %
    "impurity_percent": np.random.normal(0.2, 0.05, n_samples),  # Impurities %
    "iodine_value": np.random.normal(18, 1.5, n_samples),        # Iodine value
    "peroxide_value": np.random.normal(2.5, 0.8, n_samples),     # Peroxide value
}

df = pd.DataFrame(data)

# Inject a small number of anomalies (simulating real QC deviations)
anomaly_idx = np.random.choice(n_samples, size=15, replace=False)
df.loc[anomaly_idx, "ffa_percent"] += np.random.uniform(2, 4, 15)
df.loc[anomaly_idx, "peroxide_value"] += np.random.uniform(3, 6, 15)

df.to_csv("data/qc_lab_samples.csv", index=False)
print(f"Generated {n_samples} samples -> data/qc_lab_samples.csv")
print(f"Injected anomalies at indices: {sorted(anomaly_idx.tolist())}")