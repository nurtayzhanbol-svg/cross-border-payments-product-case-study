# Dataset Notes

> **The raw dataset in `data/raw/` must not be modified.** All cleaning or transformation must write to `data/processed/` (or elsewhere) and leave the original file untouched.

## File

| Field | Value |
|---|---|
| Original filename | `rpw_dataset_2011_2025_q3.xlsx` |
| Location in repo | `data/raw/rpw_dataset_2011_2025_q3.xlsx` |
| File format | Microsoft Excel Open XML Workbook (`.xlsx`) |
| File size | 50,780,339 bytes (~48.4 MiB) |
| SHA-256 | `f1d7265b1856d61812c158d3d03fae686dbff58735deabe016a6bfe23482d2a8` |
| Workbook title (file properties) | Remittance Prices Worldwide dataset |
| Workbook last modified (file properties) | 2026-09-10 |
| Date downloaded | Unknown (file provided by project owner on 2026-09-30) |

Verify integrity with: `sha256sum data/raw/rpw_dataset_2011_2025_q3.xlsx`

## Source

| Field | Value |
|---|---|
| Source organization | The World Bank |
| Dataset name | Remittance Prices Worldwide (RPW) |
| Source URL | https://remittanceprices.worldbank.org (as stated in the workbook) |
| Methodology URL | https://remittanceprices.worldbank.org/en/methodology (as stated in the workbook) |
| Contact (per workbook) | paymentsystems@worldbank.org |

## Workbook sheets

| # | Sheet name | Content type (structural) |
|---|---|---|
| 1 | Terms of Use | Text box with terms-of-use summary and links |
| 2 | Methodology | Text box describing World Bank cost-average methodology |
| 3 | Legend | Column definitions |
| 4 | Countries | Country reference table (ISO code, name, region, income group, lending category, G8/G20) |
| 5 | Dataset (up to Q1 2016) | Data table, periods `2011_1Q`–`2016_1Q` |
| 6 | Dataset (from Q2 2016) | Data table, periods `2016_2Q`–`2025_3Q` |

## Terms of use (summary as stated in the workbook)
- Data may be copied, distributed, adapted and included in other products, commercially and non-commercially, subject to limitations.
- Required attribution: "The World Bank, Remittance Prices Worldwide, available at http://remittanceprices.worldbank.org".
- Must not claim or imply World Bank endorsement or use World Bank logos/trademarks.
- Some data may be subject to third-party restrictions ("Terms of use: Restricted Data" list).
- Links in the workbook: http://go.worldbank.org/C09SUA7BK0, http://go.worldbank.org/OJC02YMLA0, http://go.worldbank.org/R6942GMMH0
