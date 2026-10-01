# Phase 3 Audit Report — Phase 3.5 (Dataset Documentation Audit)

**Scope.** This is an independent, adversarial re-check of the Phase 3 documentation against the raw workbook. The four documents checked are `docs/data_dictionary.md`, `docs/schema_comparison.md`, `docs/dataset_quality_report.md` and `docs/dataset_notes.md`. The aim was to falsify their claims, not to confirm them.

**Constraints followed**
- No Phase 4 work.
- No data cleaning or merging.
- No existing documentation edited.
- `data/raw/` untouched: SHA-256 `f1d7265b1856d61812c158d3d03fae686dbff58735deabe016a6bfe23482d2a8` verified before and after the audit.

The field-by-field audit is in `docs/data_dictionary_audit.md` (claims F01–F40). This report adds the non-field claims (R01–R50), the required topic audits, the manual row trace, and the severity classification.

## 0. Method

| Step | How |
|---|---|
| Independent read | All six sheets were read with `header=None, dtype=object, keep_default_na=False, na_values=[]`. No Phase 3 helper code, notebook or `outputs/tables` file was reused. |
| Independent XML parse | `zipfile` + `ElementTree` over the worksheet XML, the shared strings, `calcChain.xml`, `externalLinks/` and `workbook.xml`. This was used for formulas, cached values, the used range, merged cells, hidden rows/columns, and the raw values of the sampled rows. |
| Falsification checks | Cost identities, FX direction across 8+ corridors over time, transparency × notes × margins, candidate keys, period vs date, country labels vs the Countries sheet, provider variants, schema label vocabularies. |
| Not re-verified | The web sources behind the licensing conclusion in `dataset_notes.md`. This audit re-read only the workbook (see R13). |

The audit scripts were run ad hoc outside the repository and are not committed. Every number below can be reproduced from the workbook using the definitions stated.

## 1. Headline counts

| Result | Field claims (F) | Other claims (R) | **Total** |
|---|---:|---:|---:|
| CONFIRMED | 24 | 37 | **61** |
| PARTIALLY CONFIRMED | 13 | 11 | **24** |
| UNSUPPORTED | 0 | 0 | **0** |
| INCORRECT | 2 | 0 | **2** |
| UNCLEAR | 1 | 2 | **3** |
| **Claims checked** | 40 | 50 | **90** |

No finding is classified CRITICAL. The 2 INCORRECT claims and the period-structured missingness, transparency-coding and grain findings are MAJOR (§10).

## 2. Claim register (non-field claims)

