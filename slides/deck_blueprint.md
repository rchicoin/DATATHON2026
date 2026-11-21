# Deck blueprint: Lululime, "Should we scrap repairs and expand loyalty?"

Owner: Aylin (deck) · 2026-11-21 · Numbers reconciled across streams (decisions #20–22 in `docs/decisions_log.md`).
Rule for every content slide: **headline = the takeaway as a sentence**, one main visual, 2–3 supporting numbers, a one-line caveat in the footer. Max 10 content slides (title, thank-you and appendix don't count).

## The one-sentence answer
**Don't proceed as planned.** The recovery came from fewer, older customers spending more, not from loyalty. Free repairs roughly pay for themselves and keep the store's best (Gold) customers. Expanding loyalty perks adds to a cost that's already ~6% of revenue, with no proven retention effect. **Keep repairs (faster), redesign loyalty before expanding it, and spend on winning back 18–24s.**

## Storyline
Situation (1–4) → who is affected (5) → the two programs tested (6–7) → money (8) → what to do (9) → what could go wrong (10).

| # | Headline (draft) | Rubric section | Main visual | Key numbers | Source |
|---|---|---|---|---|---|
| 0 | Title: "Keep what keeps customers" (team names) | — | — | — | — |
| 1 | **Our answer: keep repairs, fix loyalty before expanding it, win back young shoppers** | Problem framing + recommendation preview | 3 boxes: Repairs / Loyalty / Customers, each with a verdict + one number | Repairs: closing nets only +$57K to −$67K/yr · Loyalty: points cost $413K/yr (5.9% of revenue), no retention effect · 18–24 ARR −46% | all |
| 2 | **Leadership credits loyalty for the recovery and wants to cut repairs. We tested both claims against ARR and profit** | Problem framing | Timeline Nov 2022 → Oct 2026: competitor 15 Mar 2024, loyalty Jun 2024, Pilates Jan–Mar 2025, repairs Apr 2025, website Nov 2025, new manager Feb 2026 | 3 hypotheses to test: (1) loyalty drove the recovery, (2) repairs only cost money, (3) repairs cannibalize outerwear. ARR = trailing-12-month repeat revenue. Profit = revenue − production − repair − points/20 | case, `definitions.md` |
| 3 | **One clean table, and three guardrails against false conclusions** | Data & methodology | Left: pipeline (sales → items → customers, left joins, 351K lines → 190K baskets → 14.4K customers). Right: 3 guardrails | Cleaning: 1,016 duplicate rows dropped; blank tier pre-launch = "Pre-loyalty"; repair cost at drop-off only (unpicked still count); pickups/returns linked on transaction + item; points summed per basket; returns reverse cost. Guardrails: **(a) same months year-over-year** (December = 2× a normal month); **(b) matched comparisons** (age band × spend); **(c) churn model + scenarios** for causality | `summary.py` §2, A F6, `decisions_log.md` |
| 4 | **ARR is back at a record $6.67M, but from fewer customers spending more** | Key insight | `results/d_customers_arr/d1_arr_line.png` (events marked). Optional inset: `d1_recovery_index.png` | $6.29M (Feb 2024) → $5.53M low (Feb 2025) → $6.67M (Oct 2026), +6%. Active repeat customers still −5% vs pre-competitor; revenue per customer +17% | D F1, F2 |
| 5 | **The competitor took young shoppers, and new-customer campaigns haven't replaced them** | Customer / behaviour story | Left: `results/a_competitor/a4_arr_change_by_age.png` (or `a1_recovery_index.png`). Right: `results/d_customers_arr/d2_pilates_retention.png` | 18–24 sales −50% from opening day, still ~45% below 2023; 18–24 ARR −46% ($549K); first-time 18–24s halved (420 → 201); leggings −30%. 25+ recovered by visiting 22% more often. Pilates recruits: 52% came back within a year vs 81%; 90% churned; $148 ARR each vs $591 | A F1–F4, F9–F12; D F3 |
| 6 | **Loyalty rewards the customers who were already loyal: it doesn't create new loyalty, and its cost keeps rising** | Key insight (Q3, Q4, Q5) | Main: `results/b_loyalty/b1_redemption_cost.png`. Side: small `b2_return_rate_points.png` + one number for tier proximity | Matched: members +$1,110 revenue / +$609 profit vs similar non-members (**upper bound**: joiners spent 3.6× more before launch). Membership has **no retention effect** after controls (odds ratio 0.99). Points: $797K since launch, 2.4% → ~6% of revenue. >50%-points purchases returned 2.4× as often (24% vs 10%). Baskets flat near the next tier ($156–164) | B F1–F3, D F5, A F11 |
| 7 | **Repairs keep the best customers: users are mostly Gold members and churn far less** | Key insight + behaviour (Q8) | `results/c_repairs/c1_churn_matched.png` (+ small `c1_churn_turnaround.png`) | 64% of active repair users are Gold (vs 8%); ARR $2,456 vs $494. Churn 15% vs 66% for matched non-users; **after controls, repairs cut churn 5–9 pts** (churn model, AUC 0.84). >20-day turnaround: 24% churn vs 11–13%. No cannibalization: repair users' outerwear spend +10%; the outerwear drop came from non-users | C F1, F2, F4, F5; D F5 |
| 8 | **Scrapping repairs saves almost nothing, and the money is in retention, not perks** | Financial impact | **To build:** one bar chart, $K profit per year: repair cost saved $134K vs profit at risk $77K–$201K (net +$57K to −$67K) · points cost $413K/yr · win-back of half the lost 18–24s +$212K profit. Base on `results/d_customers_arr/d3_repair_arr_forecast.png` | Repairs: net effect of closing is within ±$70K (<1% of revenue). Loyalty: each 1 pt of revenue in points ≈ $70K/yr. Young shoppers: worth ~$430 profit each per year | D F5, C F3, B F1, A F12 |
| 9 | **Recommendations and how to measure them** | Recommendations | Table: action → KPI → target | (1) **Keep free repairs**; turnaround ≤ 20 days; KPI: matched churn gap, % repairs > 20 days. (2) **Redesign loyalty before expanding**: reward visits/retention, cap points at 50% of a purchase; KPIs: profit per member vs matched non-members, points ≤ 5% of revenue, tier retention. (3) **Win back 18–24s** with a price-match on leggings/staples; KPI: first-time 18–24s per quarter, 18–24 ARR. (4) **Judge campaigns on 6/12-month retention**, not sign-ups | `summary.py` §8 |
| 10 | **Risks, trade-offs and what to watch** | Risks & trade-offs | 2-column: risk → how we'd see it early | Self-selection (members and repair users choose in): our effects are upper bounds, so run a holdout test before expanding perks. Repair net is near zero: watch repair cost per item and turnaround. Price-matching staples squeezes margin: test in one category first. ARR lags by up to 12 months: track monthly repeat customers too. Website (Nov 2025) and new manager (Feb 2026) overlap the 2026 growth and aren't separated in our data. Q6 (demoted Silver members) not measured: tier is only recorded at a visit | all streams |
| — | Thank you / questions | — | — | — | — |

## Appendix (optional, doesn't count)
A1 seasonality heatmap `a_competitor/a2_seasonality_heatmap.png` (December 194, jackets 49% in Nov–Jan) · A2 holiday-sale size `a2_promo_days.png` · A3 hardest-hit categories/areas `a1_hardest_hit_category_area.png` · A4 C's 25/50/100% what-ifs `c_repairs/c2_cost_vs_profit.png` (label: "what-ifs, not estimates") · A5 churn-model odds ratios `d_customers_arr/d3_churn_odds.png` · A6 tier proximity `b_loyalty/b3_basket_near_tier.png` · A7 matched loyalty by age `b_loyalty/b1_matched_did.png` · A8 cannibalization `c_repairs/c3_cannibalization.png` · A9 data-quality checks (duplicates, unlinked returns, open drop-offs).

## Rubric coverage
| Criterion (pts) | Where we earn it |
|---|---|
| Data quality & structure (10) | Slide 3; appendix A9 |
| Analytical rigor (10) | True profit incl. points, ARR definition (2–4); matched comparisons (6–7); basket grouping |
| Awareness & assumptions (10) | Same-month comparisons, selection caveats on every program slide, slide 10 |
| Customer journey (10) | 5 (acquisition → retention by age, Pilates cohort), 6 (tier proximity), 7 (churn, turnaround) |
| Contextual depth (15) | Competitor timing by day, age split behind the "recovery", repairs = Gold members |
| Utility (15) | 8–9: dollar figures per decision, KPIs with targets |
| Visualization (15) | One chart per slide, headline = takeaway, shared palette (blue/orange) |
| Clarity & flow (15) | Answer first, then evidence, then money, then actions |
| Bonus: advanced (10) | Churn model (logistic + boosted trees, AUC 0.84, bootstrapped forecast), scenario testing, matched diff-in-diff |

## Before building: open items
1. **C's existing slides (`slides/build_c_slides.js`, `c_repairs_slides_7-8.pptx`) still say "net loss $15K–$115K".** Use the reconciled headline: closing nets **+$57K to −$67K a year** (decision #20).
2. **Build the slide 8 financial-impact chart** (none exists yet).
3. **Timeline graphic for slide 2** (can reuse `mark_events` dates from `src/config.py`).
4. Tell Person B their findings were consolidated (`analysis/b_loyalty/b_loyalty.py`); B-1 changed method (decision #21).
5. Regenerate `summary.ipynb` from `summary.py` (new §5 loyalty code) and run it top to bottom.
