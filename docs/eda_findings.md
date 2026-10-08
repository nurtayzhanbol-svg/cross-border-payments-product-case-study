# Exploratory Analysis — Findings

Reproduce with `PYTHONPATH=src .venv/bin/python -m rpw.analysis`, or run `notebooks/02_exploratory_analysis.ipynb`. Every number below is in `outputs/tables/eda/eda_key_figures.json` or in the CSVs next to it.

## How to read these numbers

- **Unit:** one surveyed price quote. These are not transactions, and the dataset has no volumes or market shares. All averages are **unweighted** across quotes. They are not the World Bank's published Global Average, which uses a different population and weighting.
- **Population:** `complete_cost_eligible` USD 200 quotes, i.e. quotes with a disclosed FX margin, a standard denomination, no duplicate surplus copy and a valid cost identity. That is 245,469 of 253,960 USD 200 quotes.
  - Quotes whose FX margin is undisclosed are **excluded**, not treated as zero. Their totals are fee-only.
  - **Latest window** = 2024_3Q, 2024_4Q, 2025_1Q, 2025_3Q (2025_2Q was not surveyed).
- **Sample composition:** corridors and providers enter and leave the survey. Trends are therefore also shown on a fixed panel.
- All statements are **descriptive**. None of them establishes a cause.

## Findings

**F1 — Costs have fallen, but the typical quote is still above the 3% SDG target.**
- USD 200 quotes:
  - the mean fell from 8.76% (2011_1Q) to 7.44% (2016_2Q) and 6.36% (2025_3Q);
  - the median fell from 6.00% (2016_2Q) to 4.13% (2025_3Q).
- On a fixed panel of 1,679 corridor × provider pairs present in both 2016_2Q and 2025_3Q, the median fell from 6.50% to 4.33%. So the decline is not only a change in sample mix.
- The cost fields have the same definition across the 2016 schema change. Even so, the survey's coverage changed then.
- Chart: `outputs/charts/01_cost_trend_cc1.png`.

**F2 — Prices vary widely within the same corridor.**
- Latest window, 348 corridors:
  - the median of corridor medians is 4.50%;
  - 43.4% of corridors have a median quote above 5%;
  - only 15.5% have a median at or below 3%;
  - but in 87.6% of corridors at least one surveyed non-negative quote is at or below 3%.
- The gap between the median quote and the 10th-percentile quote in a corridor has a median of 2.22 pp, and is ≥2 pp in 57.5% of corridors.
- *Interpretation (hypothesis):* a sender who uses a typical provider pays noticeably more than one who uses a low-cost provider *in the same corridor*.
- **Limitation:** the data cannot show whether senders know about the cheaper options or can use them (e.g. KYC, payout reach, speed, or trust).
- Charts: `02_corridor_cost_distribution.png`, `06_corridor_dispersion.png`.

**F3 — Small transfers are penalised by fixed fees.**
- Comparing the same record at both amounts (26,245 records in the latest window):
  - the median total is 4.50% at USD 200 and 3.13% at USD 500;
  - the mean fee falls from 4.42% to 2.21% of the amount;
  - the mean FX margin barely changes (2.03% vs 2.02%);
  - the USD 500 quote is cheaper in percentage terms in 86.4% of records.

**F4 — The FX margin is a material, less visible part of cost.**
- Latest window: the mean fee is 4.41% and the mean FX margin is 2.02%. The FX margin is about 31% of the mean total.
- The FX margin exceeds the fee in 33.5% of quotes.
- 9.4% of quotes charge no fee. Their median total is 1.50% (vs 4.86% for fee-bearing quotes), and their mean FX margin is 1.85%. So "no fee" does not mean "no cost".
- The workbook's own notes warn that a 0% margin may mean the FX cost was not disclosed.
- Chart: `03_fee_vs_fx_composition.png`.

**F5 — Provider types differ.**
- Median USD 200 totals, latest window:
  - money transfer operators: 4.24% (21,807 quotes);
  - banks: 9.65% (3,882 quotes), driven by fees (median fee 6.67%);
  - mobile operators: 2.66%, but only 92 quotes;
  - post offices: 7.14% (85 quotes).
- Groups with fewer than ~100 quotes are too small to generalise.

**F6 — Digital access is associated with lower prices.**
- Latest window medians: digital-only access 4.05% vs physical-only 5.88%.
- Within the same corridor (326 corridors with both), the digital-only median is lower in 81.0% of corridors; the median gap is 1.89 pp.
- *Not causal:* the gap is confounded by provider and payout method. The channel field is an assumption-bearing mapping (`docs/pipeline.md`).

**F7 — Transparency coding limits FX-cost analysis.**
- FX margin is undisclosed in 8.2% of PRE records and 1.8% of POST records.
- The `transparent = no` flag disappears after 2021, while notes still describe non-transparent services (audit M3).
- Before 2021 and after 2022, the share of quotes with fully known costs is therefore not measured the same way.
- Chart: `04_transparency_coding.png`.

**F8 — Markets.**
- Latest window, receiving regions:
  - Sub-Saharan Africa has the highest median (5.74%);
  - South Asia has the lowest named-region median (3.45%).
  - Both old and new MENA labels appear, because the classification changed (audit m1).
- Sending markets (46): Tanzania, Türkiye and Senegal have the highest medians; Côte d'Ivoire, Kuwait and Costa Rica the lowest.
- Chart: `05_receiving_region_costs.png`.

**F9 — Underserved-corridor screen (a screen, not a verdict).**
- In 43 of 348 surveyed corridors, no non-negative quote is at or below 3%. In 12, none is at or below 5%: e.g. TURBGR, ISRMAR, SAUSYR, GBRGMB, USAAFG, ZAFAGO, TZARWA, DOMHTI, GBRAFG, AGONAM.
- 19 corridors have no surveyed digital quote.
- 344 negative-total quotes (promotions or quote-orientation artefacts, audit M1) are excluded from the "cheapest" measure.
- Table: `underserved_corridor_screen_latest_window_cc1.csv`.

## What the data cannot tell us

- How much money flows through each provider or corridor, or which provider customers actually choose.
- Whether senders compare prices, understand FX margins, or would switch providers.
- The received amount in the recipient's currency. FX rate levels are unreliable (audit M1), so only margin percentages are used.
- Service quality, reliability, KYC friction, or the cost of cash-out at the recipient end.