| # | Phase 3 claim (source) | Evidence (this audit) | Result |
|---|---|---|---|
| R01 | PRE 49,491 × 41; POST 204,469 × 42 headed + 5 unlabeled (DQR §1–2) | Reproduced | CONFIRMED |
| R02 | POST declared range `A1:BV204470`; values only in A–AU; BM, BR–BV hold one styled empty cell each (DQR §3) | The `<dimension>` is `A1:BV204470`; the column scan agrees | CONFIRMED |
| R03 | Data sheets are clean rectangular ranges (DQR §1) | No `mergeCell` and no `hidden="1"` in either data sheet. **Not mentioned in Phase 3:** merged cells exist in Legend (`A1:B1`, `A31:B31`) and Countries (`A1:E1`, the title row). They are harmless, but undocumented. | CONFIRMED |
| R04 | 6,690 formula cells: J 37, K 2, AP 6,651 (DQR §3) | XML: J 37, K 2, AP 6,651 (AP as shared formulas). PRE: 0. `calcChain` lists the same 6,690 cells. | CONFIRMED |
| R05 | J/K are external VLOOKUPs in 2023_1Q (Kosovo); AP is `=C&I` in 2024_4Q | J: 37 rows, K: 2 rows, all KSV, 2023_1Q. AP: 6,651 rows, all 2024_4Q. | CONFIRMED |
| R06 | All formula cells have cached values, and pandas reads 6,690/6,690 equal to the cache | 6,690 `<v>` present; pandas value = cached XML value 6,690/6,690 | CONFIRMED |
| R07 | Cached values match reconstruction from other fields | AP = `source_code+destination_code` 6,651/6,651. J/K = Countries-sheet name/region of KSV 39/39. | CONFIRMED |
| R08 | The external link points to `/Users/schen/…/rpw_dataset_2011_2023_q1_with formula.xlsx`, whose sheets `Countriesold`, `CountriesQ320–Q322` and `HistoricalCountryCat` are "not in this file" | The path is confirmed (it also contains `WeChat Files/yanningchen/…/2024-07`). The linked workbook lists **11** sheets, including the six sheet names that *are* in this file. The Phase 3 wording implies it contains only the extra sheets. | PARTIALLY CONFIRMED |
| R09 | Terms of Use and Methodology text sits in drawing text boxes; pandas cannot see it | Terms: cell range `B28:B31` (link labels only). Methodology: `A1` empty. The text is in `xl/drawings`. | CONFIRMED |
| R10 | The Methodology defines no row-level equations | Methodology text describes averages only | CONFIRMED |
| R11 | The Methodology's Global Average uses USD 200 and excludes non-transparent RSPs | Present in the Methodology text | CONFIRMED |
| R12 | File size, hash, title, sheet list (`dataset_notes.md`) | 50,780,339 bytes; hash identical; 6 sheets in that order (`workbook.xml`) | CONFIRMED |
| R13 | No third-party restriction applies (dataset_notes licensing section) | Web sources not re-fetched in this audit. The workbook itself only points to an external "Restricted Data" list. | UNCLEAR (not re-verified) |
| R14 | Periods 2011_1Q–2016_1Q (17) and 2016_2Q–2025_3Q (37); 5 quarters missing | Reproduced | CONFIRMED |
| R15 | 35/49 senders, 105/105 receivers, 310/372 corridors, 368 POST code pairs, 637/713 firms, 440 in both | Reproduced | CONFIRMED |
| R16 | Text numbers in 2024_3Q–4Q; Excel dates and `Yes` in 2025 | Reproduced; all values parse | CONFIRMED |
| R17 | `..` counts per field (DQR §5 table) | Reproduced | CONFIRMED |
| R18 | `destination_region` `..` co-occurs with "HRV, KOR, POL, EST, LVA, LTU, ANT (high income)" | ANT is not high income: its income is `..`. GNQ (upper-middle income) also has region `..` in the Countries sheet. | PARTIALLY CONFIRMED |
| R19 | Total ≈ fee/amount×100 + margin within 0.01 pp in 99.57 / 99.64 / 99.96 / 99.97% of rows | 99.569 / 99.644 / 99.962 / 99.971% (213 / 175 / 78 / 60 exceptions) | CONFIRMED |
| R20 | Margin ≈ (1 − applied/interbank)×100 within 0.01 pp in ~95–96% of rows | 96.0 / 96.0 / 94.8 / 95.2% | CONFIRMED |
| R21 | "A positive margin means the sender receives less than at the interbank rate" | True when the rates are quoted as pay-out currency per send unit. Fails economically in the inverted ZAFZWE periods: applied 15.50 < interbank 15.74 ZAR/USD would favour the sender, yet the stored margin is +1.4–2.3 (F28). | PARTIALLY CONFIRMED |
| R22 | Exceptions = zero cc2 amount (103), zero interbank (1), margin 0 with differing rates, cc2 duplicating cc1 (2013_2Q AUSPHL) | These exist, but the list omits the largest clusters: 124 of 213 PRE cc1 exceptions are in **2014_2Q**; corridor SGPTHA alone has 66; **39 PRE rows report total = margin only, omitting a non-zero fee** (e.g. SGPTHA BKK Forex 2014_3Q: fee 12 on 260, reported 0.79). The AUSPHL example could not be reproduced in the rows inspected (cc1 = cc2 margins there match the rates). | PARTIALLY CONFIRMED |
| R23 | Same currency ≥99.9%; same applied rate 96–97%; cc2/cc1 = 2.5 in ~56–60% | 97.3% / 96.3% same rate. Ratio within 0.01: 59.5% / 56.4%; exactly 2.5 only 46.6% / 44.1%; within 0.05: 98.6% / 98.4%. | CONFIRMED |
| R24 | Negative counts; every negative total has a negative margin | Reproduced | CONFIRMED |
| R25 | Transparency × margin table (DQR §6) | Every cell reproduced (4,036 / 8,866 / 3,351 / 25,885; notes 3,962 / 6 / 3,315 / 282) | CONFIRMED |
| R26 | Exact disclaimer text, used as evidence that 0 ≠ zero cost | Verbatim match (see §4). Three further variants also exist. | CONFIRMED |
| R27 | For `transparent = no`, total cost "covers the fee only and understates the full cost" | Fee-only arithmetic holds in 4,032/4,057 PRE and 3,349/3,361 POST cc1 rows. **21 PRE / 10 POST** `no` rows carry a non-zero margin. "Understates" is an inference: the notes say the cost is *undisclosed*, not that it is positive. | PARTIALLY CONFIRMED |
| R28 | `yes` rows with margin 0 and rate 1 are mostly same-currency services (**inferred**) | Supported where notes say "USD service"/EUR pay-out. But of the 6,775 PRE / 21,103 POST `yes` rows with margin 0 and rate 1, **1,621 / 11,395 have no note at all** (neither standard note nor note2). | PARTIALLY CONFIRMED |
| R29 | No `transparent = no` after 2021_4Q; reason unclear | Confirmed (see F32 for the 2021 transition) | CONFIRMED |
| R30 | 282 POST `yes` rows carry a "not transparent" note | 282: 272 in 2021_3Q–2022_1Q, 10 scattered | CONFIRMED |
| R31 | `period + id` unique in both sheets | Reproduced | CONFIRMED |
| R32 | `id`: 5 reused in PRE (10 rows); unique in POST; no overlap | Reproduced (ids 44140–44144) | CONFIRMED |
| R33 | Candidate-key table values (DD §1) | Every row reproduced, e.g. POST `…+payment instrument+access point+pickup method` = 196,316 distinct / 15,598 rows in duplicate groups | CONFIRMED |
| R34 | Duplicates ignoring `id`: 133 PRE / 189 POST | POST: 372 rows in 183 groups, i.e. 189 surplus rows. PRE: 266 rows, 133 surplus. The numbers are "surplus rows", not "rows in duplicate groups"; the documentation does not say which. | CONFIRMED |
| R35 | Grain: "one row = one service (firm × corridor × service configuration) in one period" | Not falsified, but not demonstrated either. The duplicate rows are identical in **every** field, including date and all costs. "Service" is not a recorded entity: the id changes every period. Equally consistent: duplicated survey entries. | PARTIALLY CONFIRMED |
| R36 | 36 shared column names, 5 PRE-only, 6 POST-only headed | Reproduced | CONFIRMED |
| R37 | `product` dropped (Legend) | Legend text "dropped"; the column is absent from POST | CONFIRMED |
| R38 | `payment instrument` added (Legend NEW) | Confirmed | CONFIRMED |
| R39 | `sending location` → `access point`: "concept yes, vocabulary no" | Rename is in the Legend. But PRE values are almost entirely `Not available` in 2011_1Q–2013_2Q (F14), and `at Branch` does not separate agent from bank branch. In practice the comparable PRE window is 2013_3Q–2016_1Q only. | PARTIALLY CONFIRMED |
| R40 | `coverage` → `receiving network coverage`: the scale changed | Geographic labels vs High/Medium/Low; no mapping in the workbook | CONFIRMED |
| R41 | Pick-up split; "POST moves place-type values into `pickup location`" | POST `pickup method` still has `Home Delivery` (13) and `ATM Network` (62). `pickup location` also holds account/wallet-like values (`Own/partner Bank account`, `Vodafone mobile wallet`, `Any Bank`). | PARTIALLY CONFIRMED |
| R42 | `product` information is split across `payment instrument` (sender) and `pickup method` (receiver) | `product` also encodes channel (`Online service` 7,671; `Mobile` 386; `Door to door` 1,216) and currency (`USD/EUR/LCU/JPY/GBP service`) | PARTIALLY CONFIRMED |
| R43 | `sending network coverage` is in the Legend but absent from the data | Confirmed | CONFIRMED |
| R44 | `note1` ≈ `Standard Note` (**inferred**) | The same standard sentences occur verbatim in both | CONFIRMED |
| R45 | `corridor` and `pickup location` are not in the Legend | Confirmed (Legend A1:B36) | CONFIRMED |
| R46 | Region/income labels are the classification "in force when the row was recorded" (**inferred**) | Constant within period × code and different from the 2025 Countries sheet, which is consistent with the reading. But the 2024_1Q–2Q `Lower income` label shows that some differences are labelling variants, not vintages. Nothing in the workbook documents the vintage. | UNCLEAR |
| R47 | ANT is "the only income case" and should become missing | ANT is the only `..` income in the *data* (121 PRE rows). The Countries sheet also has VEN = `..`. ANT is `..` in all four classification fields. | PARTIALLY CONFIRMED |
| R48 | Kosovo `KSV`/`XKX`, 95 rows (2021_4Q, 2023_1Q) | 34 + 61 = 95; `XKX` is absent from the Countries sheet | CONFIRMED |
| R49 | Provider renames are recorded only in notes (Transferwise → Wise) | `Transferwise` last appears 2020_4Q, `Wise` first appears 2021_1Q; no structured field links them | CONFIRMED |
| R50 | The panel is unbalanced (corridors, firms, senders enter and exit) | Counts reproduced | CONFIRMED |

