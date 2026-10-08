# End-to-End Work Log — From Audited Dataset to Product Case Study

This log records what was done in the end-to-end phase (merged as PR #4): how each step was done, what it produced, which decisions were taken and why, which problems came up and how they were handled, and how to reproduce the results. The findings and product arguments themselves are in the linked documents; this file does not repeat them in full.

## 1. Scope and constraints followed

The brief was to turn the audited Phase 3 / 3.5 foundation into a complete, evidence-driven PM case study. These constraints applied throughout:

- **Raw data untouched.** `data/raw/rpw_dataset_2011_2025_q3.xlsx` was never written to. Every build verifies its SHA-256 (`f1d7265b1856d61812c158d3d03fae686dbff58735deabe016a6bfe23482d2a8`) before and after processing, and a test checks it again.
- **No silent data changes.** No row was deleted and no value was "corrected". Anomalies are kept and marked with boolean flags; raw columns are kept next to every derived column.
- **Undisclosed FX costs are never treated as zero.** Quotes whose FX margin is not disclosed are excluded from cost comparisons and counted separately.
- **No fabricated evidence.** RPW is a survey of provider price quotes. It has no transaction volumes, market shares or customer behaviour, so every statement about customer needs or product impact is labelled as a hypothesis.
- **Independence.** All outputs, including the prototype, state that the project is not affiliated with Wise or the World Bank and is not a production system.
- **Repo isolation.** Only this repository was touched; `codechecker` was not.
- **No merge without approval.** All work went to one branch and one PR; the user merged it.

## 2. What was done, step by step

### Step 1 — Apply the Phase 3.5 audit corrections
- **Files:** `docs/data_dictionary.md`, `docs/schema_comparison.md`, `docs/dataset_quality_report.md` (commit `0d440a0`).
- **Corrections applied (M1–M4 and the key minor findings):**
  - **M1 — FX-rate units.** `ccX lcu fx rate` and `inter lcu bank fx` are quoted in an unrecorded payout currency (often USD); their direction varies by period and `1` can be a placeholder. Only margin % and total cost % are treated as comparable.
  - **M2 — Not-collected fields.** PRE `sending location = Not available` (2011 Q3–2013 Q2) and PRE `pick-up method` blanks (2011–2013) are documented as non-collection, not as categories.
  - **M3 — Transparency coding.** The meaning of `transparent` shifts around 2021: `no` disappears, and some `yes` rows carry "not transparent" notes.
  - **M4 — Grain.** "One row = one service" is restated as a hypothesis. `period + id` is the only technical key, and duplicate counts now distinguish duplicate-group rows (266 PRE / 372 POST) from surplus rows (133 / 189).
  - **Minor items.** `..` readings downgraded to observations; `Lower income` vs `Low income`; non-ISO currency codes; dates outside their quarter; PRE quotes with different currency codes; fees omitted from total cost.

### Step 2 — Build a reproducible data pipeline
- **Code:** `src/rpw/` (commit `0b00aeb`), documented in `docs/pipeline.md`.

| Module | Role |
|---|---|
| `config.py` | Paths, raw hash, expected row counts, column mappings, numeric fields, provider aliases |
| `load.py` | Hash check; reads each data sheet with `dtype=object, keep_default_na=False` so `N/A` and `..` survive as text; caches to `data/interim/` (git-ignored) |
| `harmonise.py` | Renames to snake_case, stacks PRE and POST, converts types, adds normalised categories next to raw values |
| `providers.py` | Conservative provider-name normalisation |
| `flags.py` | Record-level and quote-level quality flags; converts wide → long |
| `build.py` | Runs everything, writes outputs and a manifest, asserts row counts |

- **Harmonisation decisions:**
  - Fields that exist in only one schema keep a `_pre` / `_post` suffix and are **not** merged (e.g. `product`, `payment instrument`, `sending location` vs `access point`, the two coverage fields, the pickup fields).
  - `note1` and `Standard Note` stay separate because their equivalence is unproven.
  - Text-stored numbers (2024 Q3–Q4) are parsed; values that can't be parsed would become NaN and be counted (none occur).
  - Dates are parsed from both `dd/Mon/yyyy` text and Excel datetimes (2025).
  - `Lower income` → `Low income` is applied but flagged as inferred.
  - `corridor_key = source_code + destination_code`; the 95 POST rows where the raw `corridor` differs (Kosovo `KSV`/`XKX`) are flagged.
- **Provider normalisation:** whitespace and case are folded, plus two explicit aliases (`Transferwise` → `Wise`, a documented rebrand; `Taptap Send` → `TapTap Send`). No fuzzy matching, so different legal entities are never merged. Raw names are kept in `firm_raw`; the mapping is exported to `provider_name_map.csv` (894 canonical providers).
- **Quality flags:** 27 boolean flags, each traced to a Phase 3 / 3.5 finding (full table in `docs/pipeline.md`). Key counts:

| Flag | PRE | POST |
|---|---|---|
| FX margin not disclosed (`transparent = no`) | 4,057 records | 3,361 records |
| PRE access channel not collected | 16,559 | – |
| PRE pickup method not collected | 9,388 | – |
| Numbers stored as text | – | 13,291 |
| Corridor code mismatch (KSV/XKX) | – | 95 |
| Duplicate except `id` (group rows / surplus rows) | 266 / 133 | 372 / 189 |
| Collection date outside its quarter | 6 | 181 |
| Cost identity fails by > 0.01 pp (quotes) | 388 | 138 |
| Non-zero fee left out of total (quotes) | 47 | 12 |
| Negative FX margin (quotes) | 3,609 | 18,298 |
| Negative total cost (quotes) | 398 | 3,282 |
| Total cost > 50% (quotes) | 11 | 347 |

- **Analysis populations (defined by flags, nothing removed):**
  - `cost_analysis_eligible`: total cost present, standard denomination, not a duplicate surplus copy, and the cost identity `total ≈ fee / amount × 100 + margin` holds within 0.01 pp.
  - `complete_cost_eligible = cost_analysis_eligible & fx_margin_disclosed`: the default population for cost comparisons. It covers about 90.6% of PRE quotes and 97.8% of POST quotes.
- **Outputs (`data/processed/`):**
  - `rpw_records_wide.parquet`: 253,960 records × 84 columns (USD 200 and USD 500 quotes side by side);
  - `rpw_quotes_long.parquet`: 507,920 quotes × 94 columns (one row per record × amount);
  - `provider_name_map.csv`, `data_quality_flag_summary.csv`;
  - `manifest.json`: raw hash, row/column counts, Python and pandas versions.
- **Invariants asserted on every build:** raw hash unchanged; 49,491 + 204,469 = 253,960 records in and out; long dataset is exactly 2 × wide.

### Step 3 — Exploratory analysis
- **Code and outputs:** `src/rpw/analysis.py`, `notebooks/02_exploratory_analysis.ipynb`, `docs/eda_findings.md`, 6 charts in `outputs/charts/`, 11 CSV tables and `eda_key_figures.json` in `outputs/tables/eda/` (commit `6369e21`).
- **Method decisions:**
  - Unit of analysis is the quote; the default population is `complete_cost_eligible`, USD 200 (`cc1`) unless the amount comparison needs USD 500.
  - All statistics are **unweighted** survey statistics, so they are not the World Bank's published volume-weighted Global Average.
  - Trends are shown twice: on all quotes, and on a **fixed panel** of 1,679 corridor × provider pairs present in both 2016 Q2 and 2025 Q3, to control for changes in which corridors and providers are surveyed.
  - "Latest window" = the last four surveyed quarters (2024 Q3, 2024 Q4, 2025 Q1, 2025 Q3; 2025 Q2 is absent from the file).
  - Corridor dispersion uses the 10th percentile, not the raw minimum, and negative-total quotes are excluded from "cheapest" measures (344 quotes) but kept in the data.
  - FX-rate levels are never compared.
- **Findings F1–F9** (headline values; denominators and caveats are in `docs/eda_findings.md`):
  - **F1 Trend:** USD 200 median 6.00% (2016 Q2) → 4.13% (2025 Q3); fixed panel 6.50% → 4.33%. Still above the 3% SDG target.
  - **F2 Dispersion:** 348 corridors in the latest window; median of corridor medians 4.50%; 43.4% of corridor medians exceed 5% and 15.5% are ≤ 3%, yet 87.6% of corridors have at least one surveyed quote ≤ 3%. Median gap between a corridor's median and its 10th percentile: 2.22 pp.
  - **F3 Amount:** across 26,245 paired records, median total cost is 4.50% at USD 200 vs 3.13% at USD 500; USD 500 is cheaper in 86.4% of pairs. FX margin is almost identical (2.03% vs 2.02%), so the gap comes from fixed fees.
  - **F4 Composition:** FX margin is about 31% of the mean total cost and exceeds the fee in 33.5% of quotes; 9.4% of quotes have no fee but still carry a mean FX margin of 1.85%.
  - **F5 Provider type:** latest medians — mobile operator 2.66%, MTO 4.24%, mixed 5.06%, post office 7.14%, bank 9.65% (non-bank FI has only 12 quotes and is not interpreted).
  - **F6 Access channel:** of 326 corridors with both digital and physical quotes, digital is cheaper in 81%, median gap 1.89 pp. This is an association, confounded by provider and payout method.
  - **F7 Transparency:** undisclosed FX margin affects 8.2% of PRE and 1.8% of POST records; the 2021 coding change is shown as a data limitation.
  - **F8 Markets:** latest receiving-region medians range from 3.45% (South Asia) to 5.74% (Sub-Saharan Africa).
  - **F9 Underserved screen:** 43 of 348 corridors have no surveyed non-negative quote ≤ 3%, 12 have none ≤ 5%, and 19 have no digital quote. Labelled as a screen, not a verdict.

### Step 4 — Product opportunity assessment
- **File:** `docs/product_opportunity.md` (commit `9eec969`).
- **Demonstrated problems** (from the data): price dispersion within corridors; a large, less visible FX-margin share; fixed fees penalising small transfers; some corridors lacking low-cost or digital options.
- **Four competing hypotheses**, compared on user problem, evidence strength, impact, international-payments fit, feasibility, regulation/compliance and risks:
  - **H1 — All-in cost clarity** with a corridor benchmark;
  - **H2 — Small-transfer pricing** (plans/bundles for frequent small senders);
  - **H3 — Underserved-corridor entry**;
  - **H4 — Digital switching** for cash/agent senders.
- **Choice: H1.** It has the broadest and strongest evidence, is feasible as an MVP (fee and rate are known at quote time), and is a precondition for H2 and H4. H2 depends on an unobservable sending-frequency segment; H3 is a network/licensing decision; H4 rests on a confounded association.
- **Still hypotheses:** that senders misjudge total cost, that they value a benchmark, and that clearer pricing changes completion, trust or retention.

### Step 5 — Product requirements (PRD)
- **File:** `docs/prd.md`.
- **Contents:** problem statement; persona (explicitly a hypothesis, not research); jobs to be done; proposed "True Cost" quote breakdown; core journey; MVP scope; explicit exclusions; alternatives considered; key assumptions; risks and trade-offs.

### Step 6 — Measurement and validation plan
- **File:** `docs/measurement_plan.md`.
- **North Star:** informed completions — share of quotes where the sender sees the all-in cost and completes the transfer.
- **Also defined:** supporting KPIs, guardrails (revenue per transfer, latency, abandonment, complaints, accessibility), adoption funnel, a stratified user-level A/B test in 3–5 corridors with ship / iterate / stop decision rules, what RPW can and cannot measure (and the telemetry needed instead), and customer-discovery next steps.
- **Sample size is not computed**, because the baseline completion rate is not public; the method for computing it is given.

### Step 7 — Interactive prototype
- **Code:** `prototype/` — React 18 + Vite 5 + TypeScript 5, tests with Vitest (commit `6c74eb4`).
- **Main journey:** choose corridor and amount (validated USD 20–5,000) → loading → quote breakdown (fee, FX margin vs mid-market rate, total cost in both currencies, amount received) → FX explainer → corridor survey benchmark (10th percentile / median / 90th percentile) → larger-amount comparison → review → simulated expired quote → demo confirmation.
- **Data:** corridor benchmarks are **real** RPW latest-window statistics for six corridors (GBR→NGA, GBR→IND, GBR→KEN, USA→MEX, USA→PHL, DEU→TUR), exported by `src/rpw/prototype_data.py` to `prototype/src/data/benchmarks.json`. Fees and exchange rates are **illustrative** and labelled as such.
- **Accessibility and layout:** labelled inputs, `aria-live` updates, `aria-invalid` / `aria-describedby` on errors, `aria-expanded` on the explainer, visible keyboard focus, responsive layout.
- **Labelling:** a permanent banner says the app is an independent, non-production demo, not affiliated with Wise or the World Bank.
- **Screenshots:** `outputs/prototype/desktop.png`, `outputs/prototype/mobile.png`.

### Step 8 — Case study and presentation
- **Files:** `docs/case_study.md` (end-to-end narrative: context, data foundation, findings, opportunity choice, proposal, prototype, measurement, limitations and next steps) and `docs/presentation.md` (Marp slide deck) (commit `cf01b77`).
- **README:** rewritten with the deliverables table, setup and reproduction commands, key limitations and the disclaimer.

### Step 9 — QA
- **Python tests (16, `pytest`):**
  - `test_units.py`: numeric parsing, date parsing, provider normalisation, category groupings;
  - `test_processed.py`: raw workbook unchanged, no rows dropped, manifest matches, periods and types, transparency flags, undisclosed FX never treated as complete, duplicates flagged not removed, cost identity on eligible quotes, raw values preserved;
  - `test_reported_stats.py`: every figure quoted in the findings, opportunity, PRD, case study and presentation matches the generated `eda_key_figures.json`.
- **Prototype:** 4 Vitest tests (fee + FX cost reconciles with the amount received; percentage cost falls with amount when a fee is fixed; every corridor has pricing and ordered percentiles; quote position within the survey range). `tsc` type-check and `vite build` pass.
- **Lint:** `ruff` clean on `src/` and `tests/`.
- **Reproducibility:** re-running `rpw.analysis` reproduces byte-identical tables, figures and charts.
- **Visual check:** headless Chrome screenshots at desktop and mobile widths.

## 3. Problems found during the work and how they were handled

| Problem | Handling |
|---|---|
| Corridors appeared twice in the underserved screen because country/region labels vary across periods (e.g. `FRADZA`, `SAUSYR`, `ISRMAR`) | Group by `corridor_key` only; carry one representative label. Result: 348 unique corridors |
| Raw minimum cost was negative in some corridors, making "cheapest quote" meaningless | Use the 10th percentile for dispersion; exclude negative totals from "cheapest" measures and report how many (344) |
| The non-bank FI provider type has only 12 quotes with extreme values, distorting a mean-based chart | Chart uses medians; text warns about small groups |
| Prototype breakdown rows overflowed horizontally on mobile | Breakdown rows now wrap (`flex-wrap`); mobile screenshot re-checked |
| Node and npm were not on PATH | Used the existing nvm install (Node 20) |
| `pyarrow` and `pytest` were missing from the venv | Installed and pinned in `requirements.txt` |
| Python Playwright not available for screenshots | Used the installed headless Chrome directly |

## 4. What was deliberately not done

- No row deletion, imputation or value correction in the processed data.
- No volume weighting: no corridor flow data is in the repo (KNOMAD bilateral remittance estimates would be the next addition).
- No comparison of FX-rate levels across periods or corridors.
- No causal claims (e.g. "digital causes lower prices").
- No claims about customer behaviour, market share or product impact as facts.
- No live prices, real accounts, payments or competitor scraping in the prototype.
- No browser-driven click-through test of the prototype (checked with unit tests, build and screenshots).

## 5. Known limitations (carried into the case study)

- RPW is a quarterly price survey of selected corridors and providers; sample composition changes over time.
- All statistics are unweighted, so they differ from the World Bank's official averages.
- The meaning of `transparent` changes around 2021.
- Payout currency is unrecorded, so FX-rate direction is unreliable.
- Negative and extreme costs are flagged, not explained.
- Persona, needs and impact are hypotheses that need customer discovery and an experiment.

## 6. How to reproduce

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

PYTHONPATH=src python -m rpw.build            # raw workbook -> data/processed/ (~2 min)
PYTHONPATH=src python -m rpw.analysis         # EDA tables + charts
PYTHONPATH=src python -m rpw.prototype_data   # survey benchmarks for the prototype
python -m pytest -q                           # 16 tests

cd prototype && npm ci && npm test && npm run build   # Node 20
npm run dev                                           # open the prototype locally
```
