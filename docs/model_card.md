# Model Card: QC Anomaly Detector (Isolation Forest)

## Model Details

- **Model type:** Isolation Forest (unsupervised anomaly detection)
- **Version:** v1 (contamination=0.07, n_estimators=200, random_state=42)
- **Trained on:** `data/qc_lims_sample.xlsx` (synthetic data matching
  real LIMS structure; not yet trained on real plant data)
- **Framework:** scikit-learn 1.9.1
- **Last trained:** See `models/isolation_forest_qc_final.pkl` file
  timestamp; no automated retraining pipeline yet

## Intended Use

**Primary use:** Advisory flagging of potentially anomalous refined
oil QC samples (FFA, MIV, Colour, PV, Saponification Value,
Refractive Index, Specific Gravity, Iodine Value) for manual review
by QC staff.

**Intended users:** QC lab personnel, QA supervisors reviewing flagged
batches before release decisions.

**Out of scope / not intended for:**
- Automated pass/fail decisions without human review
- Use as the sole basis for product release or rejection
- Deployment on process parameters it was not trained/validated on
- Use on raw material (PKC) QC — currently scoped to refined oil only

## Training Data

- Synthetic dataset structured to match real LIMS export format
- 200 samples, ~4 hourly samples per sheet
- Ground truth Pass/Fail label based on **placeholder** ISO 9001-style
  thresholds (not yet finalized against the plant's actual SOP
  specification limits — see `docs/known_limitations.md`)

## Performance

Evaluated against synthetic Pass/Fail labels on a held-out test set:
- Precision: 80%
- Recall: 100%
- See `README.md` "Validation Against Real Quality Outcomes" section
  for full methodology

## Known Limitations

1. **Trained on synthetic, not real, plant data.** Real-world
   performance is unverified until trained/validated on actual LIMS
   exports.
2. **Pass/Fail thresholds are placeholders**, pending finalized ISO
   9001 spec limits from QA (tracked in SOP-QA-LAB-001).
3. **Borderline cases are harder to catch** — see `docs/threat_model.md`
   discussion of sample S0052, which sat at a moderate statistical
   deviation and was inconsistently flagged.
4. **No drift monitoring** — model does not currently detect when its
   own performance degrades over time.
5. **Single-feature-set assumption** — model will fail (not
   silently mis-predict) if given data with a different schema,
   which is a safe failure mode but not yet gracefully handled.

## Ethical / Operational Considerations

- Model is explicitly **advisory, not autonomous** — this is a
  deliberate design decision, not a current limitation to fix. A QC
  release decision affects product quality and potentially food
  safety; final judgment should remain human.
- False negatives (missed real defects) are treated as more costly
  than false positives (unnecessary manual re-checks) — reflected in
  the contamination=0.07 tuning decision.

## Maintenance

- **Owner:** [To be assigned — QA/QC team]
- **Review cadence:** Recommend quarterly review of model performance
  against actual outcomes once deployed on real data
- **Retraining trigger:** Significant process change, new product
  line, or sustained drop in precision/recall against QC outcomes