# Phase 5 analysis: Wise's position and corrected findings

Code: `src/rpw/phase5.py` (`PYTHONPATH=src python -m rpw.phase5`). Outputs: `outputs/tables/phase5/`, `outputs/charts/p5_*.png`, key figures in `outputs/tables/phase5/phase5_key_figures.json` (tested by `tests/test_phase5.py`).
The original EDA (`src/rpw/analysis.py`, `docs/eda_findings.md`) is unchanged so the old and corrected figures can be compared.

**Common rules.** Latest window = the four latest surveyed quarters (2024 Q3, 2024 Q4, 2025 Q1, 2025 Q3; 2025 Q2 was not surveyed). Only `complete_cost_eligible` quotes (identity holds, FX margin disclosed, not a duplicate surplus). All statistics are unweighted survey statistics: **a quote count is not a transaction volume or a market share.**

## A1 — Wise in the RPW survey

**Identification.** `firm == "Wise"` after the existing conservative mapping (`Wise`, `TransferWise`, case/spacing variants). Bank products "via Wise" and the unrelated "Remit Wisely" are *not* merged. Test: `test_wise_aliases_merged`.

**Coverage.** 979 Wise records (1,958 quotes: USD 200 + USD 500) in **127 of 348** surveyed corridors from 23 sending markets. Payout is bank account in 976 records and mobile wallet in 3. No Wise cash-pickup record exists in the window.

**Method.** For every corridor × quarter where Wise was surveyed, Wise's quote is compared with the *credible* quotes of all other providers in the same corridor and quarter (non-negative total cost and FX margin). Then the corridor value is the median over its quarters. "Like-for-like" restricts alternatives to digital access + bank-account payout, the same kind of service as Wise's surveyed product.

| Measure (median across corridors) | USD 200 | USD 500 |
|---|---:|---:|
| Wise total cost | 2.65% | 1.92% |
| Wise fee (% of amount) | 2.54% | 1.80% |
| Wise FX margin | 0.01% | 0.01% |
| Share of other quotes cheaper than Wise | 23.6% | 23.5% |
| Share of like-for-like quotes cheaper than Wise | 45.0% | 34.4% |
| Wise minus corridor median (pp) | −1.21 | −0.93 |
| Wise minus corridor p10 (pp) | +0.49 | +0.48 |
| Wise minus cheapest credible quote (pp) | +1.13 | +0.85 |
| Corridors where Wise is in the cheapest 10% | 30.7% | 29.9% |
| Corridors where Wise is cheaper than the median | 73.2% | 79.5% |
| Corridors where Wise is more expensive than the median | **26.8% (34)** | **20.5% (26)** |
| Corridors where Wise costs more than 3% (SDG target) | **42.5%** | 23.6% |

**Fee structure.** From the two surveyed amounts, the implied Wise fee is `fixed + variable × amount`: median variable 1.29% (IQR 0.72–2.21%) and median fixed USD 2.23 equivalent (IQR 1.51–4.61). This is a fit through two survey points, not Wise's published tariff. At USD 200 the fixed part alone is about 1.1 pp of cost.

**Where Wise loses (USD 200).** 34 corridors. 23 of them are above the median at both amounts (a corridor-pricing problem); 11 only at USD 200 (a small-amount problem). By sending market, the median share of cheaper quotes is 100% for UAE (all 7 UAE corridors), 69.9% Belgium, 58.6% Netherlands, 36.7% USA, 25.4% UK, but 4.7% Canada, 0% Japan and New Zealand. Examples: Germany→Turkey 6.12% vs corridor median 3.02% (USD 500: 3.31%); USA→Egypt 6.82% vs 4.60%; UK→Ghana 3.80% vs 1.34%; UAE→Pakistan 5.30% vs 0.63%.

**Who is cheaper.** 3,195 credible USD 200 quotes undercut Wise in the same corridor and quarter: 91.2% are money transfer operators, 27.5% charge no fee (median FX margin 1.12%, median fee 1.42%). Payout: 45.8% bank account, 42.7% cash, 11.2% mobile wallet. So about half of the cheaper offers are not like-for-like (cash/wallet payout).

**Independent cross-check.** A separate script reading the raw workbook with `openpyxl` (no `src/rpw` code, own identity and denomination filters) reproduces the USD 200 and USD 500 rows above exactly (127 corridors; 2.65/1.92; 23.6/23.5; −1.21/−0.93; 26.8/20.5; 30.7/29.9).
The audit's earlier "median Wise total 2.94%, 27.8% cheaper" was a *quote-level* median pooled over quarters; the corridor-level same-quarter figures above are the corrected method.

**Caveats.** RPW surveys one Wise service per corridor (typically bank-funded, bank payout) at two amounts; it does not cover pay-in method differences, Wise balance funding, speed guarantees or promotional pricing. Cheaper competitor quotes may be promotional or first-transfer offers (CFPB Circular 2024-02 discusses promotional remittance pricing). Survey quarters lag current prices by up to five quarters, and Wise changes fees regularly (see `docs/wise_product_landscape.md`).

