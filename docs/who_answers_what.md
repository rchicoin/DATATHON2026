# Who answers what (4-hour version)

Each person has **2 must-haves** (done by the 2:00 check-in), then 1–2 should-haves if time allows. Everything marked **Cut** is out of scope; mention it as a limitation if it matters.
The timeline and slide outline are in `work_plan.md`. Every method below uses only the shared tables and `src.config`.

## Overview

| | Must (by 2:00) | Should (2:10–3:00) | Cut | Slides |
|---|---|---|---|---|
| **A** Competitor & trends | A-1 competitor impact (Q1), A-2 seasonality (Q2) | Sign-ups and visits per customer by age band | Formal change-point test | 4 |
| **B** Loyalty | B-1 revenue vs profit (Q4), B-2 points-funded returns (Q5) | B-3 behaviour near the next tier (Q3) | Q6 demoted Silver members | 5, 6 |
| **C** Repairs | C-1 churn of repair users (Q8), C-2 cost vs ARR at risk with scenarios (Q9) | Outerwear cannibalization; repair-user profile | Turnaround modelling beyond buckets | 7, 8 |
| **D** ARR & strategy | D-0 slide skeleton, D-1 ARR line, D-2 Pilates (Q7) | — | — | 1, 2, 3, 9, 10 + `summary.py` |

With a **5th person**: they take B-3 and C's cannibalization, then own deck design from 3:00.

---

## Person A: Competitor & trends

Shows what happened when the competitor opened, and what normal seasonality looks like, so others don't confuse background trends with program effects.

**A-1. How did sales change after the competitor opened, and who was hit hardest? (Q1) · 45 min · Must**
- Data: `lines` where `row_type == C.PURCHASE`. Use `revenue`, `month`, `age_band`, `home_area`, `category`.
- Method: monthly revenue by age band → year-over-year % change (`pct_change(12)`, which compares each month with the same month a year earlier, so seasonality cancels out). YoY is available from Nov 2023. The month the 18–24 line drops confirms the competitor date (working date March 2024). Then a table: YoY change for Mar–Oct 2024 vs Mar–Oct 2023 by category and by home area, sorted.
- Output: line chart of YoY revenue % by age band with `C.COMPETITOR_OPEN` marked; a table of the 5 hardest-hit categories and areas.

**A-2. Are there seasonal patterns? (Q2) · 30 min · Must**
- Data: `lines` purchases, `category` (or `season`) × calendar month.
- Method: average revenue by calendar month across years. Check whether Outerwear and hoodies peak in Nov–Jan, and note the size of Black Friday and Boxing Week.
- Output: heatmap of category × calendar month (each row scaled to its own average).

**Should:** new sign-ups per month and visits per customer, by age band, before vs after the competitor date.
**Hands over:** the confirmed competitor date (if it's not March 2024, tell the team at the check-in; don't edit `config.py`), the hardest-hit groups, and the message "compare year over year, not month to month".

---

## Person B: Loyalty program

Measures what loyalty really earns and costs.

**B-1. How did loyalty affect revenue vs profit? (Q4) · 60 min · Must**
- Data: `visits` (`revenue`, `profit`, `redeemed_dollars`) + `customers` (`is_member`, `age_band`).
- Method: take customers with at least one visit in the 12 months **before** launch (2023-06-01 to 2024-05-31). For each, revenue and profit in that year vs the 12 months **after** launch (2024-06-01 to 2025-05-31). Compare the change for members vs non-members, within each age band, then average (a simple matched difference-in-differences). Also: redeemed $ as a % of member revenue, by quarter.
- Output: bar chart of change in revenue and in profit per customer, members vs non-members; one line for redemption cost % over time.
- Caveat to state: members choose to join, so they were likely already more engaged. Matching on age band and pre-launch spend reduces this but doesn't remove it.

**B-2. Are items paid mostly with points returned more often? (Q5) · 30 min · Must**
- Data: `visits` with `has_purchase` and `revenue > 0`; `links` where `link_type == "return"` (`original_transaction_id`).
- Method: points share = `redeemed_dollars / revenue` per purchase visit. Buckets 0%, 1–25%, 26–50%, >50%. A visit is "returned" if any return links to it.
- Output: bar chart of return rate by points-share bucket, with the visit count per bucket.

