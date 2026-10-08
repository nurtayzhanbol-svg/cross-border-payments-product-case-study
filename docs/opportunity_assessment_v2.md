# Opportunity assessment v2 and decision memo

Inputs: `docs/phase5_analysis.md` (market data), `docs/wise_product_landscape.md` (what Wise already does), `docs/customer_evidence.md` (external customer evidence). The original assessment (`docs/product_opportunity.md`, True Cost) is kept for comparison and tagged `v1-true-cost-case-study`.

**Bottom line.** No opportunity has enough *customer* evidence to be called proven. The selected direction is the most promising **hypothesis for validation**, not a validated solution.

## 1. Candidates

| # | Opportunity | Target customer | Customer problem (hypothesis) | Supporting evidence | Existing Wise coverage |
|---|---|---|---|---|---|
| O1 | **Pricing for regular small senders** | People sending ≤ ~USD 500 to the same family member every month | A fixed fee per transfer takes 1–2% of a small remittance; in some corridors cheaper MTO offers exist | Wise implied fixed fee ≈ USD 2.23 (≈1.1 pp at USD 200); Wise >3% in 42.5% of its corridors at USD 200 vs 23.6% at USD 500; 34 corridors above median at USD 200; most remitters send monthly (World Bank UK survey) | Scheduled transfers exist; volume discounts only above £20k/$25k a month; fee reviews have raised fixed fees on some routes |
| O2 | Cash-pickup corridors | Senders whose recipients need cash | Wise cannot pay out cash, so these senders use MTOs | 132 surveyed corridors from Wise's sending markets with no Wise quote; median 70.7% cash-payout quotes; median cost 4.92%; 29% of non-digital senders prefer face-to-face (WU) | Not offered (absence NOT VERIFIED) |
| O3 | Mobile-wallet payout expansion | Senders to wallet-heavy destinations | Recipient has a wallet, not a bank account | Wallet payout median 3.61% vs cash 4.94% (USD 200); 11% of quotes cheaper than Wise are wallet payouts | Partly offered (bKash, M-PESA, M-PAiSA) |
| O4 | Route-level repricing in the 23 corridors uncompetitive at both amounts | Senders on UAE outbound, EU→Morocco/Turkey routes | Wise is simply more expensive there | UAE corridors 100% cheaper alternatives; DEU→TUR 6.12% vs 3.02% | Wise runs regular fee reviews (business-as-usual) |
| O5 | True Cost transparency (v1) | Any sender | Doesn't understand all-in cost | Market dispersion only | **Exists** (mid-market rate, fee breakdown, compare tool) |
| O6 | Wise Platform for remittance-heavy banks | Bank customers sending remittances | Banks are the most expensive provider type (median 9.65%) | F5; Platform partners grow | **Exists** (Wise Platform) |

## 2. Detailed evaluation

| | O1 Regular small senders | O2 Cash pickup | O3 Wallet payout | O4 Route repricing | O5 True Cost | O6 Platform for banks |
|---|---|---|---|---|---|---|
| Differentiation vs Wise today | New price construct for a segment Wise's discounts ignore | New capability | Extension | BAU pricing | None | None |
| User value | ~USD 1–2 per transfer at USD 200; certainty | High for cash-dependent recipients | Medium | Medium | Low | Medium (indirect) |
| Business value | Uncertain: gives up fee revenue; may raise retention/volume | Potentially large, new segment | Medium | Medium | Low | High but existing |
| Feasibility | High: pricing rule on existing scheduled transfers | Low: agent networks, cash AML, licences | Medium: partner aggregators | Medium: cost drivers unknown | High | Existing |
| Regulatory / operational | Fee disclosure, fair-pricing rules, notice periods for price changes; amount-splitting abuse | Heavy (cash AML, agent oversight) | Wallet partner due diligence, KYC | Standard | Low | Partner contracts |
| Key risks | Cannibalising fee revenue from senders who would stay anyway; splitting large transfers | Brand dilution, fraud, cost | Partner reliability | Competitor quotes may be promotional | Duplicates Wise | Already pursued |
| Evidence gaps | Share of Wise senders who are regular small senders; price elasticity; cost per scheduled transfer | Recipient demand; unit cost | Wallet penetration per corridor | Internal cost structure | Customer problem | Bank demand |
| MVP testability | **High**: randomised pricing pilot in a few corridors | Low | Medium: corridor launch, waitlist | Medium: route price test | Medium | Low (B2B sales cycle) |

