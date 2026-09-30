# Cross-Border Payments Product Case Study

## Project
An independent Product Management portfolio case study exploring the cross-border payments / remittance domain using public data.

## Primary data source
World Bank — Remittance Prices Worldwide (RPW): https://remittanceprices.worldbank.org

Attribution: "The World Bank, Remittance Prices Worldwide, available at http://remittanceprices.worldbank.org". See [`docs/dataset_notes.md`](docs/dataset_notes.md) for file metadata and terms of use.

## Purpose
The project will investigate cross-border remittance costs using data analysis, then use the findings to develop and evaluate a product hypothesis.

## Current status
**Phase 3 — Dataset understanding** (structure, data dictionary, schema comparison and quality report; no analysis or product work yet). See [`notebooks/01_dataset_understanding.ipynb`](notebooks/01_dataset_understanding.ipynb) and `docs/`.

## Planned workflow
1. Understand the dataset
2. Perform exploratory analysis
3. Define analytical/product questions
4. Identify meaningful patterns
5. Develop product hypotheses
6. Evaluate potential solutions
7. Prototype a selected solution
8. Define success metrics and experiment design
9. Produce the final Product Management case study

## Repository structure
```
data/raw/         Original source data (never modified)
data/processed/   Derived datasets (later phases)
notebooks/        Jupyter notebooks
src/              Reusable Python code
docs/             Project and dataset documentation
outputs/charts/   Generated charts
outputs/tables/   Generated tables
```

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Reproduce Phase 3 (reads the raw workbook read-only, regenerates `outputs/tables/`):
```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/01_dataset_understanding.ipynb
```

## Documentation
- [`docs/dataset_notes.md`](docs/dataset_notes.md) — file metadata, source, terms of use and licensing check
- [`docs/data_dictionary.md`](docs/data_dictionary.md) — field definitions and unit of observation
- [`docs/schema_comparison.md`](docs/schema_comparison.md) — pre- vs post-Q2-2016 schema
- [`docs/dataset_quality_report.md`](docs/dataset_quality_report.md) — structural profile, workbook issues, cost-field validation, harmonization plan

## Disclaimer
This is an independent portfolio project using publicly available data. It is not affiliated with, endorsed by, or based on internal data from Wise or the World Bank.
