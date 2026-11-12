"""
Generates a synthetic Excel file matching the real LIMS sheet structure:
hourly refined oil samples, 4 hours per sheet, with ISO 9001 pass/fail labels.
"""

import pandas as pd
import numpy as np

np.random.seed(42)

n_samples = 200  # simulates 50 sheets x 4 hourly samples

df = pd.DataFrame({
    "sample_id": [f"S{i:04d}" for i in range(n_samples)],
    "hour": np.tile([1, 2, 3, 4], n_samples // 4),
    "FFA": np.random.normal(0.1, 0.02, n_samples),           # typical refined oil FFA ~0.1%
    "MIV": np.random.normal(0.05, 0.01, n_samples),          # moisture & impurity value
    "COLOUR": np.random.normal(2.5, 0.3, n_samples),         # Lovibond color units
    "PV": np.random.normal(1.5, 0.5, n_samples),             # peroxide value meq/kg
    "SAP VALUE": np.random.normal(195, 3, n_samples),        # saponification value
    "RI": np.random.normal(1.459, 0.001, n_samples),         # refractive index
    "S.G": np.random.normal(0.915, 0.003, n_samples),        # specific gravity
    "IV": np.random.normal(18, 1.0, n_samples),              # iodine value
})

# Inject some anomalies/failures (simulate real quality deviations)
fail_idx = np.random.choice(n_samples, size=12, replace=False)
df.loc[fail_idx, "FFA"] += np.random.uniform(0.15, 0.3, 12)
df.loc[fail_idx, "PV"] += np.random.uniform(2, 4, 12)

# Pass/Fail logic based on the real, published Codex Alimentarius
# CXS 210-1999 limit for refined oils (acid value <= 0.6 mg KOH/g,
# approximated here as FFA <= 0.3% as oleic acid equivalent) and the
# Codex refined-oil peroxide value limit (<= 5 meq active oxygen/kg).
# See docs/quality_spec_reference.md for the full standard and
# citation. These are the internationally recognized limits; the
# plant's own QA team should confirm whether a stricter internal or
# contractual specification applies in production.
CODEX_FFA_MAX = 0.3   # % as oleic acid equivalent, derived from acid value <= 0.6
CODEX_PV_MAX = 5.0     # meq active oxygen/kg, refined oils, CXS 210-1999

df["pass_fail"] = np.where(
    (df["FFA"] <= CODEX_FFA_MAX) & (df["PV"] <= CODEX_PV_MAX),
    "Pass",
    "Fail"
)

df.to_excel("data/qc_lims_sample.xlsx", sheet_name="Sheet1", index=False)
print(f"Generated {n_samples} samples -> data/qc_lims_sample.xlsx")
print(f"Fail count: {(df['pass_fail'] == 'Fail').sum()}")