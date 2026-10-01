# Data Dictionary Audit — Phase 3.5

This is an independent, adversarial re-check of `docs/data_dictionary.md`. Every claim was re-tested against the raw workbook `data/raw/rpw_dataset_2011_2025_q3.xlsx` (SHA-256 `f1d7265b…a2d8`, verified unchanged before and after the audit).

- **Read mode.** All sheets were re-read without header assumptions (`header=None, dtype=object, keep_default_na=False, na_values=[]`). The worksheet XML was also parsed directly with a separate streaming parser and shared-string table, so it does not depend on pandas/openpyxl.
- **No existing documentation was edited.** Corrections are recommended here and in `docs/phase3_audit_report.md`. They are not applied.
- **PRE** = `Dataset (up to Q1 2016)`; **POST** = `Dataset (from Q2 2016)`.

**Result scale**

| Result | Meaning |
|---|---|
| CONFIRMED | Reproduced, and no counterexample was found. |
| PARTIALLY CONFIRMED | The core is right, but part of the claim is overstated, incomplete or undocumented. |
| UNSUPPORTED | No evidence for the claim. |
| INCORRECT | Counterexamples falsify the claim. |
| UNCLEAR | The evidence cannot decide. |

**Source of definition** — A = Legend, B = Methodology, C = Countries sheet, D = observed data, E = inference.

## Summary

| Result | Fields / conventions |
|---|---:|
| CONFIRMED | 24 |
| PARTIALLY CONFIRMED | 13 |
| UNSUPPORTED | 0 |
| INCORRECT | 2 |
| UNCLEAR | 1 |
| **Total audited** | **40** |

## 1. Identifiers, time, countries, corridor

