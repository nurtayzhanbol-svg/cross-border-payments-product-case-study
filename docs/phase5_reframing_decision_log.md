# Phase 5 reframing: decision log

| # | Date | Decision | Evidence / reason |
|---|---|---|---|
| D0 | 2026-10-08 | Start from revision `71c2d52` (main after PR #4). Preserve the True Cost case study as annotated tag `v1-true-cost-case-study`; work on branch `devin/1791479252-phase5-reframing`; never merge without approval | Brief §1 |
| D1 | 2026-10-08 | Copy the independent audit into `docs/archive/independent_audit_2026-10-08.md` and use it as the input; no findings reconstructed from memory | Brief §1 |
| D2 | 2026-10-08 | Keep the raw workbook untouched (SHA-256 `f1d7265b…a2d8`, verified by the loader) | Standing rule |
| D3 | 2026-10-08 | Keep `src/rpw/analysis.py` and `docs/eda_findings.md` numbers unchanged; add `src/rpw/phase5.py` with corrected methods so both can be compared | Brief §2 "keep original calculations" |
| D4 | 2026-10-08 | Wise = existing conservative alias map (`Wise`, `TransferWise`); exclude "via Wise" bank products and "Remit Wisely" | Audit A1; avoids merging different services |
| D5 | 2026-10-08 | Wise comparisons are same corridor and same quarter, against credible alternatives (non-negative total and FX margin), aggregated by median per corridor; like-for-like variant (digital + bank payout) reported alongside | Avoids pooling quarters (audit A4) and negative quotes (A6) |
| D6 | 2026-10-08 | The audit's quote-level "Wise 2.94%, 27.8% cheaper" is replaced by corridor-level 2.65% / 23.6% | Different aggregation; independently reproduced |
| D7 | 2026-10-08 | Retract the "no-fee trap" framing (F4) | Zero-fee median 1.50% vs 4.86%; cheaper within 95.1% of corridors |
| D8 | 2026-10-08 | Replace the fixed panel with one value per corridor × provider × quarter; report survival (59.7%) and pair change (−1.15 pp) | Audit A3 |
| D9 | 2026-10-08 | Report "≤3% alternative" as 72–77% same-quarter / 66–71% by p10 instead of 87.6% | Audit A4, sensitivity table |
| D10 | 2026-10-08 | FX-related conclusions survive treating all post-2021 non-Wise zero margins as undisclosed | Audit A5, sensitivity |
| D11 | 2026-10-08 | Do not propose transparency/comparison features: they already exist at Wise | `docs/wise_product_landscape.md` |
| D12 | 2026-10-08 | Six opportunities scored with weights favouring evidence and Wise-specific gap, plus two alternative weightings | `docs/opportunity_assessment_v2.md` |
| D13 | 2026-10-08 | Select O1 "pricing for regular small senders" as a **hypothesis for validation**; record O2 cash pickup as the main strategic alternative | Highest score under all weightings; invalidation criteria in memo §4.8 |
| D14 | 2026-10-08 | Primary experiment metric = retained senders per randomised eligible sender (defined for both arms); net revenue per eligible sender as the main guardrail | Audit M1 (treatment-only North Star) |
| D15 | 2026-10-08 | Rebuild the prototype around the selected direction. Use Wise-compatible illustrative pricing (0 FX margin, fixed + variable fee), label it illustrative, and show RPW Wise-position data as a separate evidence view | Brief §8; audit W2/U1–U5 |
| D16 | 2026-10-08 | Replace the long case study and deck as the entry points with a two-page case study and a six-slide deck; old versions move to the appendix | Audit D1 |
