# Threat Model: QC Anomaly Detection Pipeline

## System Overview

The pipeline ingests hourly QC lab sample data (Excel exports from
LIMS), runs it through a trained Isolation Forest model, and flags
anomalous samples for manual review. Current deployment is local
(single machine), with no network exposure, authentication, or
multi-user access control.

## Assets

| Asset | Description | Sensitivity |
|---|---|---|
| `data/qc_lims_sample.xlsx` | Raw QC lab results | Internal — production quality data |
| `models/isolation_forest_qc_final.pkl` | Trained model | Internal — reflects normal/abnormal process behavior |
| `reports/alert_log.txt` | Alert history | Internal — audit-relevant |
| `qc_detector/` | Source code | Internal — IP, logic |

## Threats

### T1: Data Poisoning (Training-Time)
**Description:** If an attacker or process error introduces manipulated
data into the training set, the model learns a false "normal" baseline,
causing genuine anomalies to go undetected.
**Likelihood:** Low (currently local, file-based, no external input)
**Impact:** High — undetected quality failures could reach dispatch
**Mitigation:**
- Validate data source integrity before training (checksum or
  version-controlled snapshots of training data)
- Retrain only from reviewed, approved datasets
- Log which dataset version trained each model (see Step 27)

### T2: Model Staleness / Drift
**Description:** Process conditions change over time (new oil batches,
seasonal variation, equipment changes) but the model isn't retrained,
causing it to flag normal variation as anomalous, or miss new failure
patterns.
**Likelihood:** Medium (expected over time without a retraining cadence)
**Impact:** Medium — alert fatigue (false positives) or missed defects
(false negatives)
**Mitigation:**
- Establish a retraining schedule (e.g., monthly or per significant
  process change)
- Track model performance against Pass/Fail labels over time
- Version models and compare results across versions

### T3: Unauthorized Access to Model or Data
**Description:** Currently, anyone with file system access can read,
modify, or replace the model file or training data with no detection.
**Likelihood:** Medium (depends on who has access to the host machine)
**Impact:** High — could silently disable detection or falsify results
**Mitigation:**
- Restrict file system permissions on `models/` and `data/` to
  authorized QA personnel
- Consider file integrity monitoring (hash verification) for the
  model file before each use
- Move to a proper access-controlled environment before production use

### T4: Silent Failure (No Alert, No Error)
**Description:** If the script fails partway, or receives malformed
data, it may fail silently or produce misleading results rather than
a clear error — a real risk given this is early-stage code.
**Likelihood:** Medium
**Impact:** High — a lab could believe samples were checked when
they weren't
**Mitigation:**
- Add explicit validation and error handling (partially done via
  `data_loader.py` column validation)
- Log every run, successful or failed, with timestamps
- Add a "last successful run" check so missed runs are visible

### T5: Over-Reliance on Model Output (Human Factor)
**Description:** QC staff may over-trust the model and skip manual
judgment, especially for borderline cases (as seen with sample S0052
in earlier testing).
**Likelihood:** Medium (human factor, common in AI deployment)
**Impact:** Medium-High — depends on what decisions are automated vs.
advisory
**Mitigation:**
- Current design is advisory only (flags for manual review, does not
  auto-reject/release product) — this should remain explicit policy
- Document known model limitations (borderline case performance) in
  user-facing materials, not just technical docs

## Out of Scope (Current Phase)

- Network-based attacks (no network exposure yet)
- Multi-user authentication (single-user/local deployment)
- Adversarial input crafted to evade detection (would require the
  model to be exposed to an adversary with query access, which it
  currently is not)

These should be revisited if/when this moves to a shared or
networked deployment.