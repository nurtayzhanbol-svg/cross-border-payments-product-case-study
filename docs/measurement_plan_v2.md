# Measurement and experiment plan v2: Regular Send pricing pilot

All baselines are **assumptions**. Every metric marked (T) needs Wise internal telemetry, which this project does not have.

## 1. Primary metric (defined identically for treatment and control)
**Retained regular senders:** share of randomised eligible senders who complete ≥ 3 transfers to the same recipient in the 12 weeks after randomisation. (T)
It is measured for every randomised sender, whether or not they saw or used Regular Send, so it is not a treatment-only metric.

## 2. Secondary metrics
| Group | Metric |
|---|---|
| Activation | Share of eligible senders who set up a Regular Send schedule (treatment) / any recurring schedule (control) (T) |
| Conversion | Quote → completed transfer rate for eligible quotes (T) |
| Customer value | Fees paid per eligible sender; recipient-received amount per sender (T) |
| Volume | Transfers and send volume per eligible sender over 12 weeks (T) |

## 3. Guardrails
| Type | Guardrail | Threshold (assumption) |
|---|---|---|
| Business | **Net fee revenue per eligible sender** over 12 weeks (T) | Not below control by more than the pre-agreed investment, e.g. −5% |
| Unit economics | Contribution per transfer after variable cost (T) | ≥ 0 |
| Behaviour | Average transfer amount; share of transfers just under the cap (splitting) (T) | No significant shift |
| Risk / compliance | Fraud and AML alert rate on scheduled transfers; failed/returned transfers (T) | No increase beyond noise |
| Customer | Support contacts and complaints per sender; schedule cancellation rate (T) | No increase |

## 4. Design
- **Population:** senders with ≥ 2 transfers ≤ USD 500 equivalent to the same recipient in the previous 90 days, in 3–5 pilot corridors.
- **Randomisation unit:** sender (customer profile), stratified by corridor and prior send frequency. Not by session or transfer, to avoid seeing different prices for the same recipient.
- **Arms:** control (current pricing), A (fixed fee −50% on scheduled eligible transfers), B (fixed fee −100%).
- **Interference:** households with shared recipients could compare prices; record recipient overlap and exclude shared recipients from the analysis if needed.
- **Analysis:** intention-to-treat difference in proportions; CUPED with prior-90-day transfer count to reduce variance.

## 5. Baseline, MDE and sample size
- Assumed baseline for the primary metric: 60% (placeholder until telemetry is available).
- Minimum detectable effect: +3 pp (60% → 63%), α = 0.05 two-sided, power 80%.
- Sample size per arm: n = (z₀.₉₇₅ + z₀.₈)² × [p₁(1−p₁) + p₂(1−p₂)] / (p₂ − p₁)² = 7.85 × 0.473 / 0.0009 ≈ **4,126 eligible senders per arm** (≈12,400 total for three arms; add about 10% for attrition, and a Bonferroni correction for two comparisons would raise this to about 5,000 per arm).
- If pilot corridors cannot supply this, widen eligibility or accept a larger MDE (+5 pp needs about 1,500 per arm).

## 6. Duration
12 weeks of exposure to match the 12-week primary metric (at least three monthly cycles), plus enrolment time. A 60-day repeat metric would not fit a 4–6-week test (audit M2).

## 7. Decision thresholds
| Outcome | Decision |
|---|---|
| Primary metric +3 pp or more **and** net revenue guardrail met **and** no risk guardrail breached | **Ship** in pilot corridors; plan wider rollout with current-price re-check |
| Primary metric up but revenue guardrail missed | **Iterate:** smaller discount, lower cap, or only corridors with the largest gap |
| No significant lift, or any risk guardrail breached | **Stop**; return to discovery (price may not be the driver) |

## 8. Telemetry requirements (T)
Sender ID, recipient ID, corridor, amount, fee components, scheduled vs ad-hoc flag, arm, quote shown, schedule created/cancelled, transfer completed/failed, fraud/AML alerts, support contacts, variable cost per transfer.

## 9. Before the experiment
Desk re-check of current prices in candidate corridors; internal analysis of regular-sender share and churn; 8–12 interviews (`docs/customer_evidence.md` §3).
