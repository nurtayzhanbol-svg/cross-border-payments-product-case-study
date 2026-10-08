# Phase 5 report: evidence-driven product reframing

Branch merged: PR #6 (`devin/1791479252-phase5-reframing`). Baseline before the phase: `71c2d52`, preserved as tag `v1-true-cost-case-study`. Raw workbook unchanged (SHA-256 `f1d7265b…a2d8`, verified before and after every run). Independent portfolio project, not affiliated with Wise or the World Bank.

## 1. Why this phase happened
An independent audit (`docs/archive/independent_audit_2026-10-08.md`) rated the original case study **NOT READY** for a Wise recruiter:
- the "True Cost" idea duplicated what Wise already shows publicly (mid-market rate, fee breakdown, comparison tool);
- Wise appears in the RPW data but had never been analysed;
- three findings were framed too strongly (fixed panel, ≤3% share, "no-fee trap");
- the headline metric could not be measured in a control group;
- the prototype had four medium defects.

## 2. What was done
| Step | Output |
|---|---|
| Preserve baseline | Tag `v1-true-cost-case-study`; v1 docs kept with a "Superseded" banner; audit archived |
| Corrected analysis A1–A6 | `src/rpw/phase5.py`, `outputs/tables/phase5/`, charts `p5_01`–`p5_03`, `docs/phase5_analysis.md` |
| Wise product research | `docs/wise_product_landscape.md` (public sources, accessed 2026-10-08) |
| Customer evidence | `docs/customer_evidence.md` (observed market, observed customer, hypotheses kept separate) |
| Opportunity comparison | `docs/opportunity_assessment_v2.md` (6 options, weighted scoring, decision memo) |
| PRD and experiment | `docs/prd_v2.md`, `docs/measurement_plan_v2.md` |
| Prototype | `prototype/` rebuilt: Regular Send flow, evidence explorer, break-even calculator |
| Recruiter outputs | `docs/case_study_v2.md` (2 pages), `docs/presentation_v2.md` (6 slides), `docs/appendix.md`, README |
| Decision log | `docs/phase5_reframing_decision_log.md` (D0–D16) |

## 3. Analytical corrections
| Original claim | Corrected result |
|---|---|
| F1 "fixed panel 6.50% → 4.33%" | One value per corridor × provider × quarter: 59.7% of 2016 pairs survive to 2025 Q3; survivors' median change −1.15 pp, 66.3% fell. Direction holds; "panel" wording retracted |
| F2 "87.6% of corridors have a quote ≤3%" | Same-quarter 72–77%; robust (p10 ≤3%) 66–71% |
| F4 "no-fee trap" | Retracted: zero-fee quotes are cheaper all-in in 95.1% of corridors with both (median 1.50% vs 4.86% at USD 200) |
| F7 undisclosed FX decline | Partly a 2021 coding change; treating all post-2021 non-Wise zero margins as undisclosed changes no conclusion |
| Audit's "Wise 2.94%, 27.8% cheaper" | Quote-level pooled figure; replaced by corridor-level same-quarter 2.65% / 23.6% |

Sensitivity: four specifications (negative values kept/dropped, zero-margin recoding). Medians move by ≤ ~0.2 pp, shares by ≤ ~5 pp; no conclusion changes direction.

## 4. Wise findings (RPW, 2024 Q3–2025 Q3, unweighted survey quotes)
- 979 Wise records in 127 of 348 corridors, 23 sending markets; bank-account payout (976), mobile wallet (3), no cash.
- Median FX margin 0.01%: Wise's cost is the fee.

| Median across Wise's corridors | USD 200 | USD 500 |
|---|---:|---:|
| Wise total cost | 2.65% | 1.92% |
| Other quotes cheaper than Wise | 23.6% | 23.5% |
| Like-for-like (digital, bank payout) cheaper | 45.0% | 34.4% |
| Wise vs corridor median | −1.21 pp | −0.93 pp |
| Corridors where Wise > 3% | 42.5% | 23.6% |
| Corridors where most quotes are cheaper | 34 | 26 |

- Implied fee: about USD 2.23 fixed + 1.29% variable, so the fixed part adds about 1.1 pp at USD 200.
- Of the 34 weak corridors, 23 are weak at both amounts and 11 only at USD 200 (the pilot set). UAE outbound is weak in all 7 corridors.
- Cheaper offers: 91.2% money transfer operators; 42.7% cash payout, 11.2% wallet.
- All headline figures were reproduced exactly by a separate script reading the raw workbook with openpyxl.

