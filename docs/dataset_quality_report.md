# Dataset Quality Report — Phase 3 (Dataset Understanding)

> **Phase 3.5 corrections applied.** This document was revised after the independent audit (`docs/phase3_audit_report.md`, `docs/data_dictionary_audit.md`). Corrected statements are tagged **[3.5-Mx]** / **[3.5-mx]** with the audit finding ID.

Generated from `notebooks/01_dataset_understanding.ipynb`. Supporting tables are in `outputs/tables/`.

This is **structural profiling only**. The counts describe the workbook, not the remittance market. No data was cleaned, merged or corrected. The raw workbook's SHA-256 (`f1d7265b…a2d8`) is verified before and after every notebook run.

## 1. Workbook structure

| Sheet | Declared range | Content | Notes |
|---|---|---|---|
| Terms of Use | `B28:B31` | Terms text in a **drawing text box**; the cells hold only 4 "REFERENCES" link labels | Hyperlinks are legacy `go.worldbank.org` short links |
| Methodology | `A1` (empty) | All text in a drawing text box | Describes how World Bank **averages** are computed (Global Average at USD 200, non-transparent RSPs excluded, Russia/former-Soviet RSPs excluded from the simple average, weighted average using KNOMAD flows, MTO Index, SmaRT link). **It defines no row-level equations.** |
| Legend | `A1:B36` | Excel table: field → definition, plus the Q2 2016 change list | Uses a generic `cc(X)` prefix |
| Countries | `A1:I217` | 215 countries: ISO3, name, region, income group, lending category, G8/G20 | Row 1 is a title/blank row; the header is row 2. Uses `..` heavily. |
| Dataset (up to Q1 2016) | `A1:AO49492` | 49,491 rows × 41 columns | Clean rectangular range |
| Dataset (from Q2 2016) | `A1:BV204470` | 204,469 rows; 42 headed + 5 unlabeled populated columns | See §3 |

pandas cannot see the drawing text (Terms of Use, Methodology). The notebook extracts it from `xl/drawings/*.xml`.

## 2. Structural profile

| Metric | PRE (≤ 2016_1Q) | POST (≥ 2016_2Q) |
|---|---:|---:|
| Data rows | 49,491 | 204,469 |
| Columns read by pandas | 41 | 47 |
| Meaningful (headed, populated) columns | 41 | 42 |
| Period range | 2011_1Q – 2016_1Q | 2016_2Q – 2025_3Q |
| Periods present | 17 | 37 |
| Unique sending countries (`source_code`) | 35 | 49 |
| Unique receiving countries (`destination_code`) | 105 | 105 |
| Unique `corridor` values | 310 | 372 |
| Unique source–destination code pairs | 310 | 368 |
| Unique providers (`firm`, raw strings) | 637 | 713 |
| Unique `firm_type` labels | 10 | 11 |
| Unique service descriptors | `product` 37 labels | `payment instrument` 26, `access point` 22, `pickup method` 10 |
| Unique `id` | 49,486 | 204,469 |
| Full-row duplicates | 0 | 0 |
| Duplicates ignoring `id` | 133 | 189 |

- **Quarters with no rows:** 2011_2Q, 2011_4Q, 2012_2Q, 2012_4Q (semi-annual collection early on) and **2025_2Q**. Rows per period: `outputs/tables/rows_per_period.csv`.
- **Corridor count vs code pairs:** POST has 372 corridor strings but 368 code pairs. The 4 extra strings are the `…XKX` Kosovo variants.
- **Per-column missingness, dtype, min/max and top values:** `outputs/tables/column_profile.csv`.

Missingness above 1%:

| Sheet | Column | Blank rows | % |
|---|---|---:|---:|
| PRE | `note1` | 31,495 | 63.6 |
| PRE | `note2` | 43,768 | 88.4 |
| PRE | `pick-up method` | 9,388 | 19.0 |
| POST | `Standard Note` | 155,892 | 76.2 |
| POST | `note2` | 204,181 | 99.9 |
| POST | `pickup location` | 115,614 | 56.5 |

- All cost fields are ≤ 0.6% blank. The `cc2` block is blank more often than `cc1` (POST 1,072 vs 22 rows).
- Numeric ranges, computed on parsed copies:

