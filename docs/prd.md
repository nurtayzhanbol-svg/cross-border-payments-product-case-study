# PRD — "True Cost" transfer breakdown (portfolio concept)

> **Superseded (Phase 5).** This is the original True Cost version, kept for comparison (tag `v1-true-cost-case-study`). The current case study is [`case_study_v2.md`](case_study_v2.md); see [`phase5_reframing_decision_log.md`](phase5_reframing_decision_log.md).

*Independent portfolio concept. Not affiliated with, endorsed by, or based on internal data from Wise or the World Bank.*

## Problem statement

People sending small international transfers cannot easily see what a transfer really costs. Part of the cost is a fixed fee; part is hidden in the exchange rate (the FX margin). Public survey data show:
- the FX margin is about 31% of the mean cost of a USD 200 transfer;
- within the same corridor, the typical quote is ~2.2 pp above the low end (`docs/eda_findings.md`).

We **hypothesise** that senders compare offers mainly by the headline fee and therefore overpay.

## Target user (persona — hypothesis, not research)

**Amina**, 34, a nurse in London who sends about GBP 150–300 to her family in Lagos once or twice a month from her phone.
- She cares about how much her family receives and how fast.
- She is wary of "no fee" claims.
- She has no time to compare exchange rates manually.

Key assumption: such senders exist in meaningful numbers. Validate this through discovery (`docs/measurement_plan.md`).

## Jobs to be done

- When I send money home, I want to know exactly what it costs me and what my family receives, so I can trust I am not overpaying.
- When I see a "no fee" offer, I want to know whether the exchange rate hides a cost, so I can compare fairly.
- When the amount is small, I want to see how fees change with the amount, so I can decide whether to send now or combine transfers.

## Proposed solution

An all-in cost breakdown on the quote screen of a money-transfer app:
1. **One total-cost number**, in the send currency and as a % of the amount. It equals the fee plus the FX margin cost against the mid-market rate.
2. **Breakdown**: fee | FX margin (shown as an amount, not only a rate) | recipient gets.
3. **Corridor context**: where this total sits within the range of public survey quotes for the corridor (World Bank RPW: 10th percentile / median), with the survey quarter and source.
4. **Amount sensitivity**: the cost % at the entered amount and at a larger amount, to make the fixed-fee effect visible.
5. **Plain-language explainers** for "FX margin" and "mid-market rate".

## Core journey

1. Enter the amount and corridor.
2. See the quote: total cost, breakdown and benchmark.
3. Optionally open the explainers.
4. Compare amounts.
5. Review and confirm.
6. Confirmation shows what the recipient gets.

## MVP scope

- The quote screen with the breakdown, the benchmark, the amount comparison and the explainers, for about 5 launch corridors.
- Benchmarks are refreshed quarterly from published RPW data, always labelled with source and quarter.
- States: loading, valid quote, benchmark unavailable, amount below the minimum, rate expired.
- Accessibility: keyboard navigation, screen-reader labels and WCAG AA contrast.

## Explicitly out of scope

- Live competitor price scraping or naming competitors.
- Subscription/bundle pricing (H2).
- New corridors (H3).
- Recommendations to use a different provider.
- Any claim of being "cheapest" (survey benchmarks are not live prices).

## Alternatives considered

- Showing only the FX margin as a rate: rejected, because a rate is harder to grasp than an amount.
- Naming specific competitors: rejected for legal risk and data staleness.
- A separate comparison website: rejected, because it is outside the transfer flow where the decision is made.

## Key assumptions

1. Senders misjudge total cost when it is split between a fee and a rate.
2. A survey-based benchmark is credible to users, even though it is quarterly.
3. Showing the cost more clearly increases trust and completion rather than causing abandonment.
4. The mid-market reference rate is available in real time.

## Risks and trade-offs

| Risk | Mitigation |
|---|---|
| The benchmark makes us look expensive in some corridors | Show it honestly. Treat it as a pricing signal internally. Use guardrail metrics. |
| Stale or unrepresentative survey data | Show the quarter and the sample size; hide the benchmark if the corridor has fewer than 10 quotes. |
| Regulatory accuracy of comparative claims | Legal review; neutral wording ("within the range of surveyed quotes"). |
| Information overload | Total first; breakdown on demand; usability testing. |