## 3. Explicitly requested inference audits

| Topic | Phase 3 position | Reproduced evidence | Counterexamples / alternatives | Audit verdict |
|---|---|---|---|---|
| Meaning of `..` | Undefined in the workbook; field-specific readings inferred | Confirmed undefined: no Legend/Methodology text mentions `..`. It is used in the Countries sheet and in the data. | It is a generic "not provided" token whose meaning differs by field | Keep it as **source token "not provided"**; any field meaning is a hypothesis. Confidence downgraded to Medium. |
| Lending `..` | "No lending category", mostly high income | High-income countries are all `..` | CUB, PRK, PSE (not high income) and ANT are also `..`. Alternative reading: not a World Bank member / not eligible / not classified. | PARTIALLY CONFIRMED; downgrade |
| G8/G20 `..` | Not a member | The 19 non-`..` codes are exactly the G20 member countries; data = Countries sheet in 100% of rows | No counterexample. RUS still `G8/G20`, so the G8 part is historical. | Strongly supported; stays an inference |
| Netherlands Antilles | `..` income → missing | ANT: 121 PRE rows (destination). `..` in region, income, lending and G8G20. | VEN also has `..` income in the Countries sheet (not in the data). ANT is a dissolved entity, which explains why every field is unclassified (external knowledge, not in the workbook). | PARTIALLY CONFIRMED |
| Applied FX rate units/direction | Receiving currency per 1 sending LCU (inferred) | Holds for e.g. USAPHL (≈ 41–57 PHP/USD), USACRI (≈ 514 CRC/USD), GBRVNM (≈ 35,000 VND/GBP) | KOR→CHN/VNM ≈ 0.0008 (USD per KRW) in every period. TZA→KEN, JPN→PHL, AUS→CHN and GBR→NGA switch between USD and local-currency quotes. ZAF→ZWE is inverted in 5 periods. Rate = 1 is used as a placeholder. | **INCORRECT**. Correct reading: pay-out currency per send unit; pay-out currency unrecorded; inconsistent across periods. |
| Corridor meaning | `source_code + destination_code` (observed) | PRE 100%. POST 100% except 95 Kosovo rows. 6,651 cells are literally `=C&I`. | No alternative meaning found | CONFIRMED |
| Pickup location | Unclear; looks like where cash is collected | 98.1% of populated values are on `pickup method = Cash` rows | `Agent` on 1,264 `Bank account` and 116 `Mobile wallet` rows; bank/wallet names as values; blank share jumps to ~80% from 2022_4Q | Remains **UNCLEAR**; the completeness break is new |
| Non-transparent margin = 0 | Not a measured zero | The workbook note text says so explicitly (§4) | 21 PRE / 10 POST `no` rows have real margins. The disclaimer also appears on 1,011 `transparent = yes` PRE rows in note2 (FRA/ITA/RUS senders). | CONFIRMED that 0 ≠ zero cost; the "fee-only" description needs qualifying |

