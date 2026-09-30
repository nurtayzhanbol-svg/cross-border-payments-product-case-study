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

## Licensing and the "Restricted Data" clause (checked in Phase 3, 2026-09-30)

**Question.** The workbook's Terms of Use say that some data may be restricted by third parties, as listed on a separate "Terms of use: Restricted Data" page. Does any restriction apply to the data in `rpw_dataset_2011_2025_q3.xlsx`?

**Official sources checked**

| Source | What it says |
|---|---|
| Workbook hyperlinks (`http://go.worldbank.org/C09SUA7BK0`, `.../OJC02YMLA0`, `.../R6942GMMH0`) | These legacy short links did not resolve from this environment (DNS/connection failure), so they could not be followed directly. |
| RPW data-download page, https://remittanceprices.worldbank.org/data-download | Repeats the same Terms of Use summary as the workbook: data may be copied, distributed, adapted, displayed or included in other products, commercially or not, subject to attribution, no implied endorsement, and the Restricted Data check. It names no RPW-specific restriction. |
| World Bank "Restricted Data" page, https://data.worldbank.org/restricted-data | "Some datasets and indicators are provided by third parties … Where applicable, these conditions are included in the dataset or indicator metadata, and as such the conditions are no longer presented on this page. This page is provided for legacy purposes only." The page no longer contains a list. |
| World Bank Data Catalog entry for RPW, https://datacatalog.worldbank.org/search/dataset/0037898/remittance-prices-worldwide | "Data Access and Licensing: This dataset is classified as **Public** under the Access to Information Classification Policy. Users inside and outside the Bank can access this dataset." No third-party restriction or separate licence condition is shown in the retrieved metadata. |

**Conclusion (with its limits).**
- The official "Restricted Data" list no longer exists. The World Bank now puts third-party conditions in each dataset's metadata.
- The RPW metadata reviewed classifies the dataset as Public and shows **no third-party restriction**.
- The RPW Terms of Use (attribution, no implied endorsement, no warranty) apply.
- On this evidence, no specific restriction was found for the RPW data in this workbook, and committing and redistributing it with attribution is consistent with the stated terms.
- This is not a legal opinion. The individual metadata pages for the four RPW sub-resources in the Data Catalog, and the legacy short-link targets, could not be fully retrieved. If certainty is needed (e.g. for commercial reuse), confirm with the contact named in the workbook, paymentsystems@worldbank.org, or data@worldbank.org (named in the Data Catalog).

**Note on data vintage.** The download page says data "from 2011 to Q1 2025" are available in Excel. The provided file contains periods up to `2025_3Q`. So the provided file is newer than the vintage that page describes, or the page text is out of date. The file's provenance cannot be confirmed beyond what the file itself contains.