| # | Field | Existing interpretation | Evidence (this audit) | Def. source | Audit result | Confidence | Correction required? |
|---|---|---|---|---|---|---|---|
| F01 | `id` | Row identifier, not persistent. PRE: 5 ids reused (10 rows). POST: unique. No overlap between sheets. POST str in 13,288 rows. | PRE 49,486 distinct / 49,491 rows. The 5 reused ids (44140–44144) pair 2014_4Q ZAFZWE with 2015_1Q BELCOD/AREEGY. POST 204,469 distinct. Overlap 0. Types: 191,181 int + 13,288 str. **New:** POST ids look like a period-specific prefix plus a sequence number (e.g. 2016_2Q = 620160001–620163905; 2022_2Q = 8090001–8095892). | A + D | CONFIRMED | High | No. Optionally note the prefix pattern (inferred). |
| F02 | `period` | Format `YYYY_nQ`. Missing quarters: 2011_2Q, 2011_4Q, 2012_2Q, 2012_4Q, 2025_2Q. | 17 PRE and 37 POST period labels; those five quarters are absent. | A + D | CONFIRMED | High | No |
| F03 | `date` | Text `dd/Mon/yyyy`. Excel datetimes in 2025 (13,117 rows). "Many dates per period." | Types reproduced, and every value parses. **Counterexamples not documented:** 4 PRE rows (all SGPCHN MoneyGram) are dated 3–10 quarters away from their period label: 2011_1Q dated 15/Jul/2013, 2012_3Q dated 13/May/2013, 2013_1Q dated 26/Jan/2011, 2013_4Q dated 03/Sep/2012. 181 POST rows, all in 2021_3Q, are dated in the previous quarter (2021_3Q starts 24 May 2021). | A + D | PARTIALLY CONFIRMED | High | Yes (minor): `date` is not always inside `period`. |
| F04 | `source_code` / `destination_code` | ISO3. Kosovo `KSV` is non-ISO. All codes exist in the Countries sheet. 35/49 senders, 105/105 receivers. | Every code is in the Countries sheet, and the counts are reproduced. `KSV` is in the Countries sheet; `XKX` is not. | A + C + D | CONFIRMED | High | No |
| F05 | `source_name` / `destination_name` | Renames CZE, TUR, MKD, SWZ. 37 cells are cached external formulas. | Multi-name codes: source CZE, TUR; destination MKD, SWZ, TUR. The 37 J-column formulas are all KSV rows in 2023_1Q. | A + D | CONFIRMED | High | No |
| F06 | `*_region` | Region label. POST adds the MENA-AfPak label. "Classification in force when the row was recorded" (**inferred**). `..` = "not classified, mainly high-income". | Label change confirmed. Region is constant within each period × code. As-recorded region equals the Countries-sheet region in 100% of PRE source rows but only 90.3% / 87.8% of destination rows, which fits the vintage reading without proving it. **`..` counterexamples:** in the Countries sheet, `..` covers 74 of 83 high-income countries plus GNQ (upper-middle income) and ANT (income `..`). 9 high-income countries do have a region (ASM, BGR, CRI, GUY, HUN, PLW, PAN, ROU, SYC). | A + C + D + E | PARTIALLY CONFIRMED | Medium | Yes: `..` means "no region given"; it is not equivalent to high income. The vintage reading stays an inference. |
| F07 | `*_income` | PRE OECD/nonOECD labels; POST `High income`. `Lower income` (1,490 rows) is undocumented. `..` only for ANT. | 1,490 = 18 source + 1,472 destination rows, confirmed. **New:** `Lower income` occurs only in 2024_1Q and 2024_2Q. Every country carrying it (AFG, COD, ERI, ETH, GMB, LBR, MDG, MLI, MOZ, MWI, RWA, SDN, …) is `Low income` in the Countries sheet, and in adjacent periods (checked ETH and RWA in 2023_4Q and 2024_3Q). So it is most likely a label variant of `Low income` (inferred). In the *data*, `..` is ANT only (121 PRE rows). In the *Countries sheet*, VEN also has income `..`. PRE income equals the Countries-sheet label in only 5.7% of source rows. | A + C + D + E | PARTIALLY CONFIRMED | High | Yes (minor): describe `Lower income` as a two-period variant, and note VEN in the Countries sheet. |
| F08 | `*_lending` | `..` mostly high-income (**inferred**: no lending category). | High-income senders all `..`. Destination `..`: ANT, EST, HUN, LTU, LVA (PRE); CUB, EST, HUN, LTU, LVA, PSE (POST). In the Countries sheet, `..` also covers the non-high-income CUB, PRK and PSE, plus ANT. "No lending category" is plausible, but the workbook never says so. | A + C + E | PARTIALLY CONFIRMED | Medium | Yes: label it as an inference and list the non-high-income counterexamples. |
| F09 | `*_G8G20` | `..` = not a member (**inferred**). | The 19 non-`..` countries in the Countries sheet are exactly ARG AUS BRA CAN CHN DEU FRA GBR IDN IND ITA JPN KOR MEX RUS SAU TUR USA ZAF (the G20 member countries). Data values equal the Countries sheet in 100% of rows. RUS is still `G8/G20` in the "updated Q3 2025" sheet, so the G8 label is historical. | A + C + E | PARTIALLY CONFIRMED | High (inference strongly supported) | Minor: keep it marked as inferred, and note that the G8 component is historical. |
| F10 | `corridor` | `source_code+destination_code`. 100% match in PRE. POST: 95 `XKX` rows. 6,651 formula cells. Not in the Legend. | PRE 0 mismatches. POST 95 mismatches, all destination KSV / corridor `…XKX` (2021_4Q: 34; 2023_1Q: 61). Formula cells: 6,651, all 2024_4Q. Corridor is absent from the Legend. | D | CONFIRMED | High | No |

## 2. Provider and service attributes