## 4. Cost model (cc1 / cc2)

| Item | Finding | Source |
|---|---|---|
| `cc1` = USD 200, `cc2` = USD 500 | CONFIRMED. Legend: `cc(X) denomination amount` = "surveyed amount sent in USD". Values: PRE cc1 200 in 49,406/49,491 rows (others 201 ×3, 202 ×1, 6 ×1, blank 80); PRE cc2 500 in 49,401 (501 ×9, 502 ×3, blank 78: 77 ZAF + 1 USA, 2014_1Q). POST: 100% 200 / 500. | A + D |
| `ccX lcu amount` | Send amount in send currency, rounded to convenient local amounts (cc2/cc1 within 0.05 of 2.5 in ~98.5%). The 103 blank cc1 amounts are the same 103 rows as the cc2 = 0 amounts (2014_3Q RUS). | A + D |
| `ccX lcu code` | Not always ISO 4217 (`CFA`, `CLF`). cc1 ≠ cc2 in 46 PRE rows. | A + D |
| `ccX lcu fee` | Send-currency fee; never negative | A + D |
| `ccX lcu fx rate`, `inter lcu bank fx` | Quote currency = unrecorded pay-out currency; inconsistent by period; placeholder 1; one interbank 0 | D (F28/F29) |
| `ccX fx margin` | (1 − applied/interbank)×100 for ~95–96% of rows within 0.01 pp. Residuals are concentrated where the interbank rate has only 2 significant digits (≈ 40% match at 0.1 pp, vs ≥ 91% for other precisions). This suggests the margin was computed from unrounded rates (inference). | A + D + E |
| `ccX total cost %` | fee/amount×100 + margin | D |

**Total-cost identity** (|reported − (fee/amount×100 + margin)| ≤ 0.01 pp)

| Sheet | Amount | Testable rows | Within 0.01 pp | % | Exceptions |
|---|---|---:|---:|---:|---:|
| PRE | cc1 | 49,381 | 49,168 | 99.569 | 213 |
| PRE | cc2 | 49,178 | 49,003 | 99.644 | 175 |
| POST | cc1 | 204,445 | 204,367 | 99.962 | 78 |
| POST | cc2 | 203,396 | 203,336 | 99.971 | 60 |

**Exception examples**
- PRE `USALBR` Western Union 2014_2Q: fee 10 / 200, margin 0, reported 7.5 vs 5.0.
- PRE `SGPTHA` BKK Forex 2014_3Q: fee 12 / 260, margin 0.79, reported 0.79 (fee omitted).
- PRE `JPNCHN` ICBC 2013_4Q: fee 4,500 / 17,000, margin 0.68, reported 0.68 (fee omitted).
- POST `TURBGR` Turkey IS Bank 2025_3Q: reported 307.2. This is extreme but *satisfies* the identity.
- POST `DEUNGA` ATL Money Transfer 2022_4Q: negative margin and negative total, consistent with the identity.

**Are the exceptions documented?** No. The workbook explains negative margins (promotion notes) and undisclosed FX cost, but gives no explanation for fee-omitted totals or for the 2014_2Q cluster. These remain undocumented data anomalies.

## 5. Transparency

