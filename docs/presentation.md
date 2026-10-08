---
marp: true
title: True Cost — remittance cost clarity
paginate: true
---

# True Cost
### Making the real cost of small international transfers visible

Independent PM portfolio case study · World Bank Remittance Prices Worldwide (2011–2025 Q3)
*Not affiliated with Wise or the World Bank*

---

## The question

Where in the cost of sending money abroad is there a **product** problem worth solving?

- Data: 253,960 survey records, 507,920 price quotes (USD 200 and USD 500)
- Raw data unchanged and hash-verified; audited documentation; 27 quality flags; tests

---

## Costs are falling — but slowly

- Median USD 200 quote: **6.00% → 4.13%** (2016 Q2 → 2025 Q3)
- The same decline appears on a fixed panel of 1,679 corridor × provider pairs (6.50% → 4.33%)
- Still above the **3% SDG target**

![w:900](../outputs/charts/01_cost_trend_cc1.png)

---

## Insight 1 — the same corridor, very different prices

- **87.6%** of corridors have a surveyed quote ≤3%
- Only **15.5%** have a *median* ≤3%
- Typical quote vs low end (10th percentile): **2.22 pp** median gap

---

## Insight 2 — the hidden part of the price

- The FX margin is **~31%** of the mean cost and exceeds the fee in **1 in 3** quotes
- "No fee" quotes still carry a **1.85%** mean FX margin
- Fixed fees: USD 200 median **4.50%** vs USD 500 median **3.13%**

![w:900](../outputs/charts/03_fee_vs_fx_composition.png)

---

## Four hypotheses → one bet

| | Evidence | Feasibility | Selected |
|---|---|---|---|
| H1 All-in cost clarity | Strong | High | ✔ |
| H2 Small-transfer pricing | Strong fee effect, unknown segment | Medium | |
| H3 Underserved corridors | Moderate (12–43 corridors) | Low | |
| H4 Digital switching | Confounded | Medium | |

---

## The proposal: True Cost

One all-in number · fee + FX margin as amounts · recipient gets · survey benchmark · amount hint

![w:520](../outputs/prototype/desktop.png)

---

## How we would know it works

- **North Star:** informed completions ÷ quotes shown
- **A/B test** in 3–5 corridors, randomised by user, ≥4–6 weeks
- **Guardrails:** revenue per transfer, quote abandonment, latency, complaints
- **Discovery first:** 8–12 sender interviews and a comprehension test

---

## Honest limits

- Survey quotes, not transactions: no volumes, no behaviour
- The need for clarity is a **hypothesis**
- Transparency coding breaks around 2021; FX-rate levels are unusable
- Next: flow-weighted analysis (KNOMAD), interviews, usability tests
