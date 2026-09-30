# Data Dictionary — Remittance Prices Worldwide (RPW) workbook

Scope: the two historical data sheets in `data/raw/rpw_dataset_2011_2025_q3.xlsx`:

- **PRE** = `Dataset (up to Q1 2016)` — 49,491 rows, periods `2011_1Q`–`2016_1Q`.
- **POST** = `Dataset (from Q2 2016)` — 204,469 rows, periods `2016_2Q`–`2025_3Q`.

Sources, in order of authority:

1. the workbook `Legend` sheet (quoted as *Legend: "…"*);
2. the `Methodology` and `Terms of Use` sheets (their text is in drawing text boxes, not cells);
3. the `Countries` sheet;
4. observed values, produced by `notebooks/01_dataset_understanding.ipynb` (tables in `outputs/tables/`).

Labels used in this document:

- **Observed** marks something measured in the file.
- **Inferred** marks a reading of the data that the workbook does not state.
- **Unclear** means the workbook does not give enough information to define the field.

The external methodology page (https://remittanceprices.worldbank.org/en/methodology) is referenced by the workbook but was not used to add definitions here.

Observed dtypes are the Python value types returned by `pandas.read_excel(..., dtype=object, keep_default_na=False)` (openpyxl cached values). For the full per-column profile see `outputs/tables/column_profile.csv`.

---

## 1. Natural unit of observation

**One row = one surveyed remittance service offered by one provider (`firm`) in one sending→receiving country corridor, in one survey period.** Each row holds price quotes for **two** transfer amounts, side by side:

- the `cc1` columns for USD 200;
- the `cc2` columns for USD 500.

In conceptual terms:

```
row  ≈  period × source country × destination country × firm × service configuration
        (pre: product / sending location / speed / pick-up / coverage;
         post: payment instrument / access point / pickup method / pickup location / speed / receiving network coverage)
        with two amount scenarios (USD 200, USD 500) stored in wide form
```

**Evidence**

- *Legend:* `id` is the "id number applied to each service". The `cc(X) …` fields are the "surveyed amount sent", fee, rate, margin and total cost for amount X.
- Every row has both a `cc1` and a `cc2` block. POST `cc1 denomination amount` is 200 in 100% of rows and `cc2` is 500 in 100%. PRE is 200/500 in >99.8% of rows, plus a few odd values (201, 202, 6; 501, 502) and 80/78 blanks.
- `cc1 lcu code == cc2 lcu code` in 100% (POST) and 99.9% (PRE) of rows. The two blocks describe the same sending currency.

**Candidate-key tests** (`outputs/tables/candidate_key_tests.csv`; "dup rows" = rows that share a key with at least one other row)

| Sheet | Key tested | Distinct keys | Dup rows | Unique? |
|---|---|---:|---:|:--:|
| PRE | `id` | 49,486 | 10 | no |
| PRE | `period + id` | 49,491 | 0 | **yes** |
| PRE | `period + source_code + destination_code + firm` | 34,386 | 25,225 | no |
| PRE | … + `product` | 43,836 | 10,634 | no |
| PRE | … + `product + sending location + speed actual` | 47,011 | 4,591 | no |
| PRE | … + `pick-up method + coverage` | 47,304 | 4,016 | no |
| PRE | … + `cc1 lcu fee + cc1 total cost %` | 49,296 | 390 | no |
| PRE | all columns except `id` | 49,358 | 266 | no |
| POST | `id` | 204,469 | 0 | **yes** |
| POST | `period + source_code + destination_code + firm` | 111,555 | 139,945 | no |
| POST | … + `payment instrument` | 162,191 | 76,661 | no |
| POST | … + `access point` | 173,461 | 57,700 | no |
| POST | … + `pickup method` | 196,316 | 15,598 | no |
| POST | … + `speed actual` | 198,086 | 12,341 | no |
| POST | … + `pickup location + receiving network coverage` | 198,344 | 11,859 | no |
| POST | … + `cc1 lcu fee + cc1 total cost %` | 204,184 | 563 | no |
| POST | all columns except `id` | 204,280 | 372 | no |

**Conclusions**

- `id` is a **row identifier**, not a stable service identifier:
  - it never repeats across the two sheets;
  - no POST id appears in more than one row, so it does not follow a service from quarter to quarter;
  - in PRE, 5 ids are reused (10 rows), each time in different periods and for unrelated firms/corridors, e.g. id 44140 = `2014_4Q ZAFZWE Standard Bank` and `2015_1Q AREEGY Al Fardan Exchange`.
- `period + id` is unique in both sheets. It is the safest technical row key.
- **No combination of descriptive fields is unique.** Even all columns except `id` leave 133 (PRE) / 189 (POST) rows that exactly duplicate another row. The workbook does not record whatever distinguishes these services, or they are duplicate records. **Unclear** which.
- Tracking "the same service" over time would therefore need an **assumption-based key**, e.g. `corridor + firm + service attributes`. It would be approximate.

---

## 2. Field reference

Column legend:

- **Pre/Post** — does the column exist in PRE / POST (✓ / –).
- **Comparable across 2016?**
  - **Yes** — same name and definition.
  - **With care** — same concept, but label sets, types or classification vintages differ.
  - **No** — not present in both, or the definition changed.

### 2.1 Identifiers and time

| Original column | Conceptual name | Meaning | Observed type | Units | Pre | Post | Missing / placeholders | Caveats | Comparable across 2016? |
|---|---|---|---|---|:-:|:-:|---|---|---|
| `id` | row_id | *Legend:* "id number applied to each service" | PRE int; POST int, plus str in 13,288 rows (2020_2Q ×1, 2024_3Q, 2024_4Q) | – | ✓ | ✓ | none | Not unique in PRE (5 ids reused). Not persistent across periods. Numbering schemes differ (PRE 1–59,392; POST 3,240,001–1,220,195,xxx). | No (identifier only) |
| `period` | survey_period | *Legend:* "data collection period". Format `YYYY_nQ`. | str | quarter | ✓ | ✓ | none | Not every quarter was surveyed. Missing: 2011_2Q, 2011_4Q, 2012_2Q, 2012_4Q (PRE was semi-annual in 2011–2012) and **2025_2Q**. | Yes (format identical) |
| `date` | collection_date | *Legend:* "day when the information was collected" | str `dd/Mon/yyyy`; POST 2025_1Q and 2025_3Q are Excel datetimes (13,117 rows) | date | ✓ | ✓ | none | Many dates per period. Mixed storage type in 2025. | Yes, after parsing |

### 2.2 Countries and corridor

`source_*` and `destination_*` share the same sub-fields (*Legend:* `source` = "country where money is sent from", `destination` = "country where money is sent to").

| Original column | Conceptual name | Meaning | Observed type | Pre | Post | Missing / placeholders | Caveats | Comparable across 2016? |
|---|---|---|---|:-:|:-:|---|---|---|
| `source_code` / `destination_code` | sending_country_iso3 / receiving_country_iso3 | ISO 3166-1 alpha-3 code | str | ✓ | ✓ | none | Kosovo is `KSV` (not ISO) in `destination_code`, while `corridor` uses `XKX` in 2021_4Q and 2023_1Q. All codes exist in the Countries sheet. PRE: 35 sending / 105 receiving. POST: 49 / 105. | Yes |
| `source_name` / `destination_name` | sending_country_name / receiving_country_name | country name | str | ✓ | ✓ | none | Names change within POST: CZE Czech Republic→Czechia, TUR Turkey→Türkiye, MKD Macedonia, FYR→North Macedonia, SWZ Swaziland→Eswatini. 37 POST cells are cached results of external VLOOKUP formulas (see quality report). | With care: join on code, not name |
| `*_region` | region | *Legend:* "country's World Bank region" | str | ✓ | ✓ | `..` in many rows (see below) | Label set changes: POST adds "Middle East, North Africa, Afghanistan & Pakistan" next to "Middle East & North Africa". Appears to be the classification in force when the row was recorded (**inferred**). | With care |
| `*_income` | income_group | *Legend:* "country's income group" | str | ✓ | ✓ | PRE `..` for ANT (121 rows) | PRE labels "High income: OECD", "High income: nonOECD"; POST "High income". POST also has "Lower income" (1,490 rows), a label not in the Countries sheet. | No, not directly (label sets differ) |
| `*_lending` | lending_category | *Legend:* "country's lending category" (IBRD / IDA / Blend) | str | ✓ | ✓ | `..` | `..` mostly for high-income countries (**inferred**: no lending category). | With care |
| `*_G8G20` | g8_g20_membership | *Legend:* "country's membership of G8 and/or G20 group" | str | ✓ | ✓ | `..` = not a member (**inferred** from the Countries sheet, where 196/215 countries have `..`) | Values `G8/G20`, `G20`, `..` | Yes |
| `corridor` | corridor_code | sending ISO3 + receiving ISO3, e.g. `USAMEX` (**observed**: equals `source_code+destination_code` in 100% PRE rows) | str | ✓ | ✓ | none | Not in the Legend. POST: 95 rows where `corridor` uses `XKX` but `destination_code` is `KSV`. 6,651 POST cells (2024_4Q) are cached formula results `=C&I`. PRE 310 corridors, POST 372. | Yes (after fixing the Kosovo code) |

### 2.3 Provider and service attributes

| Original column | Conceptual name | Meaning | Observed type | Pre | Post | Missing / placeholders | Caveats | Comparable across 2016? |
|---|---|---|---|:-:|:-:|---|---|---|
| `firm` | provider | *Legend:* "remittance service provider offering the service" (RSP) | str | ✓ | ✓ | none | Spelling/case/trailing-space variants (e.g. `Azimo`/`azimo`, `TapTap Send`/`Taptap Send`, trailing spaces). Renames are recorded only in notes (e.g. note2 "Transferwise has changed its name to 'Wise'"). PRE 637 names, POST 713, 440 in both. | With care (entity resolution needed) |
| `firm_type` | provider_type | *Legend:* "type of remittance service provider" | str | ✓ | ✓ | none | 10 (PRE) / 11 (POST) labels, including combined types ("Bank / Money Transfer Operator") and case variants ("Post Office"/"Post office"). 4 PRE / 43 POST firms have more than one type. | With care |
| `product` | product_type (**pre only**) | *Legend:* "type(s) of product offered", e.g. `Cash to cash`, `Account to account`, `Online service` | str | ✓ | – | literal `N/A` in 214 rows | 37 labels, some comma-combined. *Legend:* "dropped" as of Q2 2016. | No |
| `sending location` | sending_location / access_point (**pre**) | *Legend:* "type of location where the service is available" (e.g. `at Branch`, `On-line`, `Call Center`) | str | ✓ | – | `Not available` in 16,559 rows (33%) | *Legend:* renamed "access point" from Q2 2016. Label vocabulary differs. | No, not directly (needs a mapping) |
| `access point` | access_point (**post**) | Same concept as `sending location` (Legend rename), e.g. `Internet`, `Agent`, `Bank branch` | str | – | ✓ | none | 22 labels, comma-combined. No `Not available` category. | No, not directly |
| `payment instrument` | payment_instrument (**post only**) | *Legend:* "NEW: instrument used by the sender to pay for the transaction", e.g. `Cash`, `Bank account transfer`, `Debit card`, `Credit Card` | str | – | ✓ | none | 26 labels, comma-combined, case variants (`Credit Card`/`Credit card`). | No (no pre equivalent) |
| `speed actual` | transfer_speed | *Legend:* "time it takes for the money to be available for the receiver" | str (ordered categories) | ✓ | ✓ | PRE literal `N/A` 10 rows | Categories: Less than one hour, Same day, Next day, 2 days, 3-5 days, 6 days or more. POST has case variants and one `1-3 days`. | Yes, after case normalisation |
| `coverage` | receiving_network_coverage (**pre**) | *Legend:* "ranks the extensiveness of the network in the receiving country" | str | ✓ | – | 18 blank, 2 `N/A` | Labels are geographic: `Nationwide`, `Major cities`, `Main city`, `Urban only`, `Rural only`. | No: different scale from post |
| `receiving network coverage` | receiving_network_coverage (**post**) | Legend rename of `coverage` | str | – | ✓ | none | Labels are ordinal: `High`, `Medium`, `Low` (+ `low`). **The scale changed** and no mapping is documented. | No |
| *(Legend only)* `sending network coverage` | sending_network_coverage | *Legend:* "NEW: ranks the extensiveness of the network of the firm in the sending country" | – | – | **absent** | – | The Legend lists it as new from Q2 2016, but no such column exists in POST. See `schema_comparison.md`. | n/a |
| `pick-up method` | pickup_method (**pre**) | *Legend (`pickup method`):* "indicates how the money can be picked up in the receiving country" | str | ✓ | – | blank 9,388 rows (19%) | 31 labels mixing channel and location (`Cash`, `Bank Account`, `Home Delivery`, `ATM Network`, `Mobile`), with case variants. | With care |
| `pickup method` | pickup_method (**post**) | same Legend text | str | – | ✓ | none | Labels: `Cash`, `Bank account`, `Mobile wallet`, … | With care (label mapping needed) |
| `pickup location` | pickup_location (**post only**) | **Unclear.** Not in the Legend. Values look like where cash is collected (`Agent`, `Bank branch`, `Home delivery`, `ATM network`). | str | – | ✓ | blank 115,614 rows (57%) | Undocumented column. Some pre `pick-up method` labels (Home Delivery, ATM Network) appear here instead of in post `pickup method`. | No |

### 2.4 Cost fields (per amount `cc1` / `cc2`)

**What `cc1` and `cc2` are.** The Legend defines each cost field generically as `cc(X) …`, where X is one of the two **surveyed send amounts**:

- **`cc1` = the USD 200 scenario** (`cc1 denomination amount` = 200);
- **`cc2` = the USD 500 scenario** (`cc2 denomination amount` = 500).

In each case the amount is converted into the sending country's local currency (`cc(X) lcu amount`, often rounded to a convenient local amount). The fee, applied exchange rate, FX margin and total cost are recorded separately for each amount. The Methodology sheet's World Bank averages (Global Average, SmaRT, etc.) use **USD 200**, i.e. `cc1`. The workbook does not say what "cc" abbreviates (**unclear**).

| Original column (X = 1, 2) | Conceptual name | Meaning (Legend) | Observed type | Units | Pre | Post | Missing | Caveats | Comparable across 2016? |
|---|---|---|---|---|:-:|:-:|---|---|---|
| `ccX denomination amount` | send_amount_usd | "surveyed amount sent in USD" | int/float; POST str in 2024_3Q–4Q (`"200.00"`) | USD | ✓ | ✓ | PRE 80 / 78 blank | PRE has a few non-standard values (cc1: 201 ×3, 202 ×1, 6 ×1; cc2: 501 ×9, 502 ×3). | Yes |
| `ccX lcu amount` | send_amount_lcu | "surveyed amount sent in local currency of the sending country" | int/float; POST str in 2024_3Q–4Q | sending LCU | ✓ | ✓ | PRE cc1 103 blank; PRE `cc2 lcu amount` = 0 in 103 rows (2014_3Q RUSARM etc.) | Rounded LCU equivalents, so the cc2/cc1 ratio is exactly 2.5 in only ~56–60% of rows. | Yes |
| `ccX lcu code` | send_currency | "local currency of the sending country" (ISO 4217) | str | – | ✓ | ✓ | PRE 1 / 4 blank | Sometimes USD/EUR where the service is sent in a non-local currency (see notes). | Yes |
| `ccX lcu fee` | fee_lcu | "fee in local currency" | int/float; POST str in 2024_3Q–4Q | sending LCU | ✓ | ✓ | PRE 6 / 208; POST 22 / 1,072 blank | Fixed and percentage fees are not separated. | Yes |
| `ccX lcu fx rate` | applied_fx_rate | "foreign currency exchange rate applied to the transaction by the RSP" | float/int; POST str in 2024_3Q–4Q | receiving currency per 1 sending LCU (**inferred** from values, e.g. USA→PHL ≈ 41.65) | ✓ | ✓ | PRE cc2 294; POST 22 / 1,072 | Equals 1 or the interbank rate for most non-transparent rows (see quality report). | Yes |
| `inter lcu bank fx` | interbank_fx_rate | "interbank exchange rate" (one per row, shared by cc1/cc2) | float/int; POST str in 2024_3Q–4Q | same as above | ✓ | ✓ | none | One POST row has 0 (2018_4Q CHLPER MoneyGram). | Yes |
| `ccX fx margin` | fx_margin_pct | "percentage difference between the FX rate applied by the RSP and the interbank exchange rate" | float/int; POST str in 2024_3Q–4Q | percent (e.g. 2.07 = 2.07%) | ✓ | ✓ | PRE 1 / 186; POST 18 / 1,071 | Negative values exist (promotions, per note text). **0 does not mean zero cost for non-transparent RSPs** (note text). | Yes, with the transparency caveat |
| `ccX total cost %` | total_cost_pct | "total cost of the transaction in percentage" | float/int; POST str in 2024_3Q–4Q | percent of send amount | ✓ | ✓ | PRE 0 / 187; POST 18 / 1,072 | Observed ≈ fee / lcu amount × 100 + fx margin (99.6–99.97% of rows within 0.01 pp). Negative and >100% values exist (POST max 307.2). | Yes, with the transparency caveat |

### 2.5 Transparency and notes

| Original column | Conceptual name | Meaning | Observed type | Pre | Post | Missing | Caveats | Comparable across 2016? |
|---|---|---|---|:-:|:-:|---|---|---|
| `transparent` | fx_rate_disclosed | *Legend:* "if yes, indicates that the RSP provided the researcher with the exchange rate applied to the transaction; if no, … not provided" | str: PRE `yes`/`no`; POST `yes`/`Yes`/`no` (`Yes` = all 13,117 rows of 2025_1Q and 2025_3Q) | ✓ | ✓ | none | `no` occurs only up to 2021_4Q (PRE 4,057 rows, POST 3,361). No `no` rows after 2021_4Q; the file does not explain why. *Methodology:* non-transparent RSPs are excluded from the Global Average. | Yes, after case normalisation |
| `note1` (PRE) / `Standard Note` (POST) | standard_note | *Legend (`standard note`):* "provides additional information on the service" | free text (117 / 184 distinct) | ✓ | ✓ | PRE 64% blank; POST 76% blank | Header renamed. Semi-standardised sentences, e.g. the non-transparency disclaimer, "LCU service", "USD service", "Account required for detailed price info", promotion explanations of negative margins, EUR/USD pay-out warnings. Carries meaning that is not in structured fields. | Yes (same role), as text |
| `note2` | standard_note_2 | *Legend (`standard note 2`):* "provides additional information on the service" | free text | ✓ | ✓ | PRE 88% blank; POST 99.9% blank | e.g. "Transferwise has changed its name to 'Wise'", corridor-level currency notes, "SEPA service". | Yes, as text |

### 2.6 Post-only unlabeled columns

| Column (pandas name / Excel letter) | Content | Rows populated | Status |
|---|---|---|---|
| `Unnamed: 42` / AQ | constant `2025` | 6,470 (2025_3Q only) | helper column, undocumented |
| `Unnamed: 43` / AR | `source_code + "2025"` | 6,470 | helper column |
| `Unnamed: 44` / AS | `destination_code + "2025"` | 6,470 | helper column |
| `Unnamed: 45` / AT | `source_code + "2026"` | 6,470 | helper column |
| `Unnamed: 46` / AU | `destination_code + "2026"` | 6,470 | helper column |

They carry no information beyond existing fields and are not survey variables (**inferred**). Columns AV–BV hold no values.

---

## 3. Missing-value conventions (summary)

| Convention | Where | Proposed reading (not applied yet) |
|---|---|---|
| empty cell / empty string | cost fields (small counts), notes, `pick-up method`, `pickup location`, `coverage` | missing / not recorded |
| `..` | `*_region`, `*_income` (PRE only, ANT), `*_lending`, `*_G8G20` | for G8G20: "not a member" (a category). For region/lending: "not classified" (a category, mainly high-income countries). For income (ANT): missing. **Inferred**: the workbook does not define `..`. |
| literal `N/A` | PRE `product` (214), `speed actual` (10), `coverage` (2) | not available / missing. Default pandas settings silently turn these into NaN. |
| `Not available` | PRE `sending location` (16,559) | an explicit category in the source; keep it distinct from blank until its meaning is confirmed (**unclear**) |
| `0` in `ccX fx margin` with `transparent = no` | both sheets | **not** a measured zero: FX cost was not disclosed (note text). Treat as unknown for cost comparisons. |

## 4. Most important fields for later analysis

- **Grain:** `period`, `source_code`, `destination_code` / `corridor`, `firm`, and the service attributes.
- **Cost measures:** `cc1 total cost %` (the World Bank headline basis, USD 200) and `cc2 total cost %`, with their components `ccX lcu fee` and `ccX fx margin`.
- **Validity flag:** `transparent`, which governs whether the FX margin and total cost are complete.
- **Provider/service context:** `firm_type` and `speed actual` (both sheets); post-only `payment instrument`, `access point`, `pickup method`.