| Question | Answer | Evidence |
|---|---|---|
| What does `transparent` mean? | Whether the RSP disclosed the applied exchange rate to the researcher | Legend: "if yes, indicates that the RSP provided the researcher with the exchange rate applied to the transaction; if no, … not provided" |
| Why `no` + margin 0 ≠ zero FX cost | The workbook says so | Standard note: *"This RSP is not transparent: the exchange rate applied to the transaction was not disclosed. The 0% in the exchange rate margin does NOT necessarily mean that there is no exchange rate cost, but rather that this cost is not disclosed to the sender at the time of sending."* Variants: *"…not known by the sender…"*; *"…an exchange rate to the receiving country's local currency was not provided."* |
| Is `total cost %` for `no` rows complete? | **No: it is fee-only arithmetic for ≥ 99.3% of `no` rows** (4,032/4,057 PRE, 3,349/3,361 POST cc1), so the FX component is not included. Whether the true cost is higher is not documented. | D + note text |
| Is the flag stable over time? | **No (new finding).** `no` counts fall from 133 (2021_1Q) to 58, 32, 30, then 0. Meanwhile 272 `yes` rows in 2021_3Q–2022_1Q say "Service (is) not transparent – account required for detailed price info" or similar; of all 282 `yes` rows with a not-transparent note, 88.7% have non-zero margins. | D; interpretation inferred |

## 6. Natural unit of observation

- `period + id` is unique in both sheets; `id` alone is unique only in POST.
- No descriptive combination is unique (R33). Even all fields except `id` leave 133 / 189 surplus rows.
- The duplicate rows are identical in every field, including `date`.
- **Verdict.** The statement "one row = one service × corridor × period" is a reasonable *working hypothesis*. It is not established by the workbook. What is established: one row = one survey record identified by `period + id`, carrying USD 200 and USD 500 quotes for one firm in one corridor.

## 7. 2016 schema change

| Legend claim | Verdict | Oversimplification found |
|---|---|---|
| `product` dropped | CONFIRMED | `product` also encodes channel and currency (R42) |
| `payment instrument` added | CONFIRMED | — |
| `sending location` → `access point` | PARTIALLY | PRE field effectively uncollected 2011_1Q–2013_2Q; vocabularies differ |
| `coverage` → `receiving network coverage` | CONFIRMED as a rename, NOT semantically equivalent | The scale changed (geographic vs ordinal) |
| Pick-up structure changed | PARTIALLY | Overlapping vocabularies; `pickup location` undefined; PRE blanks are period-structured |
| `sending network coverage` missing | CONFIRMED | — |

## 8. Missed columns / structure

| Check | Result |
|---|---|
| Excel fields absent from the documentation | None. All 41 PRE and 47 POST populated columns are documented. |
| Documented fields absent from Excel | `sending network coverage` (already documented as absent) |
| Undocumented populated columns | None beyond AQ–AU (already documented) |
| Hidden rows/columns | None in any sheet |
| Merged cells | None in the data sheets. Legend `A1:B1`, `A31:B31` and Countries `A1:E1` are merged. **Not documented in Phase 3** (minor). |
| Formulas | Only POST J/K/AP (R04–R07) |
| Helper columns | AQ–AU only; hard-coded values, not formulas |

## 9. Manual row audit (30 rows)

Each row's raw cell values were read directly from the worksheet XML, independently of pandas, and compared field by field with the pandas representation used in Phase 3.
- "XML ≠ pandas": the number of fields whose values differ.
- "Recomputed": fee/amount×100 + margin.

