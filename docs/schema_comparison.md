# Schema Comparison — `Dataset (up to Q1 2016)` vs `Dataset (from Q2 2016)`

> **Phase 3.5 corrections applied.** This document was revised after the independent audit (`docs/phase3_audit_report.md`, `docs/data_dictionary_audit.md`). Corrected statements are tagged **[3.5-Mx]** / **[3.5-mx]** with the audit finding ID.

This document records the discrepancies between the two sheets. It does not resolve any of them.

- **PRE** = `Dataset (up to Q1 2016)`: 41 headed columns (A–AO).
- **POST** = `Dataset (from Q2 2016)`: 42 headed columns (A–AP), plus 5 unlabeled columns (AQ–AU). Declared range `A1:BV204470`.
- Machine-readable header comparison: `outputs/tables/schema_header_comparison.csv`.

The Legend lists these changes "as of Q2 2016":

| Legend item | Legend text |
|---|---|
| `product` | dropped |
| `sending location` | renamed "access point" |
| `coverage` | renamed "receiving network coverage" |
| `payment instrument` | NEW: instrument used by the sender to pay for the transaction |
| `sending network coverage` | NEW: ranks the extensiveness of the network of the firm in the sending country |

## 1. Columns present in both, with the same name (36)

| Group | Columns |
|---|---|
| Identifiers and time | `id`, `period`, `date` |
| Sending country | `source_code`, `source_name`, `source_region`, `source_income`, `source_lending`, `source_G8G20` |
| Receiving country | `destination_code`, `destination_name`, `destination_region`, `destination_income`, `destination_lending`, `destination_G8G20` |
| Provider | `firm`, `firm_type` |
| Service | `speed actual` |
| Cost, USD 200 (`cc1`) | `cc1 lcu amount`, `cc1 denomination amount`, `cc1 lcu code`, `cc1 lcu fee`, `cc1 lcu fx rate`, `cc1 fx margin`, `cc1 total cost %` |
| Cost, USD 500 (`cc2`) | `cc2 lcu amount`, `cc2 denomination amount`, `cc2 lcu code`, `cc2 lcu fee`, `cc2 lcu fx rate`, `cc2 fx margin`, `cc2 total cost %` |
| Other | `inter lcu bank fx`, `transparent`, `note2`, `corridor` |

Same name does not guarantee same content. See section 5.

## 2. Columns only in PRE (5)

| Column | Legend status | Post counterpart |
|---|---|---|
| `product` | "dropped" | none |
| `sending location` | renamed to `access point` | `access point` |
| `coverage` | renamed to `receiving network coverage` | `receiving network coverage` |
| `note1` | not in Legend under this name (Legend has `standard note`) | `Standard Note` (**inferred**: same position and same kind of text) |
| `pick-up method` | Legend has `pickup method` | `pickup method` (hyphen dropped) |

## 3. Columns only in POST (6 headed + 5 unlabeled)

| Column | Legend status |
|---|---|
| `payment instrument` | NEW (documented) |
| `access point` | rename of `sending location` (documented) |
| `receiving network coverage` | rename of `coverage` (documented) |
| `Standard Note` | Legend `standard note`. Header differs from PRE `note1`. |
| `pickup method` | Legend `pickup method` |
| `pickup location` | **not in the Legend** (undocumented new column) |
| `Unnamed: 42`–`Unnamed: 46` (AQ–AU) | not documented. Helper keys, 2025_3Q only. |

## 4. Renamed or conceptually equivalent fields

| PRE | POST | Basis | Equivalent content? |
|---|---|---|---|
| `sending location` | `access point` | Legend rename | Concept yes, vocabulary no. PRE: `at Branch`, `On-line`, `Call Center`, `Not available`, `on mobile phone`. POST: `Agent`, `Internet`, `Bank branch`, `Post Office branch`, `Mobile phone`, … No mapping is documented. |
| `coverage` | `receiving network coverage` | Legend rename | Concept yes, **scale no**. PRE is geographic (`Nationwide`, `Major cities`, `Main city`, `Urban only`, `Rural only`). POST is ordinal (`High`, `Medium`, `Low`). No mapping is documented. |
| `note1` | `Standard Note` | Legend `standard note`; same position (column 36) | Yes, largely: the same standard sentences occur in both. |
| `pick-up method` | `pickup method` (+ `pickup location`) | Legend `pickup method` | Partly. PRE mixes channel and place (`Cash`, `Bank Account`, `Home Delivery`, `ATM Network`, `Mobile`). POST moves some place-type values into the new `pickup location`, and adds `Mobile wallet`. **[3.5-m10]** The overlap runs in both directions (`Agent` appears in `pickup location` on Bank-account and Mobile-wallet rows), so any mapping has to be many-to-many. PRE `pick-up method` was also not collected in 2011_1Q–2013_4Q **[3.5-M2]**. |