| # | Field | Existing interpretation | Evidence (this audit) | Def. source | Audit result | Confidence | Correction required? |
|---|---|---|---|---|---|---|---|
| F11 | `firm` | Case/space variants (~15); 637 / 713 names, 440 in both; Transferwise→Wise only in notes. | 1 PRE + 14 POST case/space groups (e.g. `Azimo`/`azimo`, `TapTap Send`/`Taptap Send`, trailing spaces). 637 / 713 / 440 reproduced. `Transferwise` runs to 2020_4Q and `Wise` starts in 2021_1Q. | A + D | CONFIRMED | High | No |
| F12 | `firm_type` | 10 / 11 labels; 4 PRE / 43 POST firms have more than one type. | Reproduced exactly. | A + D | CONFIRMED | High | No |
| F13 | `product` | PRE only, 37 labels, `N/A` 214. Legend: dropped. Schema doc: its information is split across `payment instrument` + `pickup method`. | Counts confirmed. **But** the labels also encode access channel (`Online service` 7,671, `Mobile` 386, `Door to door` 1,216, `Online to cash` 10) and currency (`USD service` 89, `EUR service` 32, `LCU service` 9, `JPY service` 3, `GBP service` 2). So `product` is not only instrument + pick-up. | A + D | PARTIALLY CONFIRMED | High | Yes: remove the "split across payment instrument and pickup method" simplification. |
| F14 | `sending location` (and the `Not available` convention) | `Not available` in 16,559 rows (33%). Meaning **unclear**; keep it as a category. | **`Not available` is period-structured.** It is 100% of rows in 2011_3Q, 2012_1Q, 2012_3Q, 2013_1Q and 2013_2Q, 95% of 2011_1Q (2,474/2,603), and 0% from 2013_3Q onward. This is the signature of a field that was not collected in those periods, not of a service attribute. | A + D | PARTIALLY CONFIRMED | High | **Yes (major):** document `Not available` as period-level non-collection (2011_1Q–2013_2Q). |
| F15 | `access point` | Rename of `sending location`; 22 labels; never blank. | 22 labels, 0 blanks. The Legend states the rename. | A + D | CONFIRMED | High | No |
| F16 | `payment instrument` | POST only, 26 labels, case variants. | 26 labels, 0 blanks; `Credit Card`/`Credit card` both exist. | A + D | CONFIRMED | High | No |
| F17 | `speed actual` | Ordered categories; PRE `N/A` 10; POST case variants and one `1-3 days`. | Reproduced. The `1-3 days` row is 2020_3Q NLDTUR Western Union; it overlaps the `Next day`/`2 days`/`3-5 days` scale. | A + D | CONFIRMED | High | No |
| F18 | `coverage` | PRE only, geographic labels; 18 blank, 2 `N/A`. | Reproduced; `Nationwide` = 94%. | A + D | CONFIRMED | High | No |
| F19 | `receiving network coverage` | POST; High/Medium/Low (+`low`); different scale. | Reproduced. `low` (12 rows) occurs only in 2025. | A + D | CONFIRMED | High | No |
| F20 | `sending network coverage` | In the Legend, absent from POST. | No header matches. The only High/Medium/Low column is `receiving network coverage`. The populated range ends at AU. | A + D | CONFIRMED | High | No |
| F21 | `pick-up method` | PRE, blank 9,388 rows (19%), 31 labels. | Counts confirmed. **Blanks are period-structured:** they occur only in 2011_1Q–2013_4Q (e.g. 2012_1Q 89% blank, 2013_1Q 97%), and there are 0 blanks from 2014_1Q onward. A typo label exists (`ATM Network, Bank Acciunt`). | A + D | PARTIALLY CONFIRMED | High | Yes (major, with F14): document blanks as early-period non-collection. |
| F22 | `pickup method` | POST; Legend text. | 10 labels, 0 blanks. | A + D | CONFIRMED | High | No |
| F23 | `pickup location` | **Unclear**; values look like where cash is collected. | 98.1% of populated values (87,158/88,855) are on `pickup method = Cash` rows. **Counterexamples:** 1,264 `Bank account` rows have `Agent`, and 116 `Mobile wallet` rows have `Agent`. Values also include `Own/partner Bank account`, `Any Bank`, `Arab Bank`, `Vodafone mobile wallet`. 27% of Cash rows are blank. **New:** the blank share jumps from 35–48% (2016_2Q–2022_3Q) to 79–87% from 2022_4Q. | D + E | UNCLEAR | Medium | Yes: keep it unclear, and record the 2022_4Q completeness break and the non-cash counterexamples. |

## 3. Cost fields

