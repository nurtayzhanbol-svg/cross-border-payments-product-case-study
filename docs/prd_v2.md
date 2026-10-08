# PRD v2: Regular Send pricing (working name)

**Status:** hypothesis for validation, not a recommendation to launch. Independent portfolio concept; not affiliated with or endorsed by Wise. No Wise internal data was used; every commercial number below is an assumption to be replaced by internal data.

## 1. Target user and jobs to be done
**Primary user:** a person living in a high-income country who sends a similar small amount (≤ ~USD 500 equivalent) to the same family member at least monthly, through a bank-account or wallet payout that Wise already supports.
- *When* I send my monthly support, *I want* the fee to stay small relative to the amount, *so that* more of my money reaches my family.
- *When* I commit to sending every month, *I want* that regularity to be rewarded, *so that* I don't need to shop around each time.
- *When* I set up the payment once, *I want* it to run reliably, *so that* my family gets the money on time.

Not targeted: one-off senders, large-amount senders (already served by volume discounts), recipients needing cash.

## 2. Problem statement
Wise's fixed per-transfer fee makes small remittances relatively expensive. In the 2024–25 RPW survey, Wise's median total cost is 2.65% at USD 200 vs 1.92% at USD 500. It exceeds 3% in 42.5% of its 127 surveyed corridors at USD 200, and is above the corridor median in 34 corridors at USD 200. Wise's public price benefits reward monthly *volume* above £20k/$25k, not *regularity*, so the typical monthly remitter gets no benefit.

## 3. Evidence and assumptions
| Type | Statement | Source |
|---|---|---|
| Observed (market) | Wise position, fee structure (implied fixed ≈ USD 2.23, variable ≈ 1.29%) | `docs/phase5_analysis.md` |
| Observed (customer, external) | Remittances are typically small and monthly; cost competes with speed, trust and payout channel | `docs/customer_evidence.md` |
| Observed (Wise public) | Scheduled transfers exist; volume discounts start at £20k | `docs/wise_product_landscape.md` |
| Assumption | Many Wise remittance senders are regular small senders | Needs Wise telemetry |
| Assumption | Some of them churn to cheaper MTOs in target corridors | Needs churn and exit data |
| Assumption | Scheduled sends cost Wise less per transfer than ad-hoc sends | Needs internal cost data |

## 4. Proposed solution
A **Regular Send** option on Wise's existing scheduled transfers:
- Eligible if: recurring schedule (weekly to monthly), same recipient, each transfer ≤ a cap (e.g. USD 500 equivalent), pilot corridor.
- Price: standard variable fee, **reduced fixed fee** (pilot arms: −50% and −100% of the fixed fee). Mid-market rate as today.
- Shown upfront in the send flow: per-transfer fee, the saving versus a one-off transfer, and the annual saving at the chosen schedule.
- Clear rules: the reduced fee applies to scheduled transfers only; one-off transfers keep the standard price; the cap is visible.

## 5. Core user journey
1. Sender enters amount and recipient (existing flow).
2. If the transfer is eligible, the quote shows: "Send this every month and pay £X less per transfer".
3. Sender chooses frequency and start date (existing scheduling UI), sees the per-transfer and annual cost.
4. Review screen: amount, fee (standard vs Regular Send), rate, recipient gets, schedule, cap.
5. Each scheduled transfer runs with the Regular Send price; the activity list shows the saving.
6. If an amount above the cap or a change of recipient is requested, the standard price applies and the sender is told why.

## 6. MVP scope
- Pilot in 3–5 corridors chosen by the evidence screen: Wise above the RPW median at USD 200 but competitive at USD 500 (the 11 "small-amount-only" corridors), re-checked against current prices.
- Two price arms plus control, randomised by sender.
- Quote, scheduling and review UI changes; eligibility rule; reporting.

## 7. Non-goals
- No change to the FX rate or transparency features (they already exist).
- No cash pickup, no new payout rails.
- No change to one-off or large-amount pricing.
- No subscription fee or membership.

## 8. Alternatives rejected (see `docs/opportunity_assessment_v2.md`)
True Cost (exists), route repricing (business as usual), wallet expansion (partly exists), Platform for banks (exists), cash pickup (largest gap, but not testable cheaply; recorded as the main strategic alternative).

## 9. Unit-economics assumptions (illustrative only)
For a sender of USD 200/month: standard fee ≈ 2.23 + 1.29% × 200 ≈ USD 4.81 (RPW-implied medians, not Wise's tariff). The −50% arm gives up ≈ USD 1.12 per transfer. If C is Wise's unknown variable cost per transfer and R the fee revenue, the arm breaks even when retained transfers rise by at least ΔF / (R − ΔF − C). With C = USD 2.00 (assumption), that is 1.12 / (4.81 − 1.12 − 2.00) ≈ 66%, which is implausible. With C = USD 0.50 it is ≈ 35%. **So a reduced fixed fee only pays off if per-transfer costs of scheduled sends are low or if retention gains are large.** This is the central business risk; the prototype's break-even calculator lets an interviewer change these assumptions.

## 10. Operational and regulatory dependencies
- Price-change notice periods and fee-disclosure rules per market (Wise publishes notice periods of 7–62 days for some price increases).
- Fair treatment: eligibility rules must be clear and non-discriminatory.
- Fraud/AML monitoring for scheduled transfers and amount splitting.
- Treasury/liquidity for predictable flows (possible cost benefit, unverified).

## 11. Risks and mitigations
| Risk | Mitigation |
|---|---|
| Revenue cannibalisation from senders who would stay anyway | Randomised control; net revenue per eligible sender as guardrail; stop thresholds |
| Splitting large transfers to fit the cap | Per-recipient monthly cap; monitor amount distribution |
| Price isn't the switching driver | Interviews before the pilot; exit survey |
| RPW gaps are outdated | Re-check current prices before choosing corridors |
| Competitor prices are promotional | Track competitor prices during the pilot |

## 12. Validation roadmap
1. **Desk check (1 week):** re-run the corridor screen on current public prices.
2. **Internal data (Wise telemetry):** share of senders who are regular small senders; their churn; cost per scheduled transfer.
3. **Discovery:** 8–12 interviews in two pilot corridors; review public app reviews.
4. **Pilot:** randomised pricing test (see `docs/measurement_plan_v2.md`).
5. **Decision:** ship, iterate (different cap or discount) or stop.