**B-3. Does behaviour change near the next tier? (Q3) · 45 min · Should**
- Data: `visits` for members from `C.LOYALTY_LAUNCH`.
- Method: per customer, trailing-365-day `points_earned` before each visit (rolling `"365D"` sum, shifted by one visit). Distance to the next threshold (`C.SILVER_THRESHOLD`, `C.GOLD_THRESHOLD`). Average basket (`revenue`) by 100-point distance bucket.
- Output: line of average basket by distance to the next tier.

**Cut:** Q6 (demoted Silver members). A tier is only recorded at a visit, so demotion can't be measured cleanly in the time we have. List "tier retention" as a KPI on slide 10 instead.
**Hands to D:** loyalty's net profit effect per member and its redemption cost; whether points-funded purchases get returned more.

---

## Person C: Repair program

Tests management's claim that repairs "only cost money".

**C-1. Do repair users churn less? Does turnaround matter? (Q8) · 60 min · Must**
- Data: `customers` (`used_repair`, `churned`, `age_band`, `first_repair_date`) + `visits` + `links` where `link_type == "repair"` (`days_between` = turnaround).
- Method: **only** customers with a visit in the year before repairs launched (2024-04-01 to 2025-03-31). Compare churn of users vs non-users within age band × pre-period spend quartile, then take the weighted average gap. Turnaround: each user's median `days_between` → buckets ≤10, 11–20, >20 days → churn rate per bucket.
- Watch out: the raw gap is huge and likely mostly selection (13% vs 77% churn): it compares engaged and lapsed customers, and a pickup trip itself counts as a visit. Report the matched gap. As a robustness check, also measure churn using purchase visits only (`visits.has_purchase`).
- Output: bar chart of churn for users vs matched non-users, plus churn by turnaround bucket.

**C-2. What happens to ARR if repairs shut down? (Q9) · 45 min · Must**
- Data: C-1's matched churn gap; `lines.repair_cost_amt`; `customers.arr_12m` for repair users; profit margin from `visits`.
- Method: yearly repair cost = repair cost in the last 12 months (Nov 2025–Oct 2026). ARR at risk = repair users' ARR × churn gap. **Scenario test:** assume 25% / 50% / 100% of the gap is truly caused by repairs. Turn ARR into profit using the margin.
- Output: bridge or bar chart of cost saved vs ARR and profit lost, for each scenario. One sentence: "Scrapping repairs pays off only if less than X% of the churn gap is caused by repairs."

**Should:** cannibalization: Outerwear revenue per customer per month, for users before vs after their first repair, compared with non-users over the same months. Also a quick profile of repair users (age band, home area, interests, `max_tier`).
**Hands to D:** the C-2 bridge and the break-even sentence.

---

## Person D: ARR, Pilates & final strategy

Owns the shared ARR number, the storyline, and the final recommendation.

**D-0. Slide skeleton · 15 min · Must, at 0:00.** Put the 10 slide titles from `work_plan.md` into the deck with placeholders for each owner.

**D-1. ARR over time · 30 min · Must**
- Data: `customer_month` + `metrics.company_arr()`. Plot from Nov 2023 (the first month with a full 12 months of history).
- Method: total ARR by month; split by `customers.is_member` and `customers.used_repair`. Mark `C.EVENTS` as vertical lines.
- Output: an ARR line with the initiatives marked (slide 3; this is the backbone of the story).

**D-2. Did the Pilates campaign bring long-term customers? (Q7) · 45 min · Must**
- Data: `customers` with `signup_date` between `C.PILATES_START` and `C.PILATES_END`; `acquisition_channel == "Pilates Campaign"` (360 customers) vs other channels in the same months. `visits` for their later visits.
- Method: share with a repeat visit within 3, 6 and 12 months after signup; visits and spend in the first 12 months.
- Output: retention curve by channel.

**D-3. KPIs, recommendation and assembly · from 2:10 · Must**
- Pick 4–6 KPIs tied to findings: ARR, repeat-purchase rate, profit per member after redemptions, churn of repair users vs non-users, tier retention, redemption cost % of revenue. Give each a target and how to measure it.
- Write slides 1, 2 and 10. Recommendation = leadership's plan (scrap repairs, expand loyalty) vs alternatives, using B-1 and C-2, with risks.
- Own `summary.py`: everyone pastes their key cells into their section by 3:40; D runs it end to end and generates `summary.ipynb`.
