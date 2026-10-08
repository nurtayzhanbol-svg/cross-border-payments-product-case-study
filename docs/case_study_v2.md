# Small, regular remittances: where Wise's pricing model is weakest

*Independent Product Management portfolio case study using public data only. Not affiliated with, endorsed by, or based on internal data from Wise or the World Bank.*

## 1. Question and data
**Question:** where could Wise most credibly improve outcomes for remittance senders, given what it already offers?
**Data:** World Bank Remittance Prices Worldwide (RPW), 253,960 surveyed services, 2011–2025, each priced at USD 200 and USD 500. Survey quotes are unweighted; they are not transaction volumes or market shares. The pipeline verifies the raw workbook's hash, keeps every anomaly as a flag, and is tested and independently re-computed ([`phase5_analysis.md`](phase5_analysis.md)).

## 2. What the market data shows
- **Prices fell but remain dispersed.** Among provider–corridor pairs present in 2016 and 2025, the median USD 200 cost fell 1.15 pp (66% of pairs fell); only 60% of 2016 pairs survive, so this is not a full-market trend. The latest median corridor cost is 4.50%.
- **"Free" isn't the trap it seemed.** Zero-fee quotes are cheaper all-in in 95% of corridors where both types exist (median 1.50% vs 4.86%). The original "no-fee trap" framing was retracted.
- **Small amounts cost more.** A fixed fee weighs more on USD 200 than on USD 500.

## 3. What Wise already does (public sources, accessed 2026-10-08)
Mid-market rate with no markup, an upfront fee breakdown, a public comparison tool, scheduled/recurring transfers, mobile-money payout to some wallets, and monthly volume discounts **from £20k / $25k**. Cash pickup was not found (NOT VERIFIED). The original "True Cost" transparency idea therefore duplicated Wise and was dropped ([`wise_product_landscape.md`](wise_product_landscape.md)).

## 4. Wise in the survey
Wise was surveyed in 127 of 348 corridors (2024 Q3–2025 Q3).

| Median across Wise's corridors | USD 200 | USD 500 |
|---|---:|---:|
| Wise total cost (FX margin ≈ 0.01%) | 2.65% | 1.92% |
| Other quotes cheaper than Wise | 23.6% | 23.5% |
| Corridors where Wise is above 3% | **42.5%** | 23.6% |
| Corridors where most quotes are cheaper than Wise | **34** | 26 |

Wise beats the corridor median in about three-quarters of corridors. Its weak spot is the fee: an implied fixed component of about USD 2.23 adds about 1.1 pp at USD 200. In 11 corridors Wise is uncompetitive at USD 200 but not at USD 500.

## 5. Customer evidence (external, not collected by this project)
Remittances are typically small and monthly (World Bank survey of UK migrants); cost matters but competes with speed, trust and payout channel (World Bank, Western Union, Visa, PYMNTS; vendor sources labelled). There is no Wise customer data here, so customer impact remains a hypothesis ([`customer_evidence.md`](customer_evidence.md)).

## 6. Options compared
Six opportunities were scored on evidence, Wise-specific gap, customer value, testability, feasibility and business value ([`opportunity_assessment_v2.md`](opportunity_assessment_v2.md)):

| Opportunity | Score | Verdict |
|---|---:|---|
| **Pricing for regular small senders** | **3.80** | Selected as hypothesis |
| Route repricing in 23 corridors | 3.25 | Business-as-usual fee review |
| Cash-pickup corridors | 3.10 | Biggest gap, least testable; main alternative |
| Mobile-wallet expansion | 3.00 | Partly exists |
| Platform for banks | 2.60 | Exists |
| True Cost (v1) | 2.30 | Exists |

The ranking holds under equal weights and with feasibility removed.

## 7. Proposal: Regular Send pricing (hypothesis for validation)
Wise rewards **volume**; nothing rewards **regularity**, the pattern of a typical remittance. Proposal: on existing scheduled transfers, a reduced fixed fee for recurring small sends (≤ USD 500 equivalent, same recipient) in pilot corridors, with the per-transfer and annual saving shown upfront ([`prd_v2.md`](prd_v2.md)).
**Business risk:** every discounted transfer gives up revenue. With a USD 4.81 fee, a USD 1.12 discount and an assumed USD 2.00 variable cost, retained transfers must rise about 66% to break even; with USD 0.50 cost, about 35%. The idea only works if costs of scheduled transfers are low or retention gains large.

## 8. How it would be tested
Sender-level randomised pilot in 3–5 corridors: control, −50% and −100% fixed fee. **Primary metric** (same for every arm): share of eligible senders with ≥3 transfers to the same recipient in 12 weeks. Guardrails: net fee revenue per eligible sender, contribution per transfer, amount splitting, fraud/AML alerts, complaints. At a 60% placeholder baseline and +3 pp MDE: about 4,100 senders per arm, 12 weeks. Ship / iterate / stop rules in [`measurement_plan_v2.md`](measurement_plan_v2.md).

## 9. What would change my mind, and limits
Stop if Wise data shows few regular small senders, current prices already close the gap, the pilot lift misses break-even, or interviews show speed/cash/trust rather than price drive switching. Limits: unweighted 2024–25 survey prices, one Wise service per corridor, no internal cost data, external customer evidence only.

**Prototype:** `prototype/` — Regular Send flow, RPW evidence explorer and break-even calculator (illustrative prices). **Deck:** [`presentation_v2.md`](presentation_v2.md). **Details:** [`appendix.md`](appendix.md).