## 3. Prioritisation framework

Scores 1–5. Weights put evidence and Wise-specific gap first and feasibility last, so the easiest-to-build option cannot win on ease alone.

| Criterion (weight) | O1 | O2 | O3 | O4 | O5 | O6 |
|---|---:|---:|---:|---:|---:|---:|
| Evidence strength (25%) | 4 | 3 | 3 | 4 | 2 | 3 |
| Wise-specific gap / differentiation (20%) | 4 | 5 | 3 | 3 | 1 | 2 |
| Customer value (15%) | 3 | 4 | 3 | 3 | 2 | 3 |
| Testability of an MVP (15%) | 5 | 2 | 3 | 3 | 3 | 1 |
| Feasibility incl. regulatory (15%) | 4 | 1 | 3 | 3 | 5 | 3 |
| Business value (10%) | 2 | 3 | 3 | 3 | 1 | 4 |
| **Weighted score** | **3.80** | 3.10 | 3.00 | 3.25 | 2.30 | 2.60 |
| Equal weights | 3.67 | 3.00 | 3.00 | 3.17 | 2.33 | 2.67 |
| Feasibility weight set to 0 (others rescaled) | 3.76 | 3.47 | 3.00 | 3.29 | 1.82 | 2.53 |

O1 ranks first under all three weightings. O2 is the biggest *strategic* gap but scores lowest on feasibility and testability; it is recorded as the main alternative (see §4.7).

## 4. Decision memo: O1, pricing for regular small senders (hypothesis for validation)

**4.1 Why this problem?** Wise's mid-market-rate model removes the FX margin, so for Wise the remaining cost is the fee. Because part of the fee is fixed, Wise's cost rises at small amounts: in RPW, Wise exceeds 3% in 42.5% of its corridors at USD 200 vs 23.6% at USD 500, and is above the corridor median in 34 corridors at USD 200. Remittances are typically small and monthly.

**4.2 Why this customer?** The regular small sender (same recipient, monthly, ≤ ~USD 500) is the core remittance customer, and is the one Wise's existing price benefits skip: volume discounts start at £20k/$25k per month, and recent fee reviews raised fixed fees on some routes.

**4.3 Why important?** For a USD 200 monthly sender, 1 pp is USD 24 a year; competitors in 34 surveyed corridors already undercut Wise at this amount. If these senders leave, the loss is recurring.

**4.4 Why Wise is well placed.** Scheduled transfers and stored recipients already exist, so the product is a pricing rule plus small UX changes, not new rails. Predictable scheduled flows may let Wise pre-fund or batch liquidity (hypothesis; Wise's internal cost data is unknown).

**4.5 What Wise already offers.** Mid-market rate, fee transparency, comparison tool, scheduled/recurring transfers, monthly volume discounts above £20k.

**4.6 What is new.** A price tied to *regularity*, not *volume*: a reduced fixed fee for committed recurring small sends in pilot corridors, shown upfront with the annual saving. Plus an evidence-based corridor selection method (where Wise is above the RPW median at USD 200).

**4.7 Why not the alternatives?** O2 cash pickup is the largest gap but needs agent networks and cash AML; it cannot be tested cheaply and is outside Wise's account-to-account model. O3 wallets is partly built already. O4 is routine fee review. O5 and O6 already exist.

**4.8 What would invalidate the decision?**
- Wise telemetry shows few regular small senders, or they don't churn.
- Current Wise prices (not 2024–25 survey prices) are already competitive in the pilot corridors.
- The pilot shows no lift in retained senders, or the lift doesn't cover the revenue given up (break-even in `docs/measurement_plan_v2.md`).
- Senders split large transfers to game the price, or fraud rises on scheduled sends.
- Interviews show that speed, cash payout or trust, not price, drive switching.

**4.9 Trade-offs considered.** Lower prices do not automatically raise adoption or retention; price may not be the switching driver; revenue is given up on every pilot transfer; a fixed fee may reflect real per-transfer costs (pay-in, compliance checks) that do not fall for small amounts; price changes have notice requirements; and promotional competitor prices may not last.