## 5. Potentially incompatible fields (same name, different content)

| Field | Difference |
|---|---|
| `*_income` | PRE uses `High income: OECD` / `High income: nonOECD`. POST uses `High income`, plus an undocumented `Lower income`. Classification vintages differ. |
| `*_region` | POST adds `Middle East, North Africa, Afghanistan & Pakistan` next to `Middle East & North Africa`. The classification appears to be the one in force when each row was recorded (**inferred**). |
| `source_name` / `destination_name` | Country renames inside POST (Czechia, Türkiye, North Macedonia, Eswatini). Codes are stable. |
| `transparent` | PRE `yes`/`no`. POST adds `Yes` (2025 periods). No `no` after 2021_4Q in POST. |
| `id` | Different numbering ranges. No overlap. Not persistent. |
| Numeric cost fields, `id`, `date` | POST stores some values as text (2024_3Q–4Q) or as datetimes (2025). Values are equivalent after parsing. |
| `firm`, `firm_type` | Same concept. Spelling and case variants, and provider renames (e.g. Transferwise → Wise), are only recorded in notes. |

## 6. Fields whose definitions changed

- `coverage` → `receiving network coverage`: the measurement scale changed (geographic reach → High/Medium/Low rank). The Legend describes both as "ranks the extensiveness of the network in the receiving country", but the categories are not the same.
- `sending location` → `access point`: renamed, and the category vocabulary was redesigned.
- `product` was dropped. Its information (e.g. "Cash to account") is split in POST across `payment instrument` (sender side) and `pickup method` (receiver side). **[3.5-m9]** `product` labels also encode channel and currency, so this split is not exhaustive. No 1:1 mapping exists.
- `sending location` → `access point`: the Legend calls this a rename, but PRE `Not available` reflects non-collection in 2011_3Q–2013_2Q **[3.5-M2]**. Mapping is valid only for 2013_3Q–2016_1Q.
- Pick-up: one PRE field became two POST fields (`pickup method`, `pickup location`). `pickup location` is undefined in the Legend.

## 7. Missing expected fields — `sending network coverage`

**Finding.** The Legend lists `sending network coverage` as "NEW" from Q2 2016 ("ranks the extensiveness of the network of the firm in the sending country"). No column in the POST sheet has that name:

- no header contains "sending network";
- the only coverage column is `receiving network coverage`.

**What was checked**

- All 47 pandas-read POST columns, and every column letter present in the worksheet XML (A–AU with data; BM, BR–BV hold only one empty formatted cell each).
- The five unlabeled columns (AQ–AU). They hold year-suffixed country codes, not coverage ranks.
- The only column with an undocumented header is `pickup location`. Its values (`Agent`, `Bank branch`, `Home delivery`, …) describe the **receiving** side and are not a rank. So it does not match the Legend definition of `sending network coverage`.

**Status: unresolved.** The field is documented but absent from this workbook. Possible explanations, none confirmed:

- it was never populated;
- it was removed before publication;
- the Legend is out of date.

Do not treat any existing column as a substitute.

Other Legend/sheet mismatches:

- `corridor` and `pickup location` exist in the data but not in the Legend.
- Legend `standard note` / `standard note 2` correspond to headers `note1`/`Standard Note` and `note2`.

## 8. Harmonization feasibility (input to Phase 4, not executed)

| Category | Fields |
|---|---|
| Harmonizable by direct stacking (after type/case parsing) | `period`, `date`, `source_code`, `destination_code`, `corridor` (Kosovo fix), `firm` (entity cleaning), `firm_type` (case), `speed actual` (case), all `cc1`/`cc2` cost fields, `inter lcu bank fx`, `transparent` (case), notes (`note1`↔`Standard Note`, `note2`) |
| Harmonizable only with an explicit, documented mapping (assumption-bearing) | `*_income` (e.g. both "High income: OECD/nonOECD" → "High income"), `*_region`, `pick-up method` ↔ `pickup method`/`pickup location`, `sending location` ↔ `access point` |
| Not harmonizable: keep sheet-specific | `product` (pre only), `payment instrument` (post only), `coverage` vs `receiving network coverage` (different scales), `pickup location` (post only, undocumented), `id` (not persistent) |
| Absent | `sending network coverage` |
