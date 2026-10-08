# Customer evidence: what is observed and what is still a hypothesis

Sources accessed **2026-10-08**. No interviews, surveys or telemetry were collected for this project, and none are invented here.

## 1. Observed market evidence (RPW survey; `docs/phase5_analysis.md`)
- Remittance prices remain dispersed: median corridor cost 4.50% at USD 200; the median gap between a corridor's median and its 10th percentile is about 2.1–2.2 pp.
- Fixed fees make small transfers relatively expensive: median 4.50% at USD 200 vs 3.13% at USD 500 for the same records.
- Zero-fee offers are usually cheaper all-in (95% of corridors with both).
- Wise is cheaper than the corridor median in about three-quarters of its surveyed corridors, but is more expensive in 34 corridors at USD 200, and exceeds 3% in 42.5% of its corridors at USD 200 vs 23.6% at USD 500.
- About 43% of offers cheaper than Wise use cash payout.

## 2. Observed customer evidence (external research)

| Evidence | Source | Strength / caveat |
|---|---|---|
| UK migrants: the majority send monthly; 53.8% send cash via an MTO, 26.5% use bank transfers; 41% say speed is crucial; ease of use and security also matter | World Bank, *Migrants' Remittances from the United Kingdom*, n = 602: https://remittanceprices.worldbank.org/sites/default/files/migrants_remittances_uk.pdf | Independent, but older and small |
| US consumers: 30% say they pay no fee "but may be paying exchange-rate costs"; 41% pay a percentage fee averaging 6.2%; 28% a fixed fee averaging $14.80 | PYMNTS & Stellar, n = 2,079 (2021): https://pymnts.com/wp-content/uploads/2021/09/PYMNTS-Cross-Border-Remittances-Report-September-2021.pdf | Commercial sponsor with a crypto agenda |
| Non-digital senders: 29% prefer face-to-face, 19% don't trust digital; 73% are frustrated by re-entering forms as repeat customers; 45% want a full range of channels | Western Union *Global Money Transfer Index* (MEA/APAC, 2023): https://corporate.westernunion-microsites.com/wp-content/uploads/2023/04/Global-Money-Transfer-Index_Middle-East-and-Asia-Pacific-Series.pdf | Vendor-sponsored |
| 53% of US remitters use online banking or wallets; 69% say trust in a new method depends on who offers it | Visa *Money Travels 2026*: https://cdn.business.visa.com/Web/Visa/%7Bff53986e-c3fd-4d1b-9f2e-cae20d6e72f6%7D_Money_Travels_Report_final_2%5b25%5d.pdf | Vendor-sponsored |
| After US disclosure rules, 59% of surveyed consumers recalled fee information and 63% the exchange rate | CFPB *Remittance Rule Assessment Report* (2019): https://files.consumerfinance.gov/f/documents/bcfp_remittance-rule-assessment_report_corrected_2019-03.pdf | Regulator; US only |
| Regulators treat misleading "no fee", "free", promotional-rate and speed claims as potentially deceptive | CFPB Circular 2024-02: https://files.consumerfinance.gov/f/documents/cfpb_circular_2024-02.pdf ; Sendwave consent order (2023): https://files.consumerfinance.gov/f/documents/cfpb-0012-chime-inc-dba-sendwave-consent-order_2023-10.pdf | Regulator; enforcement, not prevalence |

**What external evidence supports.** Remittances are typically small and repeated (often monthly). Cost matters but competes with speed, trust, ease and payout channel. Many senders still use cash-based MTOs. Price claims in remittances attract regulatory scrutiny.

**What it does not support.** That Wise customers churn because of small-transfer fees; how price-sensitive Wise's small senders are; whether recipients in the 34 corridors can receive to a bank account; whether cheaper competitor quotes are promotional.

## 3. Product hypotheses still requiring validation
1. A meaningful share of Wise's remittance senders send small amounts repeatedly to the same recipient (needs Wise telemetry).
2. In corridors where Wise is uncompetitive at small amounts, senders compare and leave for cheaper MTOs (needs funnel and churn data, exit surveys).
3. A lower per-transfer price for committed recurring small sends would raise retained volume enough to cover the revenue given up (needs a pricing experiment and cost data).
4. Recurring scheduled sends have lower servicing/fraud cost per transfer than ad-hoc sends (needs internal cost data).
5. Recipients in target corridors can and will receive to bank or wallet rather than cash (needs recipient research).

Planned discovery (not done): 8–12 interviews with monthly senders in two target corridors; review of public app-store reviews for fee complaints in those corridors; Wise-internal analysis of send frequency by amount band.
