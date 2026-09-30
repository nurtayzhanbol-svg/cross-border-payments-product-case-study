# Cross-Border Payments Product Case Study

## Project
An independent Product Management portfolio case study exploring the cross-border payments / remittance domain using public data.

## Primary data source
World Bank — Remittance Prices Worldwide (RPW): https://remittanceprices.worldbank.org

Attribution: "The World Bank, Remittance Prices Worldwide, available at http://remittanceprices.worldbank.org". See [`docs/dataset_notes.md`](docs/dataset_notes.md) for file metadata and terms of use.

## Purpose
The project will investigate cross-border remittance costs using data analysis, then use the findings to develop and evaluate a product hypothesis.

## Current status
**Phase 2 — Dataset and repository setup.**

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

## Disclaimer
This is an independent portfolio project using publicly available data. It is not affiliated with, endorsed by, or based on internal data from Wise or the World Bank.
