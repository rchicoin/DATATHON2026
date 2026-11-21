# Findings — Loyalty program

Consolidated on 2026-11-21 from B's first pass (`loyalty_analysis.ipynb`, notes kept below) into `analysis/b_loyalty/b_loyalty.py`, which uses the shared `load()` table. B-2 and B-3 numbers are identical to the first pass. B-1 changed method (see F1). Charts in `results/b_loyalty/`.

## F1. Members grew spend $1,110 more than similar non-members, and 55% of it reached profit, but most of this is selection (Q4)
- **Claim:** Among the 3,798 customers who shopped in both the 12 months before launch (Jun 2023 – May 2024) and the 12 months after, the 2,565 who joined in year 1 grew revenue **$1,110** and profit **$609** more per person than non-members of the same age band and pre-launch spend quartile. That's **55%** of the extra revenue reaching profit, about the store's normal margin (57%), so redemptions don't eat the gain. Every age band shows it (18–24 smallest: +$683 revenue).
- **Points cost:** **$797K since launch (5.0% of revenue)**, $413K in the last 12 months (5.9%). Rising: 2.4% of revenue in Q3 2024 → 5.0% Q1 2025 → 5.5–6.5% in 2026, as balances build up.
- **Evidence:** `analysis/b_loyalty/b_loyalty.py`, B-1.
- **Chart:** `results/b_loyalty/b1_matched_did.png`, `results/b_loyalty/b1_redemption_cost.png`
- **Confidence / caveats:** low that this is caused by loyalty. Joining is a choice made by people who are already shopping more: joiners spent ~3.6× non-joiners before launch (A F11), and D's churn model finds **no retention effect of membership** once engagement is controlled (odds ratio 0.99, D F5). Treat $1,110 as an upper bound. *Replaces the first-pass comparison (below), which used "ever a member" and averaged over different customers in each year.*
- **So what for the recommendation:** loyalty isn't losing money per member, but there's no evidence that it *creates* loyalty, and its cost is growing. Expanding perks raises a cost that's already ~6% of revenue without a proven return.
- **What capping the cost is worth:** bringing points back to the 5%-of-sales target saves about **$62K a year** of profit: $413K redeemed in the last 12 months minus 5% × $7.02M sales ($351K). This is a simple scenario that assumes sales stay the same; it's the "+$62K" bar on the deck's financial-impact slide (`slides/deck_charts.py`, chart 9).

## F2. Purchases paid mostly with points are returned 2.4× as often (Q5)
- **Claim:** Return rate by share of the purchase paid with points: 0%: 9.5% · 1–25%: 10.5% · 26–50%: 9.8% · **>50%: 23.7%** (3,617 purchase visits).
- **Chart:** `results/b_loyalty/b2_return_rate_points.png`
- **Confidence / caveats:** medium. Correlation only; heavy redeemers may be a different kind of shopper. Small group (2% of purchase visits).
- **So what:** cap the share of a purchase payable in points (e.g. 50%).

## F3. Being close to the next tier doesn't change what members spend (Q3)
- **Claim:** Average basket is $156–$164 at every distance to the next tier (0–50 points away: $160; 400+: $156). Each customer's basket relative to their own average is flat too (0.98–1.02).
- **Chart:** `results/b_loyalty/b3_basket_near_tier.png`
- **Confidence / caveats:** medium-high. Tests basket size only, not visit timing.
- **So what:** the tier mechanic doesn't drive extra spend; richer tier perks are unlikely to either.

## Cut
- Q6 (demoted Silver members): tier is only recorded at a visit, so demotion can't be measured cleanly. "Tier retention" is a KPI on slide 10 instead.

---

## First-pass notes (B, before consolidation)

Chart 1: Basket by points-to-next-tier (B-3). The bars are essentially flat, about $155-165 across every bucket. If customers were stretching their spend to hit the next tier, baskets should be higher for people who are close (0-50 points away). They aren't. So tier proximity doesn't drive spending, and the "gamification" mechanic isn't working, at least at the basket level. This is a null result, but a useful one: the tier structure may be costing something without earning anything.

Chart 2: Return rate by share paid with points (B-2). Return rates are about 10% for 0-50% points usage, then jump to about 24% when more than half the purchase is paid with points. That is more than double. Possible explanations:

Customers treat points as "free money" and buy more casually, so more of it goes back.
Wardrobing or return abuse. Points are already spent, so there is little friction.
It is just a correlation (e.g., heavy redeemers are a different type of shopper).

Whichever it is, the heaviest redeemers are the most expensive: they get the discount and generate the most return and processing cost.

Chart 3: Profit per customer, members vs non-members (B-1). Members are far more profitable in absolute terms (about $870 before, about $715 after, versus about $340 and about $160 for non-members). But both groups dropped after launch, and members fell by roughly 18% while non-members fell by more than half. Two cautions:

Members started way ahead, which is likely self-selection: your best customers join, so the gap isn't caused by the program.
Both groups declined, which points to something broader (seasonality, macro, pricing) rather than the program alone. The program's effect is the difference in decline, and that comparison looks favorable to members, but it needs a proper difference-in-differences framing and the redemption cost % subtracted before you can say it paid for itself.

Putting it together for the deck:

Members are better customers, but this is mostly selection, not proof of uplift.
The tier mechanic doesn't visibly raise spend per visit.
Deep points redemption is linked to double the return rate, which is a hidden cost.
Recommendation direction for Person D: cap or tier the share of purchase payable in points, and rethink the tier-proximity incentives rather than expanding them.
## Open questions
-

## Decisions needed (also log them in `docs/decisions_log.md`)
-