| Field | PRE range | POST range |
|---|---|---|
| `cc1 total cost %` | −8.97 to 75.0 | −58.92 to 307.2 |
| `cc1 fx margin` | −16.58 to 36.05 | −67.48 to 59.98 |
| `inter lcu bank fx` | — | min **0** (1 row) |

## 3. Post-2016 sheet: empty columns, unlabeled columns, formulas

Source: `outputs/tables/post2016_xml_column_scan.csv`, from a streaming read of the worksheet XML.

**Populated vs empty columns**

- The declared range extends to column **BV (74 columns)**.
- Only **A–AU (47 columns)** hold values.
- BM, BR, BS, BT, BU and BV each contain one styled cell with no value. All other letters AV–BV have no cells at all.
- The extended dimension is therefore **formatting-only**.

**Unlabeled columns AQ–AU**

- Populated in exactly the 6,470 rows of **2025_3Q**, blank elsewhere.
- Deterministic helper strings:

| Column | Value |
|---|---|
| AQ | `2025` |
| AR | `source_code`+`2025` |
| AS | `destination_code`+`2025` |
| AT | `source_code`+`2026` |
| AU | `destination_code`+`2026` |

- No header and no Legend entry. They add no information.

**Formula cells** (6,690 in total)

| Column | Field | Formula cells | Formula | External? | Periods |
|---|---|---:|---|:-:|---|
| J | `destination_name` | 37 | `=VLOOKUP(I…,[1]Countries!A$3:F$217,2,FALSE)` | yes | 2023_1Q (Kosovo rows) |
| K | `destination_region` | 2 | `=VLOOKUP(I…,[1]Countries!A$3:F$217,3,FALSE)` | yes | 2023_1Q |
| AP | `corridor` | 6,651 | `=C…&I…` (shared formula) | no | 2024_4Q |

- **External link.** `[1]` resolves to `xl/externalLinks/externalLink1.xml`. It points to a file on the original author's machine: `/Users/schen/Documents/WeChat Files/…/rpw_dataset_2011_2023_q1_with formula.xlsx`. That workbook lists the six sheets present here **plus** `Countriesold`, `CountriesQ320`, `CountriesQ321`, `CountriesQ322` and `HistoricalCountryCat`, which are not in this file **[3.5-m11]**. The link part also contains a cached copy of the linked Countries table.
- **Cached values.** All 6,690 formula cells have a cached `<v>` value.
- **pandas/openpyxl read the cached values reliably.** The value pandas loads equals the cached XML value for **6,690 / 6,690** cells.
- **Cached values are consistent with the formulas' inputs:**
  - AP cached corridor = `source_code + destination_code` in 100% of formula rows;
  - the J/K cached values (`Kosovo`, `Europe & Central Asia` for `KSV`) match this workbook's Countries sheet.
- **Reproducibility.**
  - Reading the file is reproducible: the cached values are fixed in the file, and Python never recalculates them.
  - Excel/LibreOffice may prompt to update links. If recalculated, J/K would break (`#REF!`), because the source file is unavailable.
  - **Do not open and re-save the raw file in Excel.** Treat the cached values as the data of record.
  - The formulas were not modified.

## 4. Value-type inconsistencies

Full list: `outputs/tables/mixed_value_types.csv`.

| Where | Issue |
|---|---|
| POST 2024_3Q and 2024_4Q (13,284–13,291 rows) | `id`, all `ccX lcu amount / denomination amount / lcu fee / lcu fx rate / fx margin / total cost %` and `inter lcu bank fx` are stored as **text** (e.g. `"200.00"`). They all parse as numbers (0 unparseable values). |
| POST 2020_2Q | 1 `id` stored as text |
| POST 2025_1Q, 2025_3Q | `date` stored as Excel datetime; earlier periods use the text format `dd/Mon/yyyy` |
| POST 2025_1Q, 2025_3Q | `transparent` = `Yes` (capitalised), 13,117 rows |
| Both | int/float mixing in numeric columns (harmless) |

## 5. Placeholder values and label variants