| # | Sheet | Excel row | Period | Corridor | Firm | transparent | cc1 LCU amt | fee | applied fx | interbank | margin | total | Recomputed | XML ≠ pandas | Note |
|---|---|---:|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | PRE | 572 | 2011_1Q | DEUBIH | Postbank | yes | 160 EUR | 8 | 1 | 1 | 0 | 5 | 5.000 | 0 | rate 1 with transparent = yes |
| 2 | PRE | 9669 | 2012_3Q | ZAFMOZ | MoneyGram | yes | 1370 ZAR | 108 | 0.1152 | 0.11936 | 3.49 | 11.37 | 11.373 | 0 | rate in USD per ZAR |
| 3 | PRE | 18583 | 2013_3Q | ZAFMOZ | First National Bank of SA | yes | 1370 ZAR | 230 | 2.81 | 3.0593 | 8.15 | 24.94 | 24.938 | 0 | same corridor, rate now MZN per ZAR (F28) |
| 4 | PRE | 27736 | 2014_2Q | GBRBGD | Sigue Money Transfers | yes | 120 GBP | 5 | 130.77 | 130.528 | −0.19 | 3.98 | 3.977 | 0 | negative margin |
| 5 | PRE | 39442 | 2015_2Q | GBRZMB | Western Union | yes | 120 GBP | 6.9 | 11.075 | 11.319 | 2.16 | 7.91 | 7.910 | 0 | normal |
| 6 | PRE | 49029 | 2016_1Q | USACRI | Western Union | yes | 200 USD | 8 | 513.825 | 534.402 | 3.85 | 7.85 | 7.850 | 0 | normal |
| 7 | PRE | 29254 | 2014_3Q | DEUIND | HypoVereinsbank | no | 140 EUR | 37.5 | 1 | 1 | 0 | 26.79 | 26.786 | 0 | non-transparent, fee only |
| 8 | PRE | 3028 | 2011_3Q | FRADZA | Banque Populaire | no | 140 EUR | 29.5 | 1 | 1 | 0 | 21.07 | 21.071 | 0 | non-transparent, fee only |
| 9 | PRE | 4707 | 2011_3Q | GBRPHL | PNB | yes | 120 GBP | 6.5 | 68 | 67.638 | −0.54 | 4.88 | 4.877 | 0 | negative margin |
| 10 | PRE | 30121 | 2014_3Q | RUSKGZ | PrivatMoney | yes | (blank) RUB | 150 | 35.02 | 35.02 | 0 | 2.14 | n/a | 0 | blank cc1 amount (one of the 103) |
| 11 | PRE | 2401 | 2011_1Q | USAIND | Citibank | yes | 200 USD | 0 | 44.46 | 45.57 | 2.44 | 2.44 | 2.440 | 0 | zero fee |
| 12 | PRE | 23520 | 2014_1Q | GHANGA | Stanbic Bank | no | 300 GHS | 225 | 1 | 1 | 0 | 75 | 75.000 | 0 | PRE maximum total |
| 13 | POST | 8643 | 2016_4Q | DEUBIH | Azimo | yes | 140 EUR | 5 | 1 | 1 | 0 | 3.57 | 3.571 | 0 | rate 1, transparent = yes |
| 14 | POST | 24279 | 2017_4Q | AUSLBN | Westpac | yes | 200 AUD | 32 | 0.7258 | 0.76805 | 5.5 | 21.5 | 21.500 | 0 | USD pay-out quote |
| 15 | POST | 40819 | 2018_3Q | USAPHL | Wells Fargo | yes | 200 USD | 4 | 52.39 | 53.35 | 1.8 | 3.8 | 3.800 | 0 | normal |
| 16 | POST | 61463 | 2019_4Q | CANPHL | Ria | yes | 200 CAD | 7 | 38.031019 | 38.39996 | 0.96 | 4.46 | 4.460 | 0 | normal |
| 17 | POST | 75976 | 2020_3Q | ARENPL | Western Union | yes | 735 AED | 15.75 | 32.49 | 32.79894 | 0.94 | 3.08 | 3.083 | 0 | normal |
| 18 | POST | 88552 | 2021_1Q | MYSBGD | CBL Money Transfer | yes | 610 MYR | 10 | 20.43 | 20.46486 | 0.17 | 1.81 | 1.809 | 0 | normal |
| 19 | POST | 128945 | 2022_4Q | USANGA | Western Union | yes | 200 USD | 12.99 | 1 | 1 | 0 | 6.5 | 6.495 | 0 | USD→NGA at rate 1 (USD pay-out) |
| 20 | POST | 146631 | 2023_2Q | CANVNM | Ria | yes | 200 CAD | 5 | 17274 | 17491.6201 | 1.24 | 3.74 | 3.740 | 0 | normal |
| 21 | POST | 177325 | 2024_2Q | ESPCHN | MoneyGram | yes | 140 EUR | 0 | 7.6226 | 7.8207 | 2.53 | 2.53 | 2.530 | 0 | zero fee |
| 22 | POST | 196217 | 2025_1Q | AUTHUN | MoneyGram | Yes | 140 EUR | 3.99 | 380.415295 | 402.509859 | 5.49 | 8.34 | 8.340 | 1 | date: XML serial 45708 = pandas 2025-02-20 (same value) |
| 23 | POST | 13586 | 2017_1Q | ITALKA | Unicredit Banca | no | 140 EUR | 9.2 | 1 | 1 | 0 | 6.57 | 6.571 | 0 | non-transparent |
| 24 | POST | 86583 | 2021_1Q | CHESRB | Ria | no | 160 CHF | 9 | 1 | 1 | 0 | 5.63 | 5.625 | 0 | non-transparent |
| 25 | POST | 182335 | 2024_3Q | SWECHN | Remitly | yes | "1700.00" SEK | "39.900000000" | "0.690000000" | "0.69340" | 0.49 | 2.84 | 2.837 | 0 | text-stored numbers |
| 26 | POST | 200604 | 2025_3Q | GBRVNM | Ria | Yes | 120 GBP | 8 | 35058 | 35573.49475 | 1.45 | 8.12 | 8.117 | 1 | date serial (same value) |
| 27 | POST | 138344 | 2023_1Q | AUTXKX | TransferGo | yes | 140 EUR | 1.05 | 1 | 1 | 0 | 0.75 | 0.750 | 0 | Kosovo `XKX` corridor, KSV code |
| 28 | POST | 188328 | 2024_4Q | KWTEGY | Al Muzaini Exchange | yes | "65.00" KWD | "1.5" | "160.56" | 161.08256 | 0.32 | 2.63 | 2.628 | 0 | formula-cached corridor; trailing-space firm variant |
| 29 | POST | 203121 | 2025_3Q | TURBGR | Turkey IS Bank | Yes | 570 TRY | 1743 | 0.0241 | 0.024444 | 1.41 | 307.2 | 307.199 | 1 | POST maximum; rate in USD/EUR per TRY; date serial |
| 30 | POST | 41976 | 2018_4Q | CHLPER | MoneyGram | yes | 112500 CLP | 3375 | 0.0014 | 0 | 6.67 | 9.67 | 9.670 | 0 | interbank 0: margin not derivable |