## A2 — The zero-fee narrative, corrected

| | USD 200 | USD 500 |
|---|---:|---:|
| Zero-fee share of quotes | 9.4% | 9.8% |
| Median total cost: zero-fee vs fee-bearing | **1.50% vs 4.86%** | **1.46% vs 3.33%** |
| Median FX margin: zero-fee vs fee-bearing | 1.50% vs 1.36% | 1.46% vs 1.34% |
| Within corridor (corridors with both) | zero-fee cheaper in **95.1%** of 205; median gap −3.15 pp | 90.6% of 203; −1.67 pp |

**Correction.** The original F4 ("zero-fee quotes still carry a 1.85% FX margin") is numerically right but its "no-fee trap" framing is not supported. In this survey, zero-fee offers are usually *cheaper* all-in, within the same corridor. The defensible statement is narrower: a "no fee" label does not mean zero cost, because the FX margin carries the price (median 1.50%). Misleading "no fee" marketing is a documented regulatory concern (CFPB Circular 2024-02; Sendwave consent order 2023), but that is about claims, not about zero-fee offers being expensive.

## A3 — Panel repaired

Unit: one median USD 200 total cost per corridor × canonical provider × quarter (POST sheet only).

| | Value |
|---|---|
| Cross-sectional median, 2016 Q2 → 2025 Q3 | 6.00% → 4.13% |
| Pairs in 2016 Q2 / 2025 Q3 / both | 2,813 / 2,720 / 1,679 |
| Survival of 2016 pairs to 2025 | 59.7% |
| 2016 median: survivors vs exiters | 6.48% vs 5.17% |
| 2025 median: survivors vs entrants | 4.54% vs 4.12% |
| Pair-level median change (survivors) | −1.15 pp (mean −0.45 pp); 66.3% fell, 32.5% rose |

**Correction.** The original "fixed panel 6.50% → 4.33%" was not a balanced panel (rows per period grew from 2,404 to 3,791 because each pair could have several services). With one value per pair, prices of surviving pairs did fall (two-thirds fell, median −1.15 pp), so the decline is not only composition. But survivors started *more* expensive than exiters, and the mean change (−0.45 pp) is much smaller than the median, so the fall is uneven. Neither series represents the whole market; both are unweighted. Chart: `p5_03_panel_vs_cross_section.png`.

## A4–A6 — Sensitivity (USD 200, latest window)

| Specification | Median of corridor medians | Median − p10 (pp) | Corridors with a quote ≤3% (pooled) | Corridor-quarters with a quote ≤3% | Corridors with p10 ≤3% | FX share of mean cost | Zero-fee vs fee-bearing median |
|---|---:|---:|---:|---:|---:|---:|---|
| Baseline (keep negatives) | 4.50 | 2.22 | 87.6% | 76.5% | 70.7% | 31.4% | 1.50 vs 4.86 |
| Drop negative totals | 4.58 | 2.15 | 87.6% | 76.5% | 69.5% | 32.2% | 1.66 vs 4.89 |
| Drop negative total or FX margin | 4.72 | 2.09 | 85.3% | 73.3% | 65.8% | 33.7% | 1.66 vs 5.00 |
| Drop zero-margin non-Wise quotes from 2021 Q3 | 4.57 | 2.14 | 84.6% | 72.1% | 67.5% | 35.2% | 1.57 vs 4.87 |

- **A4.** "87.6% of corridors have a quote ≤3%" pools four quarters and rests on a single minimum. The same-quarter version is 72–77%, and a robust version (corridor p10 ≤3%) is 66–71%. Corridors with ≥20 quotes (329): 89.7% (minimum) and 72.0% (p10). Use "about two-thirds to three-quarters" as the claim.
- **A5.** Among `transparent = yes` POST quotes, the share with exactly zero FX margin is about 11% each year from 2021 to 2025 (10.4% excluding Wise), down from 14–17% in 2016–2020. There is no jump when `transparent = no` disappears. Excluding all non-Wise zero-margin quotes after 2021 Q3 (worst case: all are undisclosed) moves the FX share of cost from 31.4% to 35.2% and does not change any conclusion.
- **A6.** One rule is now used for "alternatives": non-negative total cost and FX margin. Under every specification the headline conclusions keep their direction; magnitudes move by at most about 0.2 pp for medians and about 5 pp for shares.

## What changes in the story

| Original claim | Status after Phase 5 |
|---|---|
| F1 "fixed panel 6.50% → 4.33%, not only mix" | Replaced by pair-level −1.15 pp with 59.7% survival; direction holds, panel wording retracted |
| F2 "87.6% of corridors have a ≤3% quote" | Reported as 72–77% same-quarter, 66–71% by p10 |
| F4 "no-fee trap" | Retracted. Zero-fee offers are cheaper all-in in 95% of corridors with both |
| F7 POST decline in undisclosed FX | Treated as partly a coding change; sensitivity shows conclusions robust |
| New: Wise position | Wise is cheaper than the corridor median in about three-quarters of corridors, but more expensive in 34 corridors at USD 200 and above 3% in 42.5% of its corridors at USD 200 |