Full counts: `outputs/tables/placeholder_counts.csv` and `label_variants.csv`.

**`..` token**

| Field | PRE rows | POST rows | Co-occurs with | Proposed eventual treatment |
|---|---:|---:|---|---|
| `source_region` | 45,452 | 178,796 | high-income senders | category "not classified" (not NaN) |
| `destination_region` | 1,656 | 3,872 | HRV, KOR, POL, EST, LVA, LTU, ANT (high income) | same |
| `source_lending` / `destination_lending` | 42,712 / 784 | 175,978 / 3,136 | high-income countries; also PSE, CUB (POST) | category "no lending category" |
| `source_G8G20` / `destination_G8G20` | 13,748 / 39,216 | 71,450 / 164,393 | non-members | category "not G8/G20" |
| `destination_income` | 121 | 0 | ANT (Netherlands Antilles) only | missing |

- The workbook does not define `..`. These readings are **inferred** from co-occurrence and from the Countries sheet, where `..` fills the same columns. **[3.5-m1]** The region/lending readings are overstated: GNQ, CUB, PRK, PSE and ANT are counterexamples. Treat `..` as "not provided by the source".
- Proposal: keep `..` as an explicit category in classification fields, never silently drop it, and convert it to missing only where no category makes sense (ANT income).

**Other placeholders and variants**

- PRE literal `N/A` in `product` (214), `speed actual` (10) and `coverage` (2). **Default `pandas.read_excel` turns these into NaN.** The notebook uses `keep_default_na=False`.
- PRE `sending location` = `Not available` in 16,559 rows (33%). It is not clear whether this means "not recorded" or "no physical sending location".
- Empty cells and empty-string cells are indistinguishable after loading. Both are treated as blank.
- Case/whitespace variants:
  - `transparent` Yes/yes;
  - `speed actual` Less than one hour/less than one hour, Next Day/Next day;
  - `receiving network coverage` Low/low;
  - `payment instrument` Credit Card/Credit card;
  - `firm_type` Post Office/Post office;
  - several `pick-up method` / `pickup location` labels;
  - ~15 `firm` names differing only by case or trailing space (e.g. `Azimo`/`azimo`, `TapTap Send`/`Taptap Send`).
- Country renames within POST: CZE, TUR, MKD, SWZ.
- Kosovo code mismatch: `destination_code = KSV` while `corridor = …XKX` in 95 rows (2021_4Q, 2023_1Q).

## 6. Cost-field validation

Tables: `outputs/tables/cost_relationship_checks.csv` and `transparency_margin_checks.csv`.

**What the workbook documents**

- The Legend defines the fields but gives no equations:
  - `fee` in LCU;
  - `lcu fx rate` = the RSP's applied rate;
  - `inter lcu bank fx` = the interbank rate;
  - `fx margin` = the percentage difference between the applied and interbank rates;
  - `total cost %` = the total cost of the transaction in percent.
- The Methodology sheet defines only aggregate averages. They use the USD 200 amount (`cc1`) and exclude non-transparent RSPs.
- The external methodology page was **not** used to add equations here.

**Relationships tested.** The expected forms below are *inferred* from the Legend wording. Differences are absolute values in percentage points (pp).

| Sheet | Amount | Relationship | Testable rows | ≤0.01 pp | ≤0.1 pp | ≤1 pp | >1 pp | Max diff |
|---|---|---|---:|---:|---:|---:|---:|---:|
| PRE | cc1 | total ≈ fee/lcu amount×100 + margin | 49,381 | 99.57% | 99.58% | 99.80% | 100 | 26.5 |
| PRE | cc2 | same | 49,178 | 99.64% | 99.66% | 99.94% | 30 | 12.1 |
| POST | cc1 | same | 204,445 | 99.96% | 99.98% | 99.99% | 29 | 23.3 |
| POST | cc2 | same | 203,396 | 99.97% | 99.98% | 99.99% | 25 | 7.1 |
| PRE | cc1 | margin ≈ (1 − fx rate / interbank)×100 | 49,490 | 96.02% | 97.93% | 99.91% | 43 | 95.9 |
| PRE | cc2 | same | 49,191 | 95.99% | 97.91% | 99.91% | 45 | 6,787 |
| POST | cc1 | same | 204,446 | 94.83% | 97.81% | 99.79% | 426 | 370,470 |
| POST | cc2 | same | 203,395 | 95.16% | 98.04% | 99.84% | 326 | 370,470 |

