# Data Pipeline — `src/rpw`

The pipeline turns the raw workbook into two analytical datasets. Every transformation is listed below.

**Invariants (checked automatically)**

- The raw workbook is never written to. Its SHA-256 is checked before and after every build.
- No row is ever removed: 253,960 records (49,491 PRE + 204,469 POST) go in and 253,960 come out, and the long dataset has exactly 2 × that many rows.
- Anomalies are **flagged, not corrected**. Raw columns are kept next to every derived column.
- Undisclosed FX costs are never treated as zero. Rows whose FX margin is not disclosed get `fx_margin_disclosed = False` and `cost_completeness = "fee only or FX margin uncertain"`, and they are excluded from `complete_cost_eligible`.

## Run

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
PYTHONPATH=src .venv/bin/python -m rpw.build      # ~2 min; add --no-cache to bypass data/interim cache
.venv/bin/python -m pytest -q
```

## Outputs (`data/processed/`)

| File | Grain | Notes |
|---|---|---|
| `rpw_records_wide.parquet` | one row per survey record (`record_key = sheet:period:id`) | USD 200 (`cc1_*`) and USD 500 (`cc2_*`) side by side |
| `rpw_quotes_long.parquet` | one row per record × amount scenario | adds `fee_pct`, the cost-identity residual and quote-level flags |
| `provider_name_map.csv` | one row per raw `firm` string | raw → canonical name |
| `data_quality_flag_summary.csv` | flag × sheet | counts and shares of every flag |
| `manifest.json` | – | raw hash, row/column counts, versions |

## Transformations, in order

1. **Load** (`load.py`). Each data sheet is read with `dtype=object, keep_default_na=False`, so `N/A` and `..` survive as literal strings. The cached formula values are used (Phase 3/3.5 verified 6,690/6,690). The unlabeled POST helper columns AQ–AU are dropped: they hold only derived `code+year` strings for 2025_3Q (audit §8). Row counts are asserted.
2. **Rename** (`config.py`). Columns get snake_case names. Fields that exist in only one schema keep a `_pre` / `_post` suffix and are **not** merged:
   - PRE only: `product`, `sending location`, `note1`, `coverage`, `pick-up method`;
   - POST only: `payment instrument`, `access point`, `Standard Note`, `receiving network coverage`, `pickup location`, `pickup method`.
   `note1` and `Standard Note` are kept separate because their equivalence is unproven (audit).
3. **Stack.** PRE and POST are concatenated, with `sheet` and `source_row` (the Excel row number) recorded for traceability.
4. **Types.**
   - The 15 numeric fields are converted to float. Blanks become NaN; text-stored numbers (2024_3Q–4Q) are parsed. Values that cannot be parsed become NaN and are counted (no such values occur in this release).
   - `date` is parsed from `dd/Mon/yyyy` text, or taken from Excel datetimes (2025). `period` becomes `year`, `quarter` and `period_start`.
   - Leading/trailing whitespace is stripped from text cells.
5. **Normalised categories.** Each one is added next to the raw column:
   - `transparent_norm` = lower-case (`Yes` → `yes`).
   - `speed`: case variants are folded; `N/A` → missing.
   - `firm_type`: `Post Office` → `Post office`. `provider_type` groups it into Bank / Money transfer operator / Post office / Mobile operator / Non-bank FI / Credit union / Mixed (any combined type).
   - `*_income_harmonised`: `High income: OECD` and `High income: nonOECD` → `High income`; `Lower income` → `Low income`. The latter is **inferred** and flagged by `flag_income_label_inferred`. `..` is kept as a token.
   - `corridor_key = source_code + destination_code`. The raw `corridor` is kept, and its 95 `XKX` rows are flagged.
   - `firm`: canonical provider name (next section).
   - `payout_method_group`: one of cash / bank account / mobile wallet / home delivery / atm / card / multiple, taken from PRE `pick-up method` or POST `pickup method`. This is an assumption-bearing mapping. PRE blanks stay missing because they were not collected.
   - `access_has_digital` / `access_digital_only`: whether the access channel includes / consists only of `On-line`, `Internet` or a mobile phone. These come from PRE `sending location` or POST `access point`, and PRE `Not available` → missing. Use them only for 2013_3Q onward.
6. **Provider normalisation** (`providers.py`). Whitespace and case are folded. Then explicit aliases are applied: `Transferwise` → `Wise` (a documented rebrand), and `Taptap Send` → `TapTap Send`. The canonical spelling is the most frequent variant. Raw names stay in `firm_raw`. No fuzzy matching is used: different legal entities are never merged without evidence.
7. **Flags** (`flags.py`). All flags are booleans, so a flag can be added to any filter.

| Flag | Meaning | Source finding |
|---|---|---|
| `flag_fx_undisclosed_by_flag` | `transparent = no` | Legend |
| `flag_note_says_not_transparent` | note text says "not transparent" / "non-transparent" | audit M3 (282 POST `yes` rows) |
| `flag_note_zero_margin_disclaimer` | note says the 0% margin "does NOT necessarily mean" no FX cost | workbook notes |
| `fx_margin_disclosed` | `transparent = yes` **and** no not-transparent note | M3 |
| `transparency_coding_era` | stable (≤2020_4Q) / transition (2021_1Q–2022_1Q) / post-transition | M3 |
| `flag_interbank_rate_placeholder`, `flag_applied_rate_placeholder` | rate equals 0 or 1 | M1 |
| `flag_corridor_mismatch` | raw corridor ≠ source+destination (KSV/XKX) | audit |
| `flag_lcu_code_differs_cc1_cc2` | the two quotes use different currency codes | m5 |
| `flag_numeric_stored_as_text` | POST 2024_3Q–4Q | audit |
| `flag_date_outside_period`, `flag_date_unparsed` | collection date is outside its period quarter / not parsable | m4 |
| `flag_access_not_collected`, `flag_pickup_not_collected` | PRE attribute not collected | M2 |
| `flag_income_label_inferred` | `Lower income` present | m3 |
| `flag_duplicate_except_id`, `flag_duplicate_surplus`, `dup_group_size` | identical to another record except `id`; surplus = every copy after the first | M4 |
| `flag_cost_identity_fail` / `_untestable` | \|total − (fee/amount×100 + margin)\| > 0.01 pp / cannot be computed | cost audit |
| `flag_fee_omitted_from_total` | a non-zero fee, but total = margin | m6 |
| `flag_denomination_nonstandard` | denomination ≠ 200/500 | audit |
| `flag_total_cost_missing`, `flag_negative_fx_margin`, `flag_negative_total_cost`, `flag_extreme_total_cost` (>50%) | self-explanatory | audit |
| `flag_zero_margin_undisclosed` | margin = 0 on a row whose margin is not disclosed | transparency audit |

8. **Analysis eligibility (quote level).** Eligibility is defined only by flags; nothing is removed.
   - `cost_analysis_eligible`: total cost is present, the denomination is standard, the row is not a duplicate surplus copy, and the cost identity is testable and holds within 0.01 pp.
   - `complete_cost_eligible = cost_analysis_eligible & fx_margin_disclosed`: the default population for cost comparisons. It covers 90.6% of PRE quotes and 97.8% of POST quotes.

## Fields that must not be used as levels

`applied_fx_rate` and `interbank_fx_rate` are quoted in an **unrecorded pay-out currency** whose orientation changes over time (audit M1). The pipeline keeps them but derives nothing from them. Use the unit-free `fx_margin_pct` and `total_cost_pct` instead.
