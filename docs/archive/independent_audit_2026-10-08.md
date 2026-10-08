# Independent audit: cross-border-payments-product-case-study

Audited revision: `71c2d52` (main, PR #4 merged). PR #5 (work log only) is still open and was not audited as content.
Audit date: 2026-10-08. Auditor posture: adversarial; audit only. No repository files, commits or PRs were changed (`git status` is clean in both checkouts).
Method: fresh clone at `~/audit_work/repo`, fresh venv, no-cache rebuild, and a **separate re-implementation** of the F1–F9 statistics. It reads the raw workbook with `openpyxl` read-only streaming and shares no code with `src/rpw`. On top of that: Wise public sources and a recorded browser run of the prototype.

---

## 1. Executive verdict

**Overall readiness: NOT READY** to show a Wise recruiter in its current form (it would be READY WITH MAJOR REVISIONS after the product reframing in §7).
**Confidence:** high on data and reproducibility findings (independently recomputed); medium-high on product and interview judgements (these are expert judgement, not measurable).

The data work is real and reproducible: every headline number reproduces. But the selected product, "True Cost", restates what Wise already does publicly and campaigns for. The prototype also models a provider that marks up the exchange rate, which is the exact practice Wise's brand is built against. For a Wise APM application this is the single most damaging issue, and it cannot be fixed with better analysis.

**Three strongest aspects**
1. **Reproducibility and data integrity.** The raw workbook hash is preserved. A clean no-cache rebuild gives byte-identical processed files, and the analysis re-run leaves the working tree clean. The independent re-implementation matches F1–F9 to two decimals.
2. **Methodological honesty about the data.** Undisclosed FX is never treated as zero. FX-rate levels are not compared. Anomalies are flagged, not deleted. Descriptive and causal statements are separated.
3. **Explicit uncertainty.** The persona and customer needs are labelled as hypotheses, and limitations are documented throughout.

**Five most serious weaknesses**
1. **True Cost largely duplicates existing Wise functionality** (W1). The prototype's "our rate vs mid-market" margin model contradicts Wise's no-markup pricing.
2. **The analysis never looks at Wise in its own dataset** (A1). Wise has 979 latest-window quotes in 127 corridors, with a median FX margin of 0.01%. The most interview-relevant analysis is missing.
3. **No customer-problem evidence** (P1). RPW measures prices, not comprehension, trust or switching. The core premise, "senders don't understand the all-in cost", is unobserved.
4. **The F4 framing is contradicted by the same data** (A2). Zero-fee quotes are cheaper overall (median total 1.50% vs 4.86%). The "no-fee trap" story is not what the data shows.
5. **The North Star is not comparable across experiment arms, and the fixed-panel claim is overstated** (M1, A3).

---

## 2. Scorecard (1–5)

| # | Dimension | Score | Evidence-based justification |
|---|---|---:|---|
| 1 | Data correctness | **4** | All F1–F9 figures reproduce independently. Cost identity holds for 99.18% of PRE and 99.70% of POST quotes. FX margin recomputed from rates matches within 0.05 pp for 99.7% of 2025 Q3. Deductions: negative FX margins are kept in means; p10 includes negative totals while the minimum excludes them; the post-2021 transparency coding is taken at face value. |
| 2 | Analytical rigor | **3** | Good caveats and denominators. But the "fixed panel" is not fixed (row count 2,404 → 3,791) and suffers survivorship (only 58.4% of 2016 pairs survive). "87.6% of corridors have a quote ≤3%" pools four quarters and relies on a single minimum. No volume weighting is possible. Wise's own position is not analysed. |
| 3 | Problem discovery | **2** | The market-level problem (prices are dispersed; SDG 3% not met) is shown. The customer problem is asserted, the persona is fictional, and there is no secondary user evidence (complaints data, FCA/CFPB research, app reviews). |
| 4 | Product differentiation | **1** | Fee and markup breakdown, mid-market reference, competitor comparison with markup shown in money, and "0% fee" warnings all exist publicly on wise.com (§5). The only novel element is an RPW survey-percentile badge. |
| 5 | Solution quality | **2** | Coherent quote → review → confirm flow, but the solution targets a provider that has a margin. The benchmark is self-flattering (the illustrative price is below the median in 24/24 tested cases). Survey data from up to five quarters ago is presented next to a live quote. |
| 6 | Metrics / experimentation | **2** | Sensible guardrails and funnel. But the North Star "sees the all-in cost and completes" is definitionally near zero for control. There is no baseline, MDE or sample size. Repeat sending at 60 days does not fit a 4–6-week test. Cannibalisation and interference are unaddressed. |
| 7 | Prototype usability | **3** | The full journey works and is keyboard-accessible, with no 375 px overflow. Faults: silent input mutation (`-200` → `200`), the benchmark currency/bucket mismatch, it recommends £12,500 when the maximum is £5,000, a skeleton flicker on every keystroke, and "fresh quote" returns the same quote. |
| 8 | Documentation / storytelling | **3** | Complete and well-linked, but very long (15+ docs). The narrative leads with data plumbing rather than a user insight, and recruiters will read only about 2 pages. The case study does not confront the "Wise already does this" objection. |
| 9 | Reproducibility | **5** | Hash verified, byte-identical rebuild in 2m00s, analysis idempotent, 16 pytest tests and 4 Vitest tests pass, typecheck, build and ruff are clean. |
| 10 | Wise interview relevance | **2** | The domain is relevant (pricing transparency is Wise's mission). The proposal reads as unaware of Wise's product, and the data includes Wise without using it. |

---

## 3. Reproducibility audit (Part 1)

| Check | Command / method | Result |
|---|---|---|
| Raw SHA-256 | `sha256sum data/raw/*.xlsx` | **PASSED** (`f1d7265b…a2d8`) |
| Clean rebuild | fresh clone + venv, `python -m rpw.build --no-cache` | **PASSED**: 253,960 × 84 wide; 507,920 × 94 long; 894 providers; 2m00s |
| Processed artefacts match the committed ones | `sha256sum -c` against the committed hashes | **PASSED**: all 5 files byte-identical |
| EDA idempotent | re-ran `rpw.analysis`; `git status` | **PASSED**: no diff in charts or tables |
| Independent row counts | separate openpyxl loader | **PASSED**: PRE 49,491; POST 204,469 |
| Python tests | `pytest -q` | **PASSED**: 16/16 (these test internal consistency only; see note) |
| Lint | `ruff check src tests` | **PASSED** |
| Frontend | `npm ci`, `npm run typecheck`, `npm test`, `npm run build` | **PASSED**: 4/4 tests; 152.55 kB JS |
| Browser journey | recorded Chrome run by the testing agent | **PASSED with MEDIUM defects** (§6) |
| Notebooks | not re-executed end-to-end | **NOT VERIFIED** |
| Hidden dependencies | Node is only available via nvm (`nvm use 20`) | LOW: documented in the README? **NOT VERIFIED**; the agent had to load nvm manually |

Note on tests: `test_reported_stats.py` checks that the docs match the pipeline's own output. It does not check correctness. Correctness was established here only by the independent re-implementation.

Leakage, silent exclusions and naming:
- No silent row loss: the row-count invariant is asserted and was verified independently.
- Exclusions are explicit flags. In the latest window only 5 of 26,408 USD 200 quotes are excluded (total missing), so eligibility filters are **not** a material selection bias for the latest-window findings.
- For PRE trends, excluding the 8.2% undisclosed quotes is material but documented.
- `flag_numeric_stored_as_text` is assigned by period list rather than detected per value (`flags.py`). It is misleadingly named but harmless.

---

## 4. Data methodology audit (Part 2)

| Topic | Verdict | Evidence |
|---|---|---|
| PRE/POST harmonisation | Sound | Sheet-specific fields are kept separate; only core fields are stacked. |
| Grain (record vs quote) | Sound | Long format has exactly 2 rows per record; amount pairing is via `record_key`, which equals the independent `(sheet, period, id)` pairing (26,245 pairs). |
| USD 200 / 500 | Sound | Denomination is checked; non-standard denominations are flagged. 11.7% of pairs have identical % cost at both amounts. |
| Fee / FX / total identity | Sound | Independent residual check passes for 99.2% (PRE) and 99.7% (POST). Margin = (1 − applied/interbank) × 100 is reproduced for 99.7% of 2025 Q3 quotes. |
| Transparency | **Partially sound** | The pre-2021 handling is correct. After the 2021 coding shift there are 0 undisclosed quotes in the latest window, yet about 11% of `transparent = yes` POST quotes have exactly 0% margin in every year from 2021 to 2025. "Complete-cost eligible" may still contain undisclosed FX. This should be stated as a limitation on F4 and F2. |
| Payout currency / FX direction | Sound | FX levels are never compared; only unit-free percentages are used. |
| Negative / extreme costs | **Inconsistent** | The minimum excludes negative totals, but p10 includes them (median gap 2.22 pp vs 2.09 pp when negatives are excluded). 1,512 negative-FX-margin quotes (5.7% of eligible latest) enter the means; excluding them moves the FX share from 31.4% to 33.7%. |
| Duplicates | Sound | Surplus rows (133 PRE / 189 POST) are excluded and duplicate-group size is kept. |
| Provider aliases | Sound, conservative | Wise and TransferWise are merged (7,642 + 2,618 raw rows). "Banque Populaire via Wise" and "Remit Wisely" are correctly **not** merged. |
| Corridor key | Sound | Codes are used and the 95 POST mismatches with the raw corridor are flagged. |
| Missing periods | Documented | 2011 Q2/Q4, 2012 Q2/Q4 and 2025 Q2 are missing. Charts should show gaps rather than join over them (**NOT VERIFIED** visually). |
| Fixed panel | **Flawed as described** | See A3. |
| Weighting | Inherent limit | All statistics are unweighted survey statistics; corridors count equally regardless of flows. |

---

## 5. Findings register

| ID | Sev. | Finding | Evidence | Impact | Verify | Recommended correction |
|---|---|---|---|---|---|---|
| W1 | **CRITICAL** | True Cost's core features already exist at Wise | §7 matrix: wise.com/gb/compare (exchange rate, total fees, recipient gets, markup), /gb/large-amounts (markup in GBP per provider), /gb/mid-market-rate (warns about "0% fee" traps), help article 2522717 (fee split, mid-market, rate lock) | The proposal reads as "build what you already have". The interview's first question will sink it. | Open the URLs | Reposition (§8): either "extend Wise's transparency to where Wise isn't / can't be" or pick another opportunity. |
| W2 | **HIGH** | The prototype models a provider that marks up FX ("Our rate vs mid-market", margins of 0.5–1.2%) | `pricing.ts` ILLUSTRATIVE; `App.tsx` "Our rate vs mid-market" | Contradicts Wise's pricing model and brand; it looks like a generic MTO feature. | Run the prototype | Model a Wise-style quote (0 markup) or relabel it explicitly as a competitor/market-wide tool. |
| A1 | **HIGH** | Wise's position in RPW is not analysed | Independent: latest window has 979 Wise quotes, 127 corridors, median total 2.94%, median FX margin 0.01%, 89.8% of quotes with margin ≤0.5%. In the median corridor, 27.8% of surveyed quotes are cheaper than Wise; Wise is at or below the corridor p10 in only 17.3% of corridors. | Misses the most relevant insight: Wise's issue is not transparency but **price competitiveness at small amounts in remittance corridors** (its percentage fee and minimum fee versus zero-fee MTO promotions). | `indep/analyse.py` "Wise" block | Add a Wise-specific analysis: where and at what amounts Wise is not cheapest, and why (fee vs margin). |
| P1 | **HIGH** | Customer problem is unevidenced | The PRD persona is labelled "hypothesis, not research"; RPW has no behaviour data | The case rests on an assumed comprehension gap. | Read `prd.md` §Target user | Add public secondary evidence (e.g. regulator studies, app-store/Trustpilot themes) and a small set of real conversations; or reframe the case as evidence-limited. |
| A2 | **HIGH** | F4's "zero-fee quotes still carry a 1.85% mean margin" implies a no-fee trap; the data shows zero-fee quotes are much cheaper overall | Independent: zero-fee median total 1.50% vs fee-bearing 4.86% (latest window, USD 200) | Undercuts H1's motivating story. A reviewer who checks will see a framing bias. | `eda_key_figures.json` composition block | Report both numbers and restate F4: "margin is material, but zero-fee offers are not on average more expensive". |
| A3 | **HIGH** | The "fixed panel" is neither fixed nor survivorship-free | 1,642 (indep.) / 1,679 (pipeline; the difference comes from name normalisation) pairs, but panel rows 2,404 (2016 Q2) → 2,978 (2020 Q1) → 3,791 (2025 Q3): multiple and new services per pair. Only 58.4% of 2,813 pairs from 2016 Q2 survive, and survivors started higher (median 6.57%) than those that exited (5.11%). | "So the decline is not only a change in sample mix" is overstated. Direction holds at pair level (one median per pair per endpoint: 6.57 → 4.59, median change −1.17 pp, 66.9% fell). | `analysis.py` trend panel | Use one value per pair per period, report the pair-level change, disclose survivorship, and soften the claim. |
| M1 | **HIGH** | North Star is ill-defined for an A/B test | "Share of quoted transfers where the sender sees the all-in cost and completes": control by definition does not see it | No valid treatment–control comparison; it doubles as conversion. | `measurement_plan.md` §North Star | Primary metric = quote-to-completion (or 30-day sender retention); comprehension as a survey secondary; state baseline, MDE and N with explicit assumed numbers. |
| M2 | MEDIUM | Experiment design gaps | 60-day repeat KPI vs 4–6-week test; no baseline or MDE; no interference, novelty or cannibalisation discussion; revenue guardrail has no threshold | Will not survive "what would make you stop?" | Read the plan | Specify thresholds, test length matched to KPIs, and a holdout. |
| A4 | MEDIUM | "87.6% of corridors have at least one surveyed quote ≤3%" is fragile | It pools 4 quarters and uses one minimum quote. Same-quarter share of corridor-quarters is 76.5%; corridor p10 ≤3% in 69.5%; 19 corridors have <20 quotes (52.6% of those). | Overstates how available cheap options are. | `indep/analyse.py` F2 | Report the p10-based share and the same-quarter share alongside it. |
| A5 | MEDIUM | Post-2021 transparency may be miscoded | ~11% of `yes` quotes have exactly 0 margin every year 2021–25; the `no` code disappears | "Complete-cost" quotes may include undisclosed FX, which biases F4 FX share downward. | Zero-margin share by year | Sensitivity: exclude zero-margin cross-currency quotes. |
| A6 | LOW | Negative-value handling is inconsistent (p10 vs minimum; negative FX in means) | 2.22 vs 2.09 pp; FX share 31.4 vs 33.7% | Small numeric effect | as above | Apply one consistent rule and show the sensitivity. |
| A7 | LOW | Composition chart stacks median fee + median FX, which ≠ median total | `analysis.py` composition chart | Visual mismatch | Compare the chart with the tables | Stack means, or label it clearly. |
| A8 | LOW | Provider-type (F5) and region (F8) contrasts are confounded by corridor mix | Bank n = 3,882 is concentrated in specific corridors; non-bank FI n = 12; MENA taxonomy split (acknowledged) | Descriptive only (already stated) | — | Add within-corridor comparisons as done for F6. |
| U1 | MEDIUM | Benchmark ignores currency: GBP/EUR amounts compared with "~USD 200/500"; the bucket switches at 350 local units | Browser: GBR→IND £349 "Lower than 90%…" vs £350 "Below the median…" at the same 1.18% | A misleading claim inside a transparency product | Recording, `benchmark-threshold.png` | Convert to USD or interpolate, and show the survey date. |
| U2 | MEDIUM | Self-flattering benchmark: illustrative price below the median in 24/24 cases and below p10 in 8/24 | Testing-agent matrix | Looks like marketing, not neutral information | `matrix.json` | Show neutral positioning and explain why a provider would display a benchmark it could lose on. |
| U3 | MEDIUM | "Sending £12,500 would cost…" when the maximum is £5,000 | `recommends-12500.png` / `rejects-12500.png` | Broken recommendation | Enter 5000 | Cap the comparison at the maximum. |
| U4 | MEDIUM | Silent input mutation and over-precision | `-200` → `200`, `2a00` → `200`; `200.123` accepted, with recipient amounts differing from `200.12` | Wrong-amount risk in a money flow | `validation-matrix.png` | Reject invalid input with an explanation; limit to 2 decimal places. |
| U5 | LOW | 350 ms skeleton on every keystroke (524 px layout jump); "fresh quote" is unchanged; restart does not reset; "will arrive" / "You paid" wording | Recording | Polish | — | Debounce input; simulate a new rate. |
| D1 | MEDIUM | Story length and voice | 15+ docs; the case study leads with the pipeline | Recruiters will not dig | — | A 2-page case study plus a 6-slide deck; the rest goes to an appendix. |
| D2 | LOW | PR #5 still open | GitHub | Housekeeping | — | Merge or close. |

---

## 6. F1–F9 verification table

All figures are latest window = 2024 Q3, 2024 Q4, 2025 Q1, 2025 Q3; USD 200 (cc1); complete-cost eligible, unless stated otherwise. "Indep." means recomputed by the separate raw loader.

| F | Claim | Indep. result | Denominator / filter | Validity and caveats | Verdict |
|---|---|---|---|---|---|
| F1 | Median 6.00% (2016 Q2) → 4.13% (2025 Q3); mean 7.44 → 6.36; panel of 1,679 pairs 6.50 → 4.33 | 6.00 → 4.13; 7.44 → 6.36. Panel: 1,642 pairs, rows 6.54 → 4.36; pair-level 6.57 → 4.59 (Δ −1.17 pp, 66.9% fell) | Per-period eligible quotes; 361 → 348 corridors | Cross-section is a composition comparison. The panel is unbalanced and survivor-selected (A3). The direction is robust; the magnitude and "not only mix" wording are overstated. | **PARTIALLY VERIFIED** |
| F2 | 348 corridors; median of corridor medians 4.50%; 43.4% >5%; 15.5% ≤3%; 87.6% have a quote ≤3%; median-to-p10 gap 2.22 pp | 348; 4.50; 43.4; 15.5; 87.6; 2.22 (2.09 excluding negatives) | Corridors with ≥1 eligible quote; median 72 quotes, 8 providers per corridor | Unweighted; minimum pooled across quarters (A4); p10 includes negatives (A6) | **VERIFIED** (numbers); interpretation **PARTIALLY** |
| F3 | 26,245 pairs; median 4.50% vs 3.13%; USD 500 cheaper in 86.4%; FX 2.03 vs 2.02 | 26,245; 4.50 vs 3.13; 86.4%; 2.03 vs 2.02 (11.7% equal) | Records eligible at both amounts | Valid within-record comparison; mechanically driven by fixed fees | **VERIFIED** |
| F4 | FX ≈ 31% of mean cost; FX > fee in 33.5%; 9.4% zero-fee; zero-fee mean margin 1.85% | 31.4; 33.5; 9.4; 1.85 | Eligible latest quotes | Omits that zero-fee median total is 1.50% vs 4.86% (A2); negative FX included; possible undisclosed zeros (A5) | **VERIFIED** (numbers); framing **MISLEADING** |
| F5 | Provider-type medians: MTO 4.24, bank 9.65, mixed 5.06, mobile 2.66, post 7.14, non-bank FI 71.24 (n = 12) | 4.24; 9.66*; 5.06; 2.66; 7.14; 71.24 | Same; n = 21,807 / 3,882 / 525 / 92 / 85 / 12 | *0.01 rounding difference. Confounded by corridor mix; small n for 3 groups | **VERIFIED** (descriptive) |
| F6 | 326 corridors with both channels; digital cheaper in 81%; median gap 1.89 pp | 326; 81.0%; 1.89. Same corridor and same firm: 942 pairs, 77.7%, 1.74 pp | Corridors with both digital-only and non-digital quotes | Stronger than documented (holds within firm), still not causal (payout and speed differ) | **VERIFIED** |
| F7 | Undisclosed FX 8.2% PRE, 1.8% POST | 8.2; 1.8 | All cc1 records | The POST decline is partly a coding change (A5), not necessarily behaviour | **VERIFIED** (numbers); interpretation **PARTIALLY** |
| F8 | Sub-Saharan Africa 5.74% highest; South Asia 3.45% lowest | 5.74; 3.45 | Eligible latest quotes by destination region | Mixed MENA taxonomy (acknowledged); ".." region 527 quotes at 3.41%; unweighted | **VERIFIED** |
| F9 | 43/348 corridors with no quote ≤3%; 12 with none ≤5%; 19 with no digital quote | 43; 12; 19. Of the 12, 3 have <10 quotes | Corridors in the latest window | A screen, not proof of being underserved (thin samples; survey coverage ≠ market) | **VERIFIED** (numbers) |

Prototype benchmarks (`benchmarks.json`): p10, median, p90 and n for all 6 corridors match the independent recomputation exactly. **VERIFIED.**

Representative raw-row trace: a 20-row stratified sample (PRE and POST, 2011–2025, transparent yes and no, extreme cases such as ZAF→MWI MoneyGram at 75.8%) recomputes fee% + margin = total within ±0.01 pp, and margin from rates matches. **VERIFIED.**

---

## 7. Wise feature-overlap matrix (sources accessed 2026-10-08)

| True Cost element | Exists at Wise? | Evidence |
|---|---|---|
| Upfront fee shown before paying | **Yes** | https://wise.com/help/articles/2522717/fees-for-sending-money: fees shown at setup, including payment-method fee |
| Mid-market rate reference | **Yes** (core proposition) | https://wise.com/gb/mid-market-rate |
| FX markup expressed as money | **Yes** (for competitors) | https://wise.com/gb/large-amounts/: per-provider "exchange rate markup £27.25" plus "cost of transfer" |
| All-in cost / recipient-gets comparison against other providers | **Yes** | https://wise.com/gb/compare/ (rate, total fees, recipient gets, "Show rate details"); https://wise.com/gb/compare/providers ; https://wise.com/gb/compare/currencies ; methodology at https://wise.com/gb/compare/disclaimer |
| "No fee" trap explainer | **Yes** | https://wise.com/gb/mid-market-rate ("watch out when a service promises a 0% fee"); Hidden Fees UK report: https://wise.com/imaginary-v2/images/8d3aa501ca9425ba71ae78036e1cc053-Hidden%20Fees%20UK%202024.pdf |
| Fee / FX split in the send calculator | **Yes** | https://wise.com/nz/blog/wise-vs-orbitremit ("all the costs of transfer and exchange split out") |
| Rate lock / quote expiry | **Yes** | Guaranteed rate: help article 2522717; batch GR expiry: https://wise.com/help/articles/5iWcIUdYHyTQMnezSzx4n3/how-do-i-send-exact-amounts-with-batch-payments |
| Fixed + variable fee model (amount sensitivity) | **Yes** (pricing structure) | https://docs.wise.com/guides/product/send-money/quotes/pricing ; https://wise.com/pr/pricing/business |
| Public advocacy on hidden FX | **Yes** | G20+ Scorecard 2026: https://wise.com/imaginary-v2/images/eb14d8e8b90fe746da557c3bb679138d-G20-Report-2026.pdf |
| **Independent survey benchmark (World Bank RPW percentile) inside the send flow** | **Not found** | Potentially novel, but it is backward-looking survey data (up to 5 quarters old), unweighted, and covers only the corridors RPW samples. A neutral third-party reference is plausible, but Wise's live compare tool already does this better. |
| **In-flow nudge "send more at once to cut % cost"** | **Not found in-flow** (NOT VERIFIED inside the logged-in app) | Small and arguably against the customer's need when remittances are needed periodically; Wise's percentage fee makes the gain smaller than in the prototype. |

What the live authenticated Wise app shows was **NOT VERIFIED**: no account was used. Public pages, help centre, developer docs and Wise reports were the evidence.

**Conclusion:** about 80–90% of True Cost is existing Wise functionality. For Wise it is repackaging, not a meaningful expansion. The remaining novelty (an RPW benchmark badge) is weak.

---

## 8. Product-thinking audit (Part 4)

1. **Market problem:** yes. Costs are dispersed and above the SDG 3% target in many corridors (F1, F2, F9). This is established descriptively.
2. **Customer problem:** no. Comprehension, trust, comparison effort and switching are not observed. It must be reframed as a hypothesis with a discovery plan, or supported by external evidence.
3. **Persona:** specific (London → Lagos nurse), but invented. Note that GBR→NGA is the corridor whose benchmark p10 is 0.11%, i.e. already highly competitive.
4. **JTBD:** reasonable but generic ("know exactly what it costs"). Wise already serves this job.
5. **Alternatives:** H2 (small-transfer pricing) and H3 (underserved corridors) were dismissed partly because they are hard to prototype. Given A1, **H2 is actually the Wise-relevant opportunity**: Wise's FX margin is about 0, so its remaining cost is the fee, which bites at small amounts.
6. **Was H1 chosen for evidence or ease?** Mostly for feasibility. The case study explicitly calls it "the most feasible MVP". The evidence for H1 (dispersion, opacity) is market-wide, not a Wise problem.
7. **MVP scope:** tidy, but scoped for a generic provider.
8. **Metrics:** the guardrails are good; the North Star is flawed (M1).
9. **Experiment credibility:** low as specified (M2). For Wise the control would already show most of the treatment.
10. **First challenge from an experienced fintech PM:** "We already show the fee, the mid-market rate and a comparison table. What problem of ours does this solve, and how do you know customers have it?"

**Fixable by better analysis:** A1 (Wise position), A2 (F4 framing), A3 (panel), A4, A5, A6, M1, M2, U1–U5.
**Requires new customer evidence:** P1 (comprehension gap), whether small-amount senders exist in volume, willingness to switch, and how much the benchmark matters to trust.

---

## 9. Portfolio / interview readiness (Part 7)

| Dimension | Assessment |
|---|---|
| Technical completeness | High (5/5) |
| Analytical validity | Good with fixable overstatements (3.5/5) |
| Product quality | Weak for Wise (2/5) |
| Originality | Low (1–2/5) |
| Interview readiness | Not yet (2/5). The commits are under the applicant's name, but most content was produced by Devin, so the applicant must be able to defend every method choice personally (panel, eligibility, transparency coding). |

**Five hardest interview questions to expect**
1. "Wise already shows the mid-market rate, the fee and a competitor comparison. What does True Cost add, and for whom?"
2. "Wise is in your dataset. In which corridors and at which amounts is Wise *not* the cheapest, and what would you do about it?"
3. "What evidence do you have that senders misunderstand the cost, rather than choosing on speed, cash pickup or trust?"
4. "Your North Star counts people who 'see the all-in cost'. How do you measure that in the control group, and what result would make you kill the feature?"
5. "Your fixed panel loses 40% of 2016 pairs, and survivors started more expensive. How much of the decline is real? And why are zero-fee quotes cheaper overall if 'no fee' is a trap?"

---

## 10. Recommended next actions (ranked by impact ÷ effort)

**Mandatory before showing to a Wise recruiter**
1. **Reposition the opportunity** (high impact, about half a session). Drop True Cost as "a new feature for Wise". Candidate directions grounded in the dataset:
   - (a) **small-amount competitiveness**: where Wise's fee loses to zero-fee MTOs at USD 200, analysed with RPW Wise quotes (A1 + H2);
   - (b) **cash-pickup and mobile-wallet corridors** where digital options are thin (F9, H3/H4) as a network-expansion case;
   - (c) keep transparency only as a **policy / B2B "Wise Platform" angle**, i.e. banks embedding Wise-style disclosure.
2. **Add the Wise-in-RPW analysis** (A1) (high impact, low effort).
3. **Fix the F4 framing** (A2) and **soften F1** with a pair-level panel and a survivorship note (A3) (high impact, low effort).
4. **Redefine the North Star and experiment** with explicit assumed baseline, MDE and N (M1, M2) (medium effort).
5. **Fix the prototype's misleading parts**: the markup model (W2), benchmark currency (U1), the £12,500 suggestion (U3), and input mutation (U4) (low effort).
6. **Cut the story** to a 2-page case study and a 6-slide deck that leads with the user and the Wise-specific insight (D1).

**Should do**
7. Gather public customer evidence and run 5–8 real sender conversations (P1).
8. Run the transparency sensitivity (A5) and apply one consistent negative-value rule (A6, A4).
9. Add within-corridor controls for F5/F8 (A8) and fix the chart stacking (A7).
10. Merge or close PR #5 (D2).

---

## 11. Final judgment

1. **Is this genuinely a strong PM case study?** Not yet. It is a strong *data* case study with a weak *product* conclusion.
2. **Is the opportunity original enough for Wise?** No. True Cost is largely Wise's existing public product and mission.
3. **Product thinking or AI-assisted technical execution?** Mainly technical execution. The product reasoning is structured but chose the hypothesis that was easiest to prototype, did not check the target company's product, and did not use the target company's own data.
4. **What most improves credibility?** Analysing Wise's own position in RPW and building the opportunity from a gap Wise actually has, plus a small amount of real customer evidence.
5. **Keep, reposition, or replace True Cost?** **Replace it as the headline**, or reposition it as a supporting element. The best candidate is small-amount pricing competitiveness in remittance corridors (H2 informed by A1), with transparency as context rather than the product.

Artifacts: independent scripts in `~/audit_work/indep/` (`load_raw.py`, `analyse.py`, `results.json`); browser recording and screenshots from the testing agent.