**Observed**

- **Total cost** is, to rounding, **fee as % of the send amount plus FX margin** in ≥99.6% of rows.
- **FX margin** matches `(1 − applied/interbank)` in ~95–96% of rows at 0.01 pp and ~98% at 0.1 pp. So margin is expressed with the interbank rate as the base, and a positive margin means the sender receives less than at the interbank rate.
- **Exceptions are kept, not corrected:**
  - PRE: 103 `cc2` rows where `cc2 lcu amount` = 0, so the ratio is undefined (e.g. 2014_3Q RUSARM).
  - POST: one row with `inter lcu bank fx` = 0 (2018_4Q CHLPER MoneyGram), which creates the huge max differences.
  - Rows where the margin is stored as 0 although the rates differ (e.g. 2011_1Q SGPPHL).
  - Duplicated-margin blocks where `cc2` fields appear to repeat `cc1` values, e.g. 2013_2Q AUSPHL: the cc2 margin 9.62 does not follow from the rates.
  - Examples are printed in notebook §11.
- **cc1 vs cc2.** Same currency in ≥99.9% of rows. The applied fx rate is identical in 96–97% of rows. The LCU amounts are rounded equivalents of USD 200/500, so the ratio is exactly 2.5 in only ~56–60% of rows. Totals differ mainly through the fee share (a fixed fee weighs less at USD 500).
- **Negative values.**
  - Negative margin: PRE 1,801 (cc1); POST 9,169 (cc1).
  - Negative total cost: PRE 127; POST 1,308 (cc1). Every negative-total row also has a negative margin.
  - The note text explains some: "A negative exchange rate margin for this operator may be due to a promotion/special offer…". This is the only explanation the workbook gives.

**Transparency and zero FX margin**

| Sheet | transparent | Rows | cc1 margin = 0 | fx rate = interbank | fx rate = 1 | Note says "not transparent" |
|---|---|---:|---:|---:|---:|---:|
| PRE | no | 4,057 | 4,036 (99.5%) | 4,037 | 4,033 | 3,962 |
| PRE | yes | 45,434 | 8,866 (19.5%) | 8,507 | 6,782 | 6 |
| POST | no | 3,361 | 3,351 (99.7%) | 3,352 | 3,352 | 3,315 |
| POST | yes/Yes | 201,108 | 25,885 (12.9%) | 25,261 | 21,169 | 282 |

- For `transparent = no`, the FX margin is almost always 0, with both rates set to 1 (placeholder rates). The standard note on these rows says: *"The 0% in the exchange rate margin does NOT necessarily mean that there is no exchange rate cost, but rather that this cost is not disclosed to the sender at the time of sending."* So **the zero is not a measured zero**. For these rows, `total cost %` covers **the fee only** and understates the full cost. **[3.5-M3]** The same disclaimer also appears on 1,011 PRE `transparent = yes` rows, and 21 PRE / 10 POST `no` rows have non-zero margins, so the rule holds in most rows but not all. The Methodology sheet confirms that the World Bank excludes such RSPs from its averages.
- Many `transparent = yes` rows also have margin 0 with rate 1. **Inferred [3.5-m14]**: 1,621 PRE / 11,395 POST such rows have no note supporting this. Some are same-currency services, e.g. notes "USD service" or "This RSP sends and pays out in EUR…", where no conversion happens at send time. The notes warn that recipients "may incur an additional cost (not shown here)".
- 282 POST `yes` rows carry a "not transparent"-type note; 272 of them fall in 2021_3Q–2022_1Q, as `no` fades out (133 → 0). Only 11% have margin 0. **[3.5-M3]** This is evidence that the flag's operational meaning shifted around 2021. Kept as recorded and flagged in Phase 4.
- **No `transparent = no` rows exist after 2021_4Q**, but zero margins continue. The workbook does not say whether non-transparent services stopped being collected, stopped being flagged, or were removed. **Unclear.**

