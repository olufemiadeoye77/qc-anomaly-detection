# AI Risk Register

| Field | Entry |
|---|---|
| **Model/System Name** | QC Anomaly Detector (Isolation Forest) |
| **Model ID** | qc-detector-v1 |
| **Owner** | [To be assigned] |
| **Purpose** | Advisory anomaly flagging for refined oil QC samples |
| **Risk Tier** | **Medium** (see justification below) |
| **Autonomy Level** | Advisory only — human review required before any release decision |
| **Data Sensitivity** | Internal production quality data — no personal data, no trade secrets beyond normal process confidentiality |
| **Deployment Status** | Prototype / not yet deployed on real plant data |

## Risk Tier Justification

Rated **Medium** rather than Low or High because:
- **Not High:** The model does not make autonomous decisions; a human
  always reviews flagged results before action is taken. No direct
  safety, financial, or irreversible impact from model error alone.
- **Not Low:** Quality control directly relates to product safety and
regulatory compliance (Codex Alimentarius and NIS/SON edible oil
standards). An undetected defect reaching dispatch carries real business and reputational risk, even with
  human review as a backstop (humans can also miss things the model
  should have flagged).

## Required Controls (per Risk Tier)

- [x] Human-in-the-loop review required before any action (satisfied —
  advisory design)
- [x] Model card documented (`docs/model_card.md`)
- [x] Threat model documented (`docs/threat_model.md`)
- [ ] Trained/validated on real plant data (pending — currently
  synthetic only)
- [ ] Finalized Codex/NIS spec thresholds incorporated (pending QA sign-off)
- [ ] Formal model owner assigned
- [ ] Retraining/monitoring cadence formally scheduled
- [ ] Access controls on model and training data files (pending)

## Review History

| Date | Reviewer | Notes |
|---|---|---|
| 2026-11-12 | [Project author] | Initial risk register entry; prototype phase |