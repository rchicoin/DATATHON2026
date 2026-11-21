# Findings — Free repair program

Owner: Stream C · Last updated: 2026-11-21

<!-- Newest at the top. -->

## F3. Repairs cost $134K a year; scrapping them pays off only if under 9% of the churn gap is caused by repairs
- **Claim:** Repair users hold 77% of company ARR. Even if repairs explain only a quarter of their lower churn, losing them would cost far more profit than the program costs.
- **Evidence:** Last 12 months (Nov 2025 to Oct 2026): repair cost $133,542 (2,384 outerwear + 1,459 activewear drop-offs). Repair users (2,175) hold $5.12M of $6.67M ARR. Margin before repair cost 56%. Churn gap 50.9 pts (F1).

  | Share of gap caused by repairs | ARR lost | Profit lost | Cost saved | Net from scrapping |
  |---|---|---|---|---|
  | 25% | $652K | $366K | $134K | −$233K |
  | 50% | $1.30M | $733K | $134K | −$599K |
  | 100% | $2.61M | $1.47M | $134K | −$1.33M |

  Break-even: 9% (7% with the plain matched gap). `analysis/c_repairs/c2_cost_vs_arr.ipynb`, `results/c_repairs/c2_scenarios.csv`.
- **Chart:** `results/c_repairs/c2_cost_vs_profit.png`
- **Confidence / caveats:** Medium. It's a yearly steady-state estimate: it assumes at-risk customers would lose their whole ARR and churn at the matched non-user rate. Doesn't count cannibalization (repairs may reduce new outerwear sales; not yet tested). The conclusion holds unless repairs cause almost none of the gap.
- **So what for the recommendation:** Keep free repairs. Scrapping saves $134K but risks $366K–$1.47M in profit.
- **Handed to D?** no

## F2. Slow repairs go with higher churn: 24% when turnaround is over 20 days vs 11–13% otherwise
- **Claim:** Repair users whose median turnaround (drop-off to pickup) is over 20 days churn about twice as often as users whose repairs come back faster.
- **Evidence:** ≤10 days: 13.5% (n=630) · 11–20 days: 11.2% (n=1,209) · >20 days: 23.6% (n=280). Median turnaround is 13 days, range 5–47. `analysis/c_repairs/c1_churn.ipynb`, `results/c_repairs/c1_churn_turnaround.csv`.
- **Chart:** `results/c_repairs/c1_churn_turnaround.png`
- **Confidence / caveats:** Medium. Not matched. Users in the >20-day bucket made fewer drop-offs (1.8 vs 2.1–2.9), so they are also lighter users of the program.
- **So what for the recommendation:** If repairs stay, a turnaround target (≤20 days) is a cheap KPI that protects retention.
- **Handed to D?** no

## F1. Repair users churn 15% vs 66% for similar non-users who were still buying after launch (gap −51 points)
- **Claim:** Among customers active in the year before launch (Apr 2024 to Mar 2025), repair users churn far less than non-users of the same age band and pre-launch spend quartile. The gap shrinks but stays large under every check.
- **Evidence:** (cohort 6,694 customers, 1,702 of them repair users)

  | Comparison | Users | Non-users | Gap |
  |---|---|---|---|
  | Raw | 14.7% | 84.2% | −69.4 pts |
  | Matched (age band × spend quartile) | 14.7% | 81.1% | −66.4 pts |
  | Matched, purchase visits only | 15.2% | 81.2% | −66.0 pts |
  | **Matched, still buying after launch** | **14.8%** | **65.7%** | **−50.9 pts** |
  | Matched, still buying, purchase visits only | 15.1% | 65.7% | −50.6 pts |

  `results/c_repairs/c1_churn_gap.csv`
- **Chart:** `results/c_repairs/c1_churn_matched.png`
- **Confidence / caveats:** Low that the full gap is *caused* by repairs. 56% of non-users in the cohort had already stopped visiting before repairs launched, so the plain matched gap mostly compares active with lapsed customers. Requiring a purchase after launch removes most of that. Counting only purchase visits barely changes anything, so pickup trips are not inflating the gap. Repair users still make far more visits after launch (median 19 purchases vs 0), so some selection remains. C-2 handles this with the 25/50/100% scenarios.
- **So what for the recommendation:** The −50.9-point gap (conservative) is the input to C-2.
- **Handed to D?** no

## Open questions
- Which gap should C-2 use: −50.9 pts (still buying after launch; current choice) or −66.4 pts (plain matched, as the plan describes)?

## Decisions needed (also log them in `docs/decisions_log.md`)
-