## 7. Unit of observation

> **[3.5-M4]** Restated: one row = one survey record (`period + id`) with USD 200/500 quotes for a firm × corridor. "One row = one service" is a working hypothesis. The 133/189 figures are **surplus** duplicate rows (duplicate groups: 266 PRE / 372 POST rows).

One row = one service (firm × corridor × service configuration) observed in one period, with USD 200 (`cc1`) and USD 500 (`cc2`) quotes in wide form.

- `period + id` is the only unique key in both sheets.
- No descriptive key is unique.
- `id` is not persistent across periods.

Details are in `data_dictionary.md` §1 and `outputs/tables/candidate_key_tests.csv`.

## 8. Can the two sheets be combined?

**Partially, and only with explicit assumptions.**

- Stacking the common core (period, countries, corridor, firm, speed, cost fields, transparency, notes) is technically straightforward, and the core cost definitions look the same (§6 relationships hold equally in both sheets).
- Service-attribute fields are **not** directly comparable across 2016:
  - `product` dropped;
  - `payment instrument` new;
  - `sending location` → `access point` with a new vocabulary;
  - `coverage` → `receiving network coverage` with a new scale;
  - pick-up split into two fields.
- Classification fields changed vintage (income group labels, regions).
- Coverage also changes: sending countries go from 35 to 49, corridors from 310 to 372, firms from 637 to 713 (440 in both). The panel is unbalanced, so any cross-period aggregate mixes composition change with price change.

**Proposed Phase 4 harmonization strategy (not executed)**

1. **Keep raw untouched.** Build `data/processed/` outputs from a scripted loader (`keep_default_na=False`, `dtype=object`) with the hash check.
2. **Per-sheet typed tables first.** Parse text numbers and dates. Normalise case and whitespace in categorical labels. Keep the original raw columns next to the normalised ones.
3. **Stack the common core** into one long table with `schema_version = pre/post`. Keep sheet-specific attributes (`product`; `payment instrument`, `pickup location`, the two coverage fields) as separate nullable columns. Do not force-map them.
4. **Reshape cost fields to long format** (`amount_usd ∈ {200, 500}`) as an optional derived view, keeping the wide original.
5. **Flag, don't fix:**
   - `transparent_norm`;
   - `fx_margin_disclosed = transparent == yes`;
   - `fx_margin_is_placeholder_zero` (non-transparent and margin 0);
   - `total_cost_fee_only` (non-transparent);
   - negative-margin and negative-total flags;
   - relationship-check residual flags;
   - zero-denominator flags;
   - duplicate-except-id flags.
6. **Country fields:**
   - use codes as keys;
   - resolve `KSV`/`XKX` with a documented rule;
   - take names and classifications from one chosen reference (the workbook's Countries sheet, updated 2025) *and* keep the as-recorded values;
   - keep `..` as explicit categories.
7. **Provider names:** a documented alias table (case/whitespace first, then known renames such as Transferwise→Wise). Do not merge ambiguous names.
8. **Mappings requiring judgement** (access point, pick-up, income labels) go in versioned CSV mapping files with rationale, and are reviewed before use.
9. **Drop only** the undocumented helper columns AQ–AU, after recording that they are derivable.

## 9. Issues that could materially affect later analysis

1. **Non-transparent rows:** FX margin 0 means "not disclosed", so total cost understates. There are no such flags after 2021_4Q.
2. **2016 schema break** in service attributes; the coverage scale changed.
3. **Unbalanced panel:** corridors, firms and senders enter and exit; 2025_2Q and four early quarters are missing.
4. **No persistent service id:** longitudinal service tracking requires an approximate key.
5. **Type drift** in 2024_3Q–4Q (text numbers) and 2025 (datetime dates, `Yes`). This is silent if loaded naively.
6. **pandas default NA handling** hides literal `N/A`.
7. **Classification vintage drift** (income/region labels) and the undefined `..`.
8. **Provider-name inconsistencies.**
9. **Extreme values** (total cost up to 307%, margins to −67%) and a few impossible denominators (0 interbank rate, 0 cc2 amount).
10. **Duplicate-except-id rows** (133 / 189).
