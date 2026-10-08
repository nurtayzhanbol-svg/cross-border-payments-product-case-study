# Measurement & Validation Plan

> **Superseded (Phase 5).** This is the original True Cost version, kept for comparison (tag `v1-true-cost-case-study`). The current case study is [`case_study_v2.md`](case_study_v2.md); see [`phase5_reframing_decision_log.md`](phase5_reframing_decision_log.md).

## North Star

**Share of quoted transfers where the sender sees the all-in cost and completes the transfer** ("informed completions" ÷ quotes shown). It captures both the clarity goal and the business outcome.

## Supporting KPIs

- Quote → transfer completion rate.
- Breakdown/explainer engagement rate.
- Repeat sending within 60 days.
- Self-reported price understanding: a post-transfer micro-survey ("I understood what this transfer cost", 1–5).
- Fewer support contacts about "unexpected amount received".

## Guardrails

- Average revenue per transfer does not fall beyond an agreed threshold.
- Quote-screen latency stays at or below the current p95.
- Abandonment on the quote screen does not rise significantly.
- No increase in complaints, chargebacks or regulatory flags.
- Accessibility defects stay at 0 critical.

## Adoption funnel

Quote viewed → total cost seen (in viewport ≥1 s) → breakdown opened → explainer opened (optional) → review → transfer completed → repeat transfer.

## Experiment design

- **Type:** randomised A/B test at the user level, in 3–5 corridors. Stratify by corridor and by new vs existing users.
- **Control:** the current quote screen. **Treatment:** the True Cost breakdown + benchmark.
- **Primary metric:** quote → completion rate. Secondary metrics: repeat rate at 60 days and the understanding survey.
- **Sample size:** set it from the baseline completion rate and the minimum detectable effect, e.g. +1 pp with α = 0.05 and power = 0.8. The baseline is unknown here, so the size cannot be computed from public data.
- **Duration:** at least 2 full send cycles (≈4–6 weeks), to cover pay-day patterns.
- **Decision rules:**
  - Ship if the primary metric improves significantly and no guardrail breaches its threshold.
  - Iterate if understanding improves but completion does not change.
  - Stop if abandonment or revenue guardrails breach.
- **Pre-launch:** an A/A test, event QA and a legal review of the benchmark wording.

## What the World Bank dataset can and cannot measure

| Can (descriptive, quarterly) | Cannot (needs product telemetry or research) |
|---|---|
| Corridor price ranges, the FX share of cost, fee vs amount effects, benchmark values | Completion, abandonment, engagement, retention, revenue |
| Changes in survey quotes over time | Whether users understood or valued the breakdown |
| | Actual prices users saw, volumes, customer segments |

## Customer discovery (next steps)

1. 8–12 interviews with small-amount senders in 2–3 corridors. Explore how they compare cost today and how they read "no fee" offers.
2. A five-second / comprehension test on the prototype: can users state the total cost and what the recipient gets?
3. A survey to size frequent small-amount senders (needed for H2).
4. Desk review of total-cost disclosure rules per launch market.