## 5. Wise public product landscape
Already offered: mid-market rate, upfront fee breakdown, comparison tool, scheduled/recurring transfers (balance-funded), mobile-money payout in some countries, Wise Business, Wise Platform, and monthly volume discounts **from £20k / $25k**. Fee reviews in 2024–25 made some small transfers more expensive. Cash pickup was not found (NOT VERIFIED). The logged-in app was not inspected.

## 6. Customer evidence
External only; no interviews, surveys or telemetry were collected or invented. Remittances are typically small and monthly (World Bank UK survey); cost competes with speed, trust and payout channel (World Bank, Western Union, Visa, PYMNTS; vendor sources labelled); regulators police "no fee" claims (CFPB). Not supported: that Wise customers churn because of small-transfer fees.

## 7. Opportunity comparison and decision
| Opportunity | Weighted | Equal weights | Verdict |
|---|---:|---:|---|
| Pricing for regular small senders | **3.80** | 3.67 | Selected as hypothesis |
| Route repricing (23 corridors) | 3.25 | 3.17 | Business-as-usual fee review |
| Cash-pickup corridors | 3.10 | 3.00 | Biggest gap, least testable; main alternative |
| Mobile-wallet expansion | 3.00 | 3.00 | Partly exists |
| Wise Platform for banks | 2.60 | 2.67 | Exists |
| True Cost (v1) | 2.30 | 2.33 | Exists |

**Selected: Regular Send pricing (hypothesis for validation).** A reduced fixed fee on recurring scheduled sends ≤ USD 500 equivalent to the same recipient, in pilot corridors, with the saving shown upfront. What is new: a price based on regularity rather than volume.
**Main risk:** with a USD 4.81 fee and a USD 1.12 discount, retained transfers must rise about 66% (variable cost USD 2.00) or 35% (USD 0.50) to break even.
**Invalidated if:** few regular small senders, current prices already competitive, lift below break-even, or price is not the switching driver.

## 8. Experiment design
Sender-level randomisation; control / fixed fee −50% / −100%; 3–5 corridors; 12 weeks. Primary metric (identical in all arms): share of eligible senders with ≥3 transfers to the same recipient. Guardrails: net fee revenue per sender, contribution per transfer, amount splitting, fraud/AML alerts, complaints. Placeholder baseline 60%, MDE +3 pp → about 4,126 senders per arm. Pre-agreed ship / iterate / stop thresholds. All baselines need Wise telemetry.

## 9. Prototype
React + Vite, `cd prototype && npm ci && npm run dev` (Node 20). Prices are illustrative: implied per corridor from Wise's two survey quotes, no FX margin, labelled on every view. Audit defects fixed: no currency/bucket mismatch (comparisons now use survey shares), no over-maximum recommendation, invalid input rejected rather than rewritten, two-decimal precision, no loading flicker or fake quote refresh.

## 10. QA results
| Check | Result |
|---|---|
| Full pipeline rebuild | No diffs in tracked outputs |
| Python tests / Ruff | 24 passed / clean |
| Prototype tests / typecheck / build | 8 passed / pass / pass |
| Independent Wise recomputation | Exact match |
| External links | 29 of 32 return 200; 3 block automated requests (Western Union PDF, owners.wise.com, World Bank UK PDF) and need a manual browser check |
| Browser E2E (Chrome, recorded) | Journey, validation, pricing rules, evidence filters (127/11), break-even (+66%, "Never") and keyboard completion passed |

**Open defects from browser testing (not yet fixed):**
- MEDIUM: at 375px the corridor dropdown overflows the page (380px; 459px with "Show all 127").
- LOW: keyboard focus falls to the page body after Continue/Back/Confirm.
- LOW: tabs don't respond to arrow keys.
- LOW: typing "200." briefly shows an error and hides the quote.

Not tested: physical devices, other browsers, screen readers.

## 11. Remaining uncertainties
- Survey prices are 2024–25 and unweighted; Wise reprices often.
- One Wise service per corridor is surveyed; pay-in method and balance funding are not covered.
- Competitor quotes may be promotional.
- Wise's cost per transfer, regular-sender share and churn are unknown.
- Customer evidence is external and partly vendor-sponsored.

## 12. Next steps
1. Fix the four prototype defects.
2. Manually check the three blocked links.
3. Re-check current Wise and competitor prices in the 11 pilot corridors.
4. Run 8–12 interviews with monthly senders in two corridors.