**Result**
- 30/30 rows: every field's raw XML value equals the pandas representation. The only differences are the three 2025 Excel date serials, which pandas converts to the same date.
- 29/29 testable rows satisfy the total-cost identity within 0.01 pp.
- The trace contradicts the documented FX-rate units in rows 2–3, 14, 19 and 29.

## 10. Findings by severity

### CRITICAL

None. No finding invalidates the raw-data reading, the cost identity, or the Phase 4 "flag, don't fix" strategy.

### MAJOR

| ID | Existing claim | Evidence | Audit conclusion | Recommended correction | Downstream impact |
|---|---|---|---|---|---|
| M1 | `ccX lcu fx rate` / `inter lcu bank fx` = "receiving currency per 1 sending LCU" (DD §2.4) | F28/F29; rows 2, 3, 14, 19, 29 | INCORRECT. The quote currency is an unrecorded pay-out currency (often USD/EUR); it changes across periods and some periods are inverted; 1 is used as a placeholder. | Rewrite the unit definition. Add a caveat that rate levels are not comparable across rows or periods without knowing the pay-out currency. | Phase 4 must not derive or compare FX levels, receive amounts or cross-period rate series. Margin and total cost (unit-free ratios) stay usable. Flag the inverted ZAFZWE periods and rate-1 placeholders. |
| M2 | PRE `sending location` `Not available` = unclear category; `pick-up method` blank 19% (DD §2.3, §3) | F14, F21 | Both are **period-structured non-collection**: `Not available` covers 100% of 2011_3Q–2013_2Q; pick-up blanks occur only in 2011_1Q–2013_4Q. | Document both as "not collected in these periods". | Any PRE service-attribute analysis or 2016 mapping is valid only for 2013_3Q/2014_1Q–2016_1Q. Treat these values as missing, not as categories. |
| M3 | Transparency: `no` = fee-only total, and the flag has a stable meaning; disclaimer only on `no` rows (DQR §6) | F32, F34, R27 | The flag's coding shifts in 2021 (`no` phases out while `yes` rows carry "not transparent" notes). The disclaimer also appears on 1,011 `yes` rows. 31 `no` rows have real margins. | Document the 2021 transition, the note-based contradictions and the qualified fee-only rule. | A `transparent`-only filter is insufficient. Phase 4 flags should combine the flag, the note text and margin/rate placeholders. Cost comparisons across 2021 are at risk of a definitional break. |
| M4 | Natural grain "one row = one service…" (DQR §7, DD §1) | R35 | A hypothesis, not demonstrated. 133 / 189 surplus rows are fully identical, and "service" is not a persistent entity. | Restate the grain as "one survey record (period + id) with USD 200/500 quotes for a firm × corridor". Label the service reading as an inference. Clarify that 133/189 are surplus rows (PRE 266 / POST 372 rows in duplicate groups). | Phase 4 must keep and flag exact duplicates, not deduplicate silently. Counts of "services" are assumption-based. |

### MINOR

| ID | Existing claim | Evidence | Audit conclusion | Recommended correction | Downstream impact |
|---|---|---|---|---|---|
| m1 | `..` readings for region/lending (DD §2.2, §3; DQR §5) | F06, F08, R18 | Overstated: GNQ, CUB, PRK, PSE and ANT are counterexamples | Describe `..` as "not provided by source"; give field-specific readings as hypotheses | Keep `..` as an explicit token. Do not map it to "high income" / "no lending". |
| m2 | `..` income only ANT (DD §3) | F07, R47 | True for the data only; the Countries sheet also has VEN | Note VEN | Relevant only if the Countries sheet is used as a lookup |
| m3 | `Lower income` = undocumented label (DD §2.2) | F07 | Occurs only in 2024_1Q–2Q, on `Low income` countries | Document it as a probable label variant (inferred) | Income mapping in Phase 4 |
| m4 | `date` text/datetime only (DD §2.1) | F03 | 4 PRE rows 3–10 quarters off; 181 POST 2021_3Q rows dated in the previous quarter | Document; use `period` as the time key | Do not derive the period from the date |
| m5 | `ccX lcu code` = ISO 4217 (DD §2.4) | F26 | `CFA`, `CLF`; 46 PRE cc1 ≠ cc2 rows | Document | Currency joins need a mapping |
| m6 | Total-cost exceptions list (DQR §6) | R22 | Largest clusters (2014_2Q; fee-omitted totals) not listed | Add the clusters | Residual flags should capture "fee omitted" separately |
| m7 | FX-margin exceptions unexplained (DQR §6) | F30 | Mostly 2-significant-digit interbank rounding (inferred) | Add as a likely explanation | Use a looser tolerance or a precision-aware flag |
| m8 | `pickup location` meaning (DD §2.3) | F23 | Still unclear; the blank share jumps to ~80% from 2022_4Q | Document the break and the counterexamples | Do not use the field for trends across 2022_4Q |
| m9 | `product` = instrument + pick-up (SC §6) | R42, F13 | Also encodes channel and currency | Correct the wording | No 1:1 mapping, as already stated |
| m10 | Pick-up split moves place types to `pickup location` (SC §4) | R41 | Overlap in both directions | Correct the wording | Mapping tables must be bidirectional-aware |
| m11 | External workbook sheets "not in this file" (DQR §3) | R08 | The linked workbook also lists the six sheets present here | Correct the wording | None |
| m12 | Merged cells not documented | R03 | Legend and Countries title rows are merged | Mention them | Loaders must skip title rows (already done) |
| m13 | Margin sign meaning (DQR §6) | R21 | Fails in inverted-quote periods | Add a caveat | As M1 |
| m14 | Same-currency explanation for `yes` + margin 0 (DQR §6) | R28 | 13,016 such rows have no note to support it | Keep it as inferred; quantify | Zero margins on `yes` rows are not all verified zeros |

