# Findings — Free repair program

Owner: Stream C · Last updated: 2026-11-21

<!-- Newest at the top. -->

## F5. Who uses repairs: the store's best loyalty members (should-have: repair-user profile)
- **Claim:** Among customers with ARR today (2,086 repair users vs 3,152 others), **97% of repair users are loyalty members (vs 76%) and 64% have reached Gold (vs 8%)**. They're a bit older (35+: 51% vs 42%; 18–24: 11% vs 17%), more often Outdoor-interested (32% vs 24%), and come through the same channels. Each holds **$2,456 of ARR vs $494** (5×).
- **Evidence:** `load("customers")`, active customers (`arr_12m > 0`), crosstab of `used_repair` by age band, membership, `max_tier`, channel and interests (added during the cross-stream review, 2026-11-21).
- **Confidence / caveats:** high (descriptive). Doesn't say repairs *made* them Gold.
- **So what for the recommendation:** leadership's two moves collide. Scrapping repairs takes a perk away from exactly the Gold members that expanding loyalty is meant to reward.

## F4. No sign that repairs cannibalize outerwear: the outerwear drop came from customers who never used repairs
- **Claim:** Outerwear revenue did fall after repairs launched, but not because of repairs. Repair users' outerwear spending *rose*. Customers who repaired a jacket cut jacket spending less than customers who repaired only activewear.
- **Evidence:**
  - Store level, 12 months before vs after launch: outerwear −12% ($1.32M → $1.16M) while every other category grew 8–29%. Split by customer: repair users' outerwear +10% ($806K → $890K); never-repair customers' outerwear −48% ($512K → $268K).
  - Customer level, 12 months before vs after first repair: outerwear repairers (n=705) outerwear −8%, everything else +36%. Activewear-only repairers (n=189) outerwear −19%, everything else +22%. Outerwear's share of spend fell in both groups by a similar amount (−6.4 vs −5.5 pts).
  - `analysis/c_repairs/c3_cannibalization.ipynb`, `results/c_repairs/c3_cannibalization.csv`.
- **Chart:** `results/c_repairs/c3_cannibalization.png`
- **Confidence / caveats:** Medium. The comparison group is small (189), and the never-repair group includes lapsing customers, so its −48% partly reflects people leaving. Nothing points towards cannibalization, though: outerwear repairers did no worse than either comparison.
- **So what for the recommendation:** Leadership's second reason for scrapping repairs doesn't hold up. The outerwear decline is store-wide and comes from customers outside the program.
- **Handed to D?** no

## F3. Repairs cost $134K a year and roughly pay for themselves: closing them nets between +$57K and −$67K a year
- **Update (reconciled with D F5, final):** the break-even is a repair effect of 4.6 pts (9% of the 51-pt gap). D's churn model, which controls for visits, spend, recency, tenure, membership and demographics, puts the effect at **5.1–8.6 pts** (10–17% of the gap): around break-even. **Headline number = D's per-customer forecast** (each repair user's own churn change × their own ARR, plus next year's new users): profit at risk **$77K–$201K** vs **$134K** saved, so closing **saves ~$57K (boosted trees) or loses ~$67K (logistic) a year**. Applying the average effect to every user's ARR (the "Churn model" rows of `c2_scenarios.csv`) gives a net loss of $15K–$115K; it's cruder because the trees model finds the effect concentrated in lower-ARR users. The 25/50/100% rows below are what-ifs, and the model says 50% and 100% are too high. `results/c_repairs/c2_scenarios.csv` now has the model rows.
- **Claim:** Repair users hold 77% of company ARR. Losing even a small part of their retention costs more profit than the program costs, but the margin is thin.
- **Evidence:** Last 12 months (Nov 2025 to Oct 2026): repair cost $133,542 (2,384 outerwear + 1,459 activewear drop-offs). Repair users (2,175) hold $5.12M of $6.67M ARR. Margin before repair cost 56%. Churn gap 50.9 pts (F1).

  | Share of gap caused by repairs | ARR lost | Profit lost | Cost saved | Net from scrapping |
  |---|---|---|---|---|
  | 25% | $652K | $366K | $134K | −$233K |
  | 50% | $1.30M | $733K | $134K | −$599K |
  | 100% | $2.61M | $1.47M | $134K | −$1.33M |

  Break-even: 9% (7% with the plain matched gap). `analysis/c_repairs/c2_cost_vs_arr.ipynb`, `results/c_repairs/c2_scenarios.csv`.
- **Chart:** `results/c_repairs/c2_cost_vs_profit.png`
- **Confidence / caveats:** Medium. It's a yearly steady-state estimate: it assumes at-risk customers would lose their whole ARR and churn at the matched non-user rate. Cannibalization was tested separately (F4) and not found. Margin: 56% here (repair users only) vs 57.2% in D F5 (all customers); the difference doesn't change any conclusion.
- **So what for the recommendation:** Keep free repairs, but present them as roughly paying for themselves, not a big win. Because the margin is thin, faster turnaround (F2) and lower cost per repair are what make the program clearly worth it.
- **Handed to D?** no

## F2. Slow repairs go with higher churn: 24% when turnaround is over 20 days vs 11–13% otherwise
- **Claim:** Repair users whose median turnaround (drop-off to pickup) is over 20 days churn about twice as often as users whose repairs come back faster.
- **Evidence:** ≤10 days: 13.5% (n=630) · 11–20 days: 11.2% (n=1,209) · >20 days: 23.6% (n=280). Median turnaround is 13 days, range 5–47. `analysis/c_repairs/c1_churn.ipynb`, `results/c_repairs/c1_churn_turnaround.csv`.
- **Chart:** `results/c_repairs/c1_churn_turnaround.png`
- **Confidence / caveats:** Medium. Not matched. Users in the >20-day bucket made fewer drop-offs (1.8 vs 2.1–2.9), so they are also lighter users of the program.
- **So what for the recommendation:** If repairs stay, a turnaround target (≤20 days) is a cheap KPI that protects retention.
- **Handed to D?** no

## F1. Repair users churn less than similar non-users: about 16 points with fair timing (the naive matched gap of 51 points is inflated)
- **Update (external review, decision #25):** the −51 pt gap is built partly into the definition. "Repair user" = repaired any time up to Oct 2026, and churn is measured in Oct 2026, so the 188 users (11%) whose first repair came after 4 May 2026 can't be churned by definition (user churn rises 14.7% → 16.6% without them). A landmark design (customers buying Apr–Sep 2025; users = repaired by 30 Sep 2025; purchase-visit churn on 31 Oct 2026; matched on age × pre-launch spend × Apr–Sep 2025 visit frequency; 3,478 customers, 833 users) gives: raw −33.8, matched age×spend −25.4, **matched incl. visits −15.8 pts** (16.9% vs 32.7%). Use ~16 pts as the fair matched estimate and D F5's 5–9 pts as the effect of repairs alone; −51 is the naive matched gap. The 25/50/100% what-ifs in F3 are fractions of 51 and stay appendix-only.
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
