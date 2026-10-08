# Appendix: detailed documents and reproduction

## Phase 5 (current)
| Topic | Document |
|---|---|
| Phase 5 report (summary of everything in this phase) | [`phase5_report.md`](phase5_report.md) |
| Decision log (baseline, method changes, product decision) | [`phase5_reframing_decision_log.md`](phase5_reframing_decision_log.md) |
| Corrected analysis A1–A6 (Wise position, zero-fee, panel, sensitivity) | [`phase5_analysis.md`](phase5_analysis.md) |
| Wise public product landscape | [`wise_product_landscape.md`](wise_product_landscape.md) |
| Customer evidence vs hypotheses | [`customer_evidence.md`](customer_evidence.md) |
| Opportunity comparison and decision memo | [`opportunity_assessment_v2.md`](opportunity_assessment_v2.md) |
| PRD | [`prd_v2.md`](prd_v2.md) |
| Measurement and experiment plan | [`measurement_plan_v2.md`](measurement_plan_v2.md) |
| Independent audit that triggered Phase 5 | [`archive/independent_audit_2026-10-08.md`](archive/independent_audit_2026-10-08.md) |

Tables: `outputs/tables/phase5/` (key figures in `phase5_key_figures.json`). Charts: `outputs/charts/p5_01_wise_position_usd200.png`, `p5_02_wise_vs_corridor_median.png`, `p5_03_panel_vs_cross_section.png`.

## Data foundation (Phases 3–4)
[`dataset_notes.md`](dataset_notes.md), [`data_dictionary.md`](data_dictionary.md), [`schema_comparison.md`](schema_comparison.md), [`dataset_quality_report.md`](dataset_quality_report.md), [`phase3_audit_report.md`](phase3_audit_report.md), [`data_dictionary_audit.md`](data_dictionary_audit.md), [`pipeline.md`](pipeline.md), [`eda_findings.md`](eda_findings.md) (original findings with Phase 5 correction note).

## Original True Cost version (superseded, kept for comparison)
[`case_study.md`](case_study.md), [`presentation.md`](presentation.md), [`product_opportunity.md`](product_opportunity.md), [`prd.md`](prd.md), [`measurement_plan.md`](measurement_plan.md), [`end_to_end_work_log.md`](end_to_end_work_log.md). Full snapshot: Git tag `v1-true-cost-case-study` (`git checkout v1-true-cost-case-study`).

## Reproduction
```bash
PYTHONPATH=src python -m rpw.build           # raw workbook -> data/processed/
PYTHONPATH=src python -m rpw.analysis        # original EDA
PYTHONPATH=src python -m rpw.phase5          # Phase 5 analysis
PYTHONPATH=src python -m rpw.prototype_data  # prototype/src/data/wise_position.json
python -m pytest -q
cd prototype && npm ci && npm test && npm run typecheck && npm run build && npm run dev
```

## Prototype
Three views: **Regular Send flow** (11 pilot corridors by default; strict amount validation, two decimals, eligibility cap at USD 500 equivalent, experiment-arm selector, review and confirm steps), **Evidence** (Wise vs corridor medians for all 127 surveyed corridors, filterable), **Break-even** (required retention uplift for a fee discount). Fees are illustrative: implied from Wise's two RPW survey points per corridor (`fixed + variable × amount`, in the sending currency) with no FX margin. Not live, official or endorsed Wise prices.
