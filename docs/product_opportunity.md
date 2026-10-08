# Product Opportunity Assessment

The evidence comes from `docs/eda_findings.md` (findings F1–F9). Throughout, **demonstrated** means shown by the RPW survey data, and **hypothesis** means a customer need or behaviour that the dataset cannot observe. No customer interviews, internal metrics or market shares were used, and none are implied.

## Problem space (demonstrated)

1. **Prices for the same corridor vary widely.**
   - Across corridors, the median gap between the typical quote and the low end (10th percentile) is 2.22 pp.
   - In 87.6% of corridors at least one surveyed quote is at or below 3%, yet only 15.5% of corridors have a median at or below 3% (F2).
2. **A large share of the cost sits in the FX margin, which is the hardest part to see.**
   - The FX margin makes up about 31% of the mean total and exceeds the fee in a third of quotes.
   - "No-fee" quotes still carry a mean margin of about 1.85% (F4).
   - The source flags and notes show that FX costs are sometimes not disclosed at all (F7).
3. **Fixed fees penalise small transfers.** USD 200 costs about 1.4 pp more than USD 500 at the median, and that gap comes almost entirely from fees (F3).
4. **Digital access is associated with lower prices** (F6, not causal), and some corridors have no surveyed low-cost or digital option (F9).

## Competing hypotheses

| | H1 — All-in cost clarity | H2 — Small-transfer pricing | H3 — Underserved-corridor entry | H4 — Digital switching for cash senders |
|---|---|---|---|---|
| **Idea** | Before paying, show the sender the full cost: fee + FX margin versus the mid-market rate, as one number in both currencies. Benchmark it against the survey range for that corridor. | A plan or scheduled-transfer bundle that spreads fixed fees for people who send small amounts often. | Prioritise launching low-cost payout in corridors with no surveyed quote ≤5% or no digital option. | Help agent/branch senders move to a digital channel. |
| **User problem** | The cheapest-looking offer ("no fee") may not be the cheapest, and senders cannot compare like with like. | Small, frequent senders pay the highest percentage. | Some corridors lack affordable options. | Physical-channel quotes are costlier. |
| **Evidence strength** | **Strong** for dispersion and the FX share (F2, F4, F7; 348 corridors). The *need* for clarity is a hypothesis. | **Strong** for the fee effect (F3). Sending frequency is **not observable**. | **Moderate**: only 12–43 corridors qualify, and only surveyed corridors appear. | **Moderate/weak**: an association confounded by provider and payout method (F6). |
| **Potential impact** | Applies in every corridor; it addresses the 31% of cost that is least visible. | Large for frequent senders, but the size of that segment is unknown. | High per corridor, narrow overall. | Uncertain: depends on why senders use cash. |
| **Fit with international payments** | Core: a payments provider that is transparent about price can show it as a differentiator. | Good, but it changes the pricing model. | Good, but it is a network/licensing decision, not a product feature. | Good. |
| **Technical feasibility** | High: the fee and the rate are already known at quote time, and the mid-market reference is a market-data feed. | Medium: needs a pricing engine and scheduling. | Low/medium: needs payout partners and local licences. | Medium. |
| **Regulatory / compliance** | Mostly favourable: aligns with total-cost disclosure rules, e.g. the EU Cross-Border Payments Regulation and the US Remittance Transfer Rule. Benchmark claims must be accurate and not misleading. | Subscription pricing must stay compliant with disclosure rules. | Licensing, AML/CFT and sanctions exposure (e.g. some flagged corridors are in sanctioned or high-risk markets). | KYC and digital onboarding for the newly digital users. |
| **Key risks** | A clearer price may not change behaviour; competitor benchmarks go stale; survey quotes are not live prices. | Cannibalises revenue; demand is unproven. | High cost; small surveyed sample. | The reason for using cash may be structural (unbanked recipients). |

## Choice: H1 — All-in cost clarity with a corridor benchmark

Why H1 beats the alternatives:
- **Broadest and strongest evidence.** Dispersion (F2) and the FX share (F4) appear across hundreds of corridors and in the fixed-composition panel. H2 depends on an unobservable frequency segment, and H3/H4 rest on smaller or confounded evidence.
- **Feasible as an MVP.** Fee and rate are already known at quote time, so no new pricing model, licences or partners are needed.
- **It works with the others.** Clarity is a precondition for H2 and H4: a sender has to see the cost before a plan or a channel switch looks worthwhile.

**Still a hypothesis (must be validated):** that senders misjudge total cost; that they value a corridor benchmark; that clearer pricing changes completion, trust or retention. The dataset shows *price structure*, not *sender behaviour*.