| # | Field | Existing interpretation | Evidence (this audit) | Def. source | Audit result | Confidence | Correction required? |
|---|---|---|---|---|---|---|---|
| F24 | `ccX denomination amount` | USD; PRE 80 / 78 blank; odd values 201/202/6 and 501/502. | PRE cc1: 200 ×49,406, 201 ×3, 202 ×1, 6 ×1 (2015_3Q SAUBGD TeleMoney), blank 80. cc2: 500 ×49,401, 501 ×9, 502 ×3, blank 78 (mostly 2014_1Q ZAF corridors, which still have an LCU amount). POST: 200 / 500 in 100% of rows. | A + D | CONFIRMED | High | No |
| F25 | `ccX lcu amount` | Sending LCU. PRE cc1 103 blank; cc2 = 0 in 103 rows. Ratio exactly 2.5 in ~56–60%. | Ratio: 59.5% PRE / 56.4% POST within 0.01, but only 46.6% / 44.1% at exact equality. **New:** the 103 blank cc1 rows are exactly the 103 rows with cc2 = 0 (all 2014_3Q, RUS→CIS corridors, e.g. RUSARM). | A + D | CONFIRMED | High | Minor: state that the ratio is computed with a tolerance, and that the two anomalies are the same 103 rows. |
| F26 | `ccX lcu code` | Local currency of the sender (ISO 4217); sometimes USD/EUR. | **Non-ISO codes exist:** `CFA` (CIV, CMR, SEN, alongside XOF/XAF), `CLF` (Chile, alongside CLP). 46 PRE rows have cc1 ≠ cc2 code (e.g. 2014_1Q AUSLBN: cc1 AUD, cc2 USD or LBP; 2011_3Q RUSAZE: cc1 USD, cc2 RUB). POST: 0 mismatches. | A + D | PARTIALLY CONFIRMED | High | Yes (minor): not always ISO 4217, and not always the same for cc1 and cc2. |
| F27 | `ccX lcu fee` | Sending LCU; blanks PRE 6/208, POST 22/1,072. | Reproduced; no negative fees. | A + D | CONFIRMED | High | No |
| F28 | `ccX lcu fx rate` | Units: "receiving currency per 1 sending LCU" (**inferred**, e.g. USA→PHL ≈ 41.65). | **Falsified as a general rule.** The quote currency is the *pay-out* currency, which is often USD/EUR, not the receiving country's currency. Examples: KOR→CHN / KOR→VNM ≈ 0.0007–0.00095 in every period (USD per KRW, not CNY/VND). TZA→KEN ≈ 0.00046 to 2018_2Q (USD per TZS), then ≈ 0.044 (KES per TZS). JPN→PHL ≈ 0.011–0.013 in 2011_1Q–2012_1Q and 2013_1Q (USD per JPY), but ≈ 0.40–0.53 in 2012_3Q and from 2013_2Q (PHP per JPY). AUS→CHN 1.08 in 2012_1Q (USD) vs ≈ 3.5–6.5 afterwards (CNY). GBR→NGA ≈ 240–500 to 2020_4Q (NGN per GBP), ≈ 1.17–1.41 in 2021_1Q–2024_1Q (USD per GBP), then ≈ 1,900–2,070 from 2024_2Q (NGN). ZAF→ZWE switches between ≈ 0.07 (USD per ZAR) and ≈ 13–15.7 (apparently **inverted**, ZAR per USD) in 2016_1Q–2016_4Q, 2017_3Q, 2018_2Q and 2019_2Q. Sampled row: same corridor ZAFMOZ is 0.1152 in 2012_3Q but 2.81 in 2013_3Q. No column records the pay-out currency. | A + D + E | INCORRECT | High | **Yes:** units = "units of the (unrecorded) pay-out currency per 1 send-currency unit; occasionally inverted; 1 for same-currency/placeholder". |
| F29 | `inter lcu bank fx` | "same as above"; one 0 row (2018_4Q CHLPER MoneyGram). | Same unit problem as F28. The 0 row is confirmed. **New:** placeholder `1` also appears in corridors with different currencies (e.g. GBRNGA medians = 1 in 2015_3Q, 2016_1Q and 2016_2Q; RUSUZB = 1 in 2011_1Q–2013_4Q and 2019_2Q–2021_1Q, then 0.0138 in 2021_4Q). | A + D | INCORRECT | High | Yes, as F28. |
| F30 | `ccX fx margin` | Percent; margin ≈ (1 − applied/interbank)×100 (95–96% within 0.01 pp); negative values; 0 ≠ zero cost for non-transparent. | Direction reproduced: 96.0 / 96.0 / 94.8 / 95.2% within 0.01 pp; the alternative formulas match only 14–26%. **Unexplained in Phase 3:** most exceptions coincide with an interbank rate stored to only 2 significant digits (e.g. 0.00091, 0.0008). When the interbank value has 2 significant digits, only ~40% of rows match within 0.1 pp, against ≥91% for other precisions. So the margin was likely computed from unrounded rates (inferred). | A + D | PARTIALLY CONFIRMED | High | Yes (minor): add the rounding explanation and the inverted-quote caveat (F28). |
| F31 | `ccX total cost %` | ≈ fee / lcu amount × 100 + margin, within 0.01 pp in 99.6–99.97% of rows. Negatives and >100% exist. | Reproduced exactly: PRE cc1 99.569% (213 exceptions), PRE cc2 99.644% (175), POST cc1 99.962% (78), POST cc2 99.971% (60). POST max 307.2 (2025_3Q TURBGR Turkey IS Bank: fee 1,743 TRY on 570 TRY). Every negative total has a negative margin. | A + D | CONFIRMED | High | No (exception structure: see audit report §MINOR). |
| F36 | `cc1` / `cc2` meaning | cc1 = USD 200; cc2 = USD 500. | The Legend defines `cc(X) denomination amount` = "surveyed amount sent in USD". The values are 200 / 500 in ≥99.8% of PRE rows and 100% of POST rows. LCU amounts scale ≈ 2.5× (98.6% / 98.4% within 0.05). The Methodology uses USD 200 for the Global Average. "cc" is never expanded. | A + B + D | CONFIRMED | High | No |