### NO ISSUE

Confirmed without correction:
- the row/column counts, the period inventory and the missing quarters;
- the unique counts;
- the formula count, location, cache, pandas agreement and reconstructability;
- the used range, and the absence of hidden or undocumented columns;
- AQ–AU helper columns;
- the `id` behaviour;
- `period + id` uniqueness;
- the candidate-key table;
- the corridor construction and the Kosovo exceptions;
- the country renames;
- the `firm` / `firm_type` variants;
- the `cc1` = USD 200 / `cc2` = USD 500 definition and the denomination anomalies;
- the total-cost identity percentages;
- the margin formula direction (for normal quotes);
- negative values;
- the transparency × margin table;
- the verbatim disclaimer;
- type drift in 2024–2025;
- literal `N/A` handling;
- `sending network coverage` absent;
- the `coverage` scale change;
- `product` dropped, `payment instrument` added;
- `note1` ≈ `Standard Note`.

## 11. Final answers

1. **Claims checked:** 90 (40 field-level, 50 other).
2. **Fully confirmed:** 61.
3. **Partially confirmed:** 24.
4. **Incorrect:** 2 (FX-rate and interbank-rate units/direction). Unsupported: 0.
5. **Unclear:** 3 (`pickup location`; classification-vintage inference; licensing, not re-verified here).
6. **Five most important corrections**
   1. FX-rate units: the pay-out currency is unrecorded, quote direction changes over time, and 1 is a placeholder (M1).
   2. PRE `sending location` `Not available` and `pick-up method` blanks are period-level non-collection (M2).
   3. The transparency flag's coding shifts in 2021; the disclaimer is not exclusive to `no`; the fee-only rule needs qualifying (M3).
   4. The grain statement is a hypothesis; clarify "surplus rows" vs "rows in duplicate groups" (M4).
   5. Region/lending/income `..` and `Lower income` readings are overstated (m1–m3).
7. **New fields / behaviours found**
   - inverted and mixed FX quote currencies;
   - period-structured non-collection in PRE;
   - the 2021 transparency recoding;
   - the disclaimer on `yes` rows;
   - the `pickup location` completeness break at 2022_4Q;
   - fee-omitted totals clustered in 2014_2Q–3Q;
   - interbank-rate rounding as the source of margin residuals;
   - non-ISO currency codes and cc1/cc2 currency mismatches;
   - date/period mismatches;
   - `Lower income` confined to 2024_1Q–2Q;
   - VEN `..` income in the Countries sheet;
   - merged title cells;
   - the POST id prefix pattern.

   No undocumented *column* was found.
8. **Is the dictionary reliable enough for Phase 4?** Reliable for column inventory, types, missingness counts, cost identity, formulas and keys. **Not yet reliable** for FX-rate semantics, PRE service-attribute missingness, the transparency flag over time, and the grain wording.
9. **Must be corrected before Phase 4:** M1–M4. The minor items m1–m14 can be corrected in the same documentation pass.
10. **Claims that remain assumptions, not documented facts**
    - every field-specific meaning of `..` (including G8/G20 = non-member);
    - the classification-vintage reading of region/income;
    - `Lower income` = `Low income`;
    - `note1` ≡ `Standard Note`;
    - `pickup location` = cash pick-up place;
    - "one row = one service";
    - same-currency services explaining `yes` + margin 0;
    - interbank rounding explaining margin residuals;
    - the reason `no` disappears after 2021;
    - that the cost omitted for non-transparent rows is positive;
    - AQ–AU being non-informative helpers;
    - the licensing conclusion (not re-verified in this audit).
