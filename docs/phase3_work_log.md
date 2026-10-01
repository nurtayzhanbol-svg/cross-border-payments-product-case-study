# Phase 3 Work Log — Dataset Understanding

This log records what was done in Phase 3 (merged as PR #1), how it was done, and which decisions were taken. The findings themselves are in the other documents; this file links to them and does not repeat them in full.

## 1. Scope and constraints followed

Phase 3 aimed to understand exactly what the World Bank RPW workbook contains. These constraints applied throughout:

- **Raw data untouched.** Nothing in `data/raw/` was modified. The notebook verifies the workbook's SHA-256 (`f1d7265b1856d61812c158d3d03fae686dbff58735deabe016a6bfe23482d2a8`) before and after every run.
- **No processing of the data.**
  - No cleaning, no correction of anomalies, no repair of formulas.
  - No merging of the two historical sheets, and no unified dataset.
- **No product work.** No product insights, hypotheses, recommendations, UI or business charts.
- **Repo isolation.** Only this repository was touched; `codechecker` was not.

## 2. What was done, step by step

### Step 1 — Licensing check (Restricted Data clause)
- **Workbook links.** Followed the workbook's Terms of Use links. The three legacy `go.worldbank.org` short links did not resolve from the work environment.
- **Official pages consulted instead:**
  - the RPW data-download page (terms summary);
  - the World Bank "Restricted Data" page, which is now legacy and holds no list. It says third-party conditions now appear in dataset metadata;
  - the World Bank Data Catalog entry for RPW, classified **Public**, with no third-party restriction shown.
- **Recorded.** Added the result, with its limits, to `docs/dataset_notes.md`. The conclusion is explicitly *not* a legal opinion.
- **Vintage mismatch noted.** The download page mentions data to Q1 2025, but the file contains data up to Q3 2025.

### Step 2 — Workbook package inspection (read-only)
- **Why read the XML.** An `.xlsx` file is a ZIP of XML parts. They were read directly with `zipfile` and `xml.etree.ElementTree`, because pandas cannot see:
  - text in drawing text boxes. **Terms of Use** and **Methodology** keep all their text in text boxes, so pandas returns empty or nearly empty sheets for them;
  - declared sheet dimensions;
  - formulas, cached values and external links.
- **Recorded for each sheet:** its XML part, size, declared range and relationships.
- **Workbook-level parts:** external link, calcChain, defined names.

### Step 3 — Legend and Countries sheets
- **Legend.** Exported as-is to `outputs/tables/legend_raw.csv`. It is the only in-workbook field dictionary, and it lists the Q2 2016 changes.
- **Countries.** Profiled the table, which has a title row first and the header in row 2. Counted the `..` placeholder in each classification column.

### Step 4 — Loading the two historical sheets
- **Load call.** `pd.read_excel(..., dtype=object, keep_default_na=False, na_values=[])`.
- **Why `dtype=object`.** It keeps each cell's raw Python type (str/int/float/datetime), so type drift within a column stays visible.
- **Why `keep_default_na=False`.** With default settings, pandas silently converts literal strings such as `N/A` into NaN. This was found during the work:
  - PRE `product`: 214 values;
  - PRE `speed actual`: 10 values;
  - PRE `coverage`: 2 values.
- **Blanks.** Only in memory, empty strings are treated as blank for profiling. Nothing is written back.

### Step 5 — Schema comparison
- **Method.** Compared headers by name and position between `Dataset (up to Q1 2016)` (PRE) and `Dataset (from Q2 2016)` (POST), and cross-checked them against the Legend's change list.
- **`sending network coverage`.** Investigated the field the Legend lists as new from Q2 2016. It does not exist in the data, and no column matches its definition. It is documented as unresolved.
- **Outputs:**
  - `docs/schema_comparison.md`;
  - `outputs/tables/schema_header_comparison.csv`.

### Step 6 — Post-2016 sheet structural scan
- **Method.** Streamed the 298 MB worksheet XML once and counted, per column letter:
  - cells;
  - non-empty values;
  - formula cells;
  - formula cells that have a cached value;
  - formulas that reference the external workbook.
- **Empty range.** The declared range runs to column BV, but values exist only in A–AU.
- **Unlabeled columns.** AQ–AU are undocumented helper keys, populated only in 2025_3Q.
- **Formulas.** 6,690 formula cells:
  - J: 37 external VLOOKUPs;
  - K: 2 external VLOOKUPs;
  - AP: 6,651 `=C&I` concatenations.
- **Cached values.** All formula cells have cached values. pandas returns exactly the cached value for 6,690 of 6,690 cells.
- **External link.** Documented the external link target, a workbook path on the original author's machine.
- **Output:** `outputs/tables/post2016_xml_column_scan.csv`.

### Step 7 — Type consistency, placeholders, label variants
- **Mixed types per column per period.** Examples:
  - text-stored numbers in 2024_3Q–4Q;
  - datetime dates and `Yes` in 2025.
  - Output: `mixed_value_types.csv`.
- **Placeholder counts.** `..`, blanks, `N/A`, `Not available`, etc.
  - Output: `placeholder_counts.csv`.
  - Also checked which countries carry `..`, and their income group.
- **Label variants.** Labels that differ only by case or whitespace.
  - Output: `label_variants.csv`.
- **Name and corridor consistency:**
  - country codes that map to more than one name;
  - mismatches between `corridor` and `source_code + destination_code` (the Kosovo `KSV`/`XKX` case).

### Step 8 — Structural profile
- **Per sheet:**
  - rows and meaningful columns;
  - period range and quarters with no rows;
  - unique countries, corridors, firms, ids and service descriptors;
  - duplicate counts.
- **Per column:**
  - missing values;
  - pandas dtype and Python types;
  - number of unique values;
  - numeric min/max/median, computed on parsed copies;
  - top values.
- **Outputs:**
  - `sheet_summary.csv`;
  - `column_profile.csv`;
  - `rows_per_period.csv`.

### Step 9 — Cost-field validation
- **What the workbook defines.** The Legend defines the cost fields but gives no equations. The Methodology sheet defines only aggregate averages.
- **Relationships tested.** Both are inferred from the Legend wording, and tested without correcting anything:
  - `total cost % ≈ fee / lcu amount × 100 + fx margin`;
  - `fx margin ≈ (1 − lcu fx rate / inter lcu bank fx) × 100`.
- **Exceptions.** Reported with examples. Zero denominators were counted separately; this was added after the first run produced `inf` differences.
- **Other checks:**
  - surveyed amounts: `cc1` = USD 200, `cc2` = USD 500;
  - consistency between the cc1 and cc2 fields;
  - negative margins and negative totals.
- **Transparency vs zero FX margin.** For `transparent = no`, the margin is 0 in more than 99% of rows. The workbook's own note says this zero is *not* a measured zero.
- **Outputs:**
  - `cost_relationship_checks.csv`;
  - `transparency_margin_checks.csv`.

### Step 10 — Unit of observation
- **Candidate keys tested.** Increasingly specific field combinations were tested per sheet.
- **Result:**
  - only `period + id` is unique;
  - no descriptive key is unique;
  - `id` does not persist across periods.
- **Conclusion.** One row = one firm's service in one corridor in one period, with USD 200 and USD 500 quotes side by side.
- **Output:** `candidate_key_tests.csv`.

### Step 11 — Harmonization feasibility (not executed)
- **Field classification.** Each field was classified as:
  - directly stackable;
  - mappable with documented assumptions;
  - not harmonizable;
  - absent.
- **Phase 4 strategy.** Proposed in `docs/dataset_quality_report.md` §8.

### Step 12 — Verification and delivery
- **Notebook run.** Executed end-to-end with `jupyter nbconvert --execute` (about 2 minutes) and validated with `nbformat`.
- **Raw-file check.** Confirmed the raw file hash is unchanged, and that `git status` shows no change under `data/raw/`.
- **PR.** Committed on a feature branch and opened PR #1. It has since been merged.

## 3. Files added or changed

| File | Status | Purpose |
|---|---|---|
| `notebooks/01_dataset_understanding.ipynb` | added | Reproducible, explained inspection of all six sheets; writes `outputs/tables/` |
| `docs/data_dictionary.md` | added | Every field in both sheets, `cc1`/`cc2`, missing-value conventions, unit of observation |
| `docs/schema_comparison.md` | added | PRE vs POST schema, renames, incompatibilities, `sending network coverage` |
| `docs/dataset_quality_report.md` | added | Structural profile, workbook issues, cost validation, placeholders, harmonization strategy |
| `docs/dataset_notes.md` | changed | Licensing / Restricted Data result appended |
| `README.md` | changed | Status set to Phase 3; reproduction command and documentation index added |
| `outputs/tables/*.csv` (12 files) | added | Machine-generated structural tables (see below) |

| Table | Content |
|---|---|
| `legend_raw.csv` | Legend sheet exported verbatim |
| `schema_header_comparison.csv` | Header presence and position in each sheet |
| `post2016_xml_column_scan.csv` | Per-column cell, formula and cached-value counts from the XML |
| `mixed_value_types.csv` | Columns with more than one Python value type, and the periods affected |
| `placeholder_counts.csv` | `..`, blank, `N/A` and similar counts per column |
| `label_variants.csv` | Category labels differing only by case or whitespace |
| `sheet_summary.csv` | Sheet-level structural metrics |
| `column_profile.csv` | Per-column missingness, types, unique values, min/max, top values |
| `rows_per_period.csv` | Row count per period per sheet |
| `cost_relationship_checks.csv` | Agreement rates for the fee/margin/total equations |
| `transparency_margin_checks.csv` | Transparency × zero margin × placeholder FX-rate counts |
| `candidate_key_tests.csv` | Uniqueness of candidate row keys |

## 4. Key decisions and why

| Decision | Reason |
|---|---|
| Read the XML directly in addition to pandas | Text boxes, formulas, external links and declared ranges are invisible to pandas |
| `keep_default_na=False` when loading | Default pandas settings silently erase literal `N/A` values |
| `dtype=object` when loading | To keep raw value types visible (text numbers, datetimes) |
| Numeric parsing only on in-memory copies | Profiling needs numbers; the source must stay unchanged |
| Treat cached formula values as the data of record | All are present and read exactly; recalculation would break (the external file is unavailable) |
| Do not open or re-save the raw file in Excel | It could trigger link updates and change the file |
| Keep `..` as a category in the proposed handling, not NaN | Its meaning is "not a member" or "not classified" in most fields (inferred from the Countries sheet) |
| Label inferences as **inferred** or **unclear** | The workbook does not define several things (`..`, `pickup location`, what "cc" abbreviates) |
| No merge in Phase 3 | Out of scope; several service fields are not comparable across 2016 |

## 5. Problems met during the work and how they were handled

| Problem | Handling |
|---|---|
| `go.worldbank.org` links unreachable | Used the official current World Bank pages instead and stated the limitation |
| World Bank API rate limiting (HTTP 429) | Relied on the rendered Data Catalog page |
| pandas hid literal `N/A` values | Switched to `keep_default_na=False` and documented it |
| `inf` differences in cost checks (zero denominators) | Excluded them from the agreement rates and counted them separately |
| `.str` accessor error on all-blank columns | Cast to `str` before string checks |

## 6. Not done in Phase 3 (by design)

- No cleaning, type conversion or label normalisation written to disk.
- No merged or unified dataset.
- No exploratory analysis, product findings or recommendations.
- No charts.

## 7. How to reproduce

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace notebooks/01_dataset_understanding.ipynb
sha256sum data/raw/rpw_dataset_2011_2025_q3.xlsx   # must equal the hash in section 1
```