## 4. Transparency, notes and helper columns

| # | Field | Existing interpretation | Evidence (this audit) | Def. source | Audit result | Confidence | Correction required? |
|---|---|---|---|---|---|---|---|
| F32 | `transparent` | PRE yes/no; POST yes/Yes/no; `Yes` = all 2025 rows; no `no` after 2021_4Q (unclear why). | Counts reproduced (PRE 45,434 / 4,057; POST 187,991 / 13,117 / 3,361). 2025_1Q and 2025_3Q are 100% `Yes`. **New:** `no` falls from 133 rows (2021_1Q) to 58, 32, 30, then 0. Meanwhile 272 `yes` rows in 2021_3Q–2022_1Q carry the notes "Service (is) not transparent – account required for detailed price info" / "Service is not transparent", and only 11% of the 282 POST `yes` + not-transparent-note rows have margin 0. So the flag's coding appears to change around 2021 (inferred). | A + B + D | PARTIALLY CONFIRMED | Medium | **Yes (major):** document the 2021 coding shift. Do not treat `yes` after 2021 as equivalent to `yes` before. |
| F33 | `note1` / `Standard Note` | Same role (Legend `standard note`); semi-standard sentences. | The identical non-transparency sentence is the most frequent PRE note (3,427 rows) and is also present verbatim in POST (POST's most frequent note is "Account required for detailed price info", 6,142 rows). Shared standard sentences: EUR pay-out, negative-margin promotion, LCU/USD service. POST adds new sentences (e.g. "Account required for detailed price info"). | A + D | CONFIRMED | High | No |
| F34 | `note2` | Additional info, e.g. corridor currency notes, Wise rename. | Confirmed. **New:** note2 also carries a "The 0% in the exchange rate margin does NOT necessarily mean that there is no exchange rate cost…" disclaimer in 1,028 PRE rows (senders FRA, ITA, RUS), of which 1,011 are `transparent = yes`; it does not occur in POST note2. The disclaimer is therefore **not exclusive to non-transparent rows**. | A + D | PARTIALLY CONFIRMED | High | Yes (minor) |
| F35 | AQ–AU (unlabeled) | 2025_3Q only (6,470 rows): `2025`, `src+2025`, `dst+2025`, `src+2026`, `dst+2026`. | Reproduced: 6,470 populated / 197,999 blank in each column. Hard values, not formulas. | D + E | CONFIRMED | High | No |

## 5. Missing-value conventions (`data_dictionary.md` §3)

| # | Convention | Existing interpretation | Evidence (this audit) | Def. source | Audit result | Confidence | Correction required? |
|---|---|---|---|---|---|---|---|
| F37 | empty cell / empty string | Missing / not recorded. | Blank counts reproduced for every column listed. | D | CONFIRMED | High | No |
| F38 | `..` | G8G20 = not a member; region/lending = "not classified" (mainly high income); income ANT = missing. **Inferred.** | See F06–F09. The G8G20 reading is strongly supported. The region/lending readings have counterexamples (GNQ, CUB, PRK, PSE; 9 high-income countries with a region). Income `..` = ANT in the data, but ANT and VEN in the Countries sheet. ANT is `..` in region, income, lending and G8G20 alike. | C + E | PARTIALLY CONFIRMED | Medium | Yes: present `..` as "value not provided by the source" everywhere, with field-specific *hypotheses*. |
| F39 | literal `N/A` | PRE `product` 214, `speed actual` 10, `coverage` 2; pandas defaults hide them. | Reproduced. | D | CONFIRMED | High | No |
| F40 | `0` margin with `transparent = no` | Not a measured zero (note text); treat as unknown. | 4,036/4,057 PRE and 3,351/3,361 POST `no` rows have cc1 margin 0. The verbatim note: "The 0% in the exchange rate margin does NOT necessarily mean that there is no exchange rate cost, but rather that this cost is not disclosed to the sender at the time of sending." Variants: "…not known by the sender…"; "the amount to be received in local currency was not quoted"; "an exchange rate is not provided until the transfer is being made". | D (note text) | CONFIRMED | High | No |

(F-numbers follow the order fields are listed in `data_dictionary.md`. F36 sits in §3 because it concerns cost semantics.)
