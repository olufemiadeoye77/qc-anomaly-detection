# Quality Specification Reference

## Important Correction

Earlier project documentation referred to "ISO 9001 Pass/Fail" limits.
This was imprecise: **ISO 9001 is a Quality Management System
standard** (how a company documents, controls, and improves its
processes) — it does not itself specify numeric limits for FFA%,
peroxide value, etc. The actual numeric product specifications for
edible oils come from:

1. **Codex Alimentarius CXS 210-1999** (international standard for
   named vegetable oils, including palm kernel oil, amended through
   2023)
2. **Nigerian Industrial Standards (NIS)** and the **Standards
   Organisation of Nigeria (SON)** specifications for edible oils
3. The plant's own internal specification, which may be stricter than
   either for commercial/contractual reasons

Using a recognized international standard (Codex) alongside the
applicable national standard (NIS/SON) reflects actual regulatory
practice for a Nigerian edible oil producer — most product leaving a
Nigerian plant is expected to meet both.

## Codex Alimentarius CXS 210-1999 — Palm Kernel Oil

| Parameter | Crude PKO | Refined (general Codex limit) |
|---|---|---|
| Free Fatty Acid (as lauric acid) | ≤ 5.0% max | Not separately specified; refined oils expected well below 1% |
| Acid Value | — | ≤ 0.6 mg KOH/g oil (refined, general) |
| Peroxide Value | — | ≤ 5 meq active oxygen/kg (refined, general) |
| Moisture & Impurities | ≤ 0.5% max | Typically tighter for refined (plant-specific) |
| Iodine Value | 14.1 – 21.0 g I₂/100g | Same range (refining does not significantly change IV) |

**Source:** Codex Alimentarius Commission, CXS 210-1999 (Standard for
Named Vegetable Oils).

## Nigerian Industrial Standards / SON — Edible Oils

Figures below are consistently cited across multiple independent
Nigerian academic studies referencing **SON (2000)** and **NIS
(1992), Standard for Edible Vegetable Oil**:

| Parameter | SON/NIS Limit | Oil Type Studied |
|---|---|---|
| Moisture Content | ≤ 0.29% max | Palm oil |
| Iodine Value | 45 – 53 g I₂/100g | Palm oil |
| Saponification Value | 195 – 205 mg KOH/g | Palm oil |
| Peroxide Value | ≤ 10 meq/kg max | Palm oil |
| Specific Gravity | 0.898 – 0.907 | Palm oil |

**Important caveat:** these widely-cited figures are for **palm oil**,
not palm kernel oil. Palm kernel oil has a fundamentally different
fatty acid profile (short/medium-chain, lauric-acid dominant, closer
to coconut oil) than palm oil (long-chain, oleic/palmitic dominant).
This is why PKO's Codex iodine value range (14.1–21.0) is so much
lower than palm oil's NIS range (45–53) — they are different products
with different chemistry, not a discrepancy between standards.

**Open item:** the specific NIS document number and limits for palm
kernel oil specifically (as opposed to palm oil) were not confirmed
in this research pass. This should be obtained directly from SON or
the plant's QA/regulatory affairs team before being used as a
production threshold.

## Status

**Resolved (this phase):** this project now applies the real,
published Codex Alimentarius CXS 210-1999 limits for refined oils
(FFA ≤ 0.3% as oleic acid equivalent, derived from acid value ≤ 0.6
mg KOH/g; peroxide value ≤ 5 meq active oxygen/kg) as its working
Pass/Fail threshold, replacing the earlier arbitrary placeholder
values. This is the internationally recognized standard for named
vegetable oils and is a defensible basis for this prototype.

**Still open (requires the plant's QA team, not resolvable here):**

1. Whether the plant's actual production specification matches these
   Codex limits exactly, follows the NIS standard instead, or applies
   a stricter internal/contractual limit
2. Exact limits for Colour, Saponification Value, Refractive Index,
   and Specific Gravity for PKO specifically (not reliably found in
   this research pass — these are often buyer-contract or
   product-grade specific)
3. Whether limits differ for different product grades or export
   markets

Food-grade production decisions should always defer to the plant's
own confirmed specification over a project prototype's assumptions —
this remains true regardless of how good the model's statistical
performance looks on synthetic data.

## Sources

- Codex Alimentarius Commission, CXS 210-1999, Standard for Named
  Vegetable Oils
- Multiple Nigerian academic studies citing SON (2000) and NIS (1992)
  standards for edible palm oil quality parameters (moisture, iodine
  value, saponification value, peroxide value, specific gravity)