# Findings — Customers, ARR & synthesis

Owner: Person D · Branch: `main` · Last updated: 2026-11-21

<!-- Add a finding as soon as you have it. Copy this block for each one. Newest at the top. -->

## F7. Loyalty buys a 6-month spending bump that fades; repairs go with spending that stays higher for over a year; no sign the website lifted members
- **Method:** linear regression (event study) on 457,780 customer-months (14,080 customers, Pilates recruits excluded). Monthly repeat spend is explained by dummies for months before/after joining loyalty and before/after the first repair, plus a dummy for every calendar month (absorbs the competitor, season, holiday sales, website, new manager) and every customer (compares each customer with themselves). Standard errors clustered by customer.
- **Loyalty, extra $ per month vs own normal:** 6–4 months before +12 · 3–1 before −20 · joining month +102 · **1–3 after +36 · 4–6 after +42 · 7–12 after +5 · 13+ after −14**. A short bump, gone within a year and slightly below where members started.
- **Repairs:** 6–4 before +46 · 3–1 before +31 · first-repair month +197 · **1–3 after +93 · 4–6 after +88 · 7–12 after +69 · 13+ after +59**. Users were already spending more beforehand (self-selection), but spending rose further and stayed up.
- **Website (Nov 2025) vs new manager:** long-standing members (joined before Nov 2024) spent **$19 a month less** after Nov 2025 (95% range −$23 to −$15), while the same test a year earlier (placebo, Nov 2024) gave +$8. **No evidence the website raised members' spending.** The new manager can't be separated from other store-wide changes.
- **Why there's no dollar-by-dollar waterfall:** a single "after joining" effect × exposure credited loyalty and repairs with more than the whole $1.15M recovery and gave the website −$2M (its placebo was also negative). An average can't describe an effect that rises then fades, so it isn't reported.
- **Evidence:** `analysis/d_customers_arr/d6_attribution.ipynb`, steps 2–3. **Chart:** `results/d_customers_arr/d6_event_study.png`
- **Confidence / caveats:** medium. Customer and month dummies remove fixed differences and store-wide events, but joining coincides with a purchase (people dip, then join during a big buy), and repair users were already rising. The *shape* is robust; exact dollar sizes are not causal.
- **So what for the recommendation:** expanding perks buys temporary spending, not lasting loyalty, which supports "redesign before expanding". Repairs go with a lasting lift, consistent with keeping them.

## F6. The recovery is fewer customers shopping more often (decomposition)
- **Claim:** Repeat revenue, year before the competitor (Mar 2023 – Feb 2024) vs the last 12 months (Nov 2025 – Oct 2026): **+6%** in total = **active repeat customers −20% + purchase visits per customer +28% + spend per visit −3%** (log %, the parts add up exactly). Every age band 25+ grew through **more frequent visits** (+26% to +37%) while spending a bit less per visit (−5% to −11%). **18–24s lost half their repeat customers** (−73 log % ≈ −52%), which visit frequency (+14%) couldn't offset: −$549K.
- **Evidence:** `analysis/d_customers_arr/d6_attribution.ipynb`, step 1. 12-month windows, so seasonality and holiday sales cancel. Purchase visits only (repair-only trips bring in $0 and didn't exist before Apr 2025).
- **Chart:** `results/d_customers_arr/d6_decomposition.png`
- **Confidence / caveats:** high (it's arithmetic). It says *how* revenue recovered, not *why*; F7 addresses why.
- **So what for the recommendation:** growth depends on a shrinking base visiting more often. Winning back customers (especially 18–24s) matters more than perks that raise spend per visit.

## F5. Churn model (scikit-learn): repairs still cut churn after controlling for everything, but by 5–9 points, not 51
- **Method:** snapshot at 30 Apr 2026. Features use only data up to then: visits, purchase visits, spend, points redeemed, returns, days since last purchase, tenure, membership, tier, repair use, age band, channel, area and interests. Label: no visit in the next 180 days. 6,129 customers active in the prior year (42% churned). Logistic regression and gradient-boosted trees, trained on 75% and tested on 25%.
- **Accuracy:** test AUC **0.84** (both models), so the model ranks who will churn well. Removing repair use barely changes AUC (0.842), because visits and recency already carry most of the signal.
- **Repair effect after controls:** odds ratio **0.51** (repair users' churn odds are half a similar non-user's). In percentage points, switching repair use off for repair users raises their predicted churn by **5.3 pts (boosted trees) to 8.6 pts (logistic)**, vs a raw gap of 37 pts. The purchase-visits-only label gives the same result (4.9–8.4 pts), so pickup trips aren't creating it.
- **Forecast, ARR at risk if repairs close (section 5, supersedes an earlier rough estimate of $151K–$247K):** scored per customer at 31 Oct 2026, each repair user's churn with vs without repairs, times their own ARR, plus next year's ~1,118 new repair users; 40 bootstrap refits per model.

  | Model | Churn rise | ARR at risk | Profit at risk (57% margin) | Net effect of closing vs $134K cost |
  |---|---|---|---|---|
  | Logistic regression | 8.1 pts | $350K | $201K (90% range $160K–$256K) | closing **loses** ~$67K/yr |
  | Gradient-boosted trees | 5.3 pts | $134K | $77K ($50K–$103K) | closing **saves** ~$57K/yr |

  **Repairs roughly break even financially.** The two models agree repairs reduce churn, but land on opposite sides of the $134K cost. The trees model finds the effect concentrated in lighter, lower-ARR users, so less ARR is at stake. Either way, C-2's 25/50/100% scenarios ($366K–$1.47M) overstate the risk.
- **Loyalty:** membership has **no retention effect** once engagement is controlled (odds ratio 0.99). Silver/Gold: 1.04. Redeeming more points goes with *higher* churn (1.34× per SD), consistent with customers cashing out before leaving.
- **At risk now:** applied to Oct 2026 data, **1,864 customers** have a 60%+ predicted churn risk, holding **$649K of ARR (9.7%)**. Only 14.5% of them use repairs.
- **Evidence:** `analysis/d_customers_arr/d3_churn_model.ipynb`
- **Chart:** `results/d_customers_arr/d3_churn_odds.png`
- **Confidence / caveats:** medium. Still observational: it controls for what we can measure, not for unmeasured loyalty to the brand. 180-day churn after one snapshot is a different measure from C-1's, so the comparison with C-2 is approximate.
- **So what for the recommendation:** scrapping repairs is **not** the clear saving leadership expects: at best ~$57K a year (under 1% of revenue), at worst a ~$67K loss, while risking customers who hold 77% of ARR, with no cannibalization (C F4). Keep repairs, but make them pay clearly: faster turnaround (C F2) and lower cost per repair. Loyalty membership doesn't keep customers. Use the at-risk list for targeted win-back offers.
- **Handed to D?** yes (own stream)

## F4. Recommendation: keep repairs, don't expand loyalty as it stands (reconciled with B, C and F5)
- **Claim:** Leadership's plan (expand loyalty, scrap repairs) rests on "loyalty drove the recovery". The evidence says revenue came back from **fewer, older customers spending more** (D-1 F2, A F4/F9), and campaigns didn't keep new customers (D-2 F3). **Loyalty (B, matched):** members grew spend $1,110 more than similar non-members in the year after launch, and 55% of that reached profit (the normal margin), but joiners were already the best customers (A F11) and membership has no retention effect after controls (F5). Redeemed points cost **$797K (5.0% of revenue)** since launch and **$413K (5.9%)** in the last 12 months, still rising. *(Corrected: an earlier draft said only ~30–34% of extra member revenue reached profit; the matched comparison doesn't support that.)*
- **Repairs (C + F5):** repair users churn 15% vs 66% for matched non-users still buying (C F1). After controls the effect is 5–9 pts, so closing repairs nets between **+$57K and −$67K a year**: roughly break-even, not the saving leadership expects. No outerwear cannibalization (C F4). Over-20-day turnaround goes with 24% churn vs 11–13% (C F2).
- **Answer:** keep free repairs with a 20-day turnaround target. Don't expand loyalty as it stands; redesign it to reward visits and retention and cap the share of a purchase payable in points. Judge campaigns on 12-month retention. Win back 18–24s on undercut staples (leggings).
- **Evidence:** `summary.py` sections 5, 6 and 8; `analysis/b_loyalty/b_loyalty.py`.
- **Confidence / caveats:** medium. Members and repair users both self-select; the matched comparisons and the churn model reduce this but don't remove it.
- **So what for the recommendation:** this is the recommendation. Confirm at the 2:00 check-in.
- **Handed to D?** yes (own stream)

## F3. The Pilates campaign brought short-term shoppers, not long-term customers (Q7)
- **Claim:** Among customers who signed up in the same weeks (Jan 6 – Mar 31, 2025), only **52%** of the 360 Pilates-campaign customers came back within a year, vs **81%** from other channels. **47%** never made a second visit (vs 17%), and **64%** made their last visit during the campaign itself (vs 23%). By month 12, 5% visit in a given month vs 22%. They're now **90% churned** (vs 60%). In their first year they spent **$368** each (vs $842) and made **$226** profit (vs $496). Today they contribute **$53K of ARR** ($148 per customer vs $591).
- **Who they were:** similar ages (57% aged 18–34 vs 53%), all Pilates-interested, fewer loyalty members (56% vs 72%). 40% of their spend went on Pilates products (vs 11%). They came for the campaign's Pilates offer and didn't move into the rest of the range.
- **Evidence:** `analysis/d_customers_arr/d2_pilates.ipynb`, sections 1–5.
- **Chart:** `results/d_customers_arr/d2_pilates_retention.png` (slide 9)
- **Confidence / caveats:** high. Same signup weeks, so season and store conditions match. The data has no campaign cost, so this is value delivered, not ROI. Comparison customers chose to come in on their own, which naturally makes them a more engaged group.
- **So what for the recommendation:** acquisition campaigns aren't what drives ARR. Retaining existing customers is. Future campaigns should be judged on 6- and 12-month retention, not sign-ups (a KPI for slide 10). This also supports the case for keeping retention programs like repairs, pending C.
- **Handed to D?** yes (own stream)

## F2. The recovery is bigger spend from fewer customers, not customers coming back
- **Claim:** Compared with the same months in the year before the competitor (Mar 2023 – Feb 2024), repeat revenue went −12% (year 1) → +1% (year 2) → **+10% (Mar–Oct 2026)**. Active repeat customers are still **5% below** pre-competitor levels, while revenue per active repeat customer is **+17%**. Revenue started recovering right after loyalty launched (index 75 in Jun 2024 → 95 by Dec 2024). Customer counts recovered more slowly, and mostly after the Pilates push and free repairs (2025).
- **Evidence:** `analysis/d_customers_arr/d1_arr.ipynb`, section 2 (recovery table and index chart).
- **Chart:** `results/d_customers_arr/d1_recovery_index.png`
- **Confidence / caveats:** medium. Comparing each month with the same calendar month removes seasonality. The rise in spend per customer is consistent with loyalty working, but it's also a mix effect: lower-spending 18–24s left (A-1 F4), and older customers who stayed spend more. B-1's matched comparison is needed before crediting loyalty.
- **So what for the recommendation:** leadership is right that revenue recovered, but it's a narrower customer base spending more. Retention (keeping customers) matters as much as perks (more spend per customer), which is the case for testing repairs (C-1/C-2) before scrapping them.
- **Handed to D?** yes (own stream)

## F1. ARR fell 11% in the year after the competitor opened, then rose 21% to a new high of $6.67M
- **Claim:** ARR (trailing-12-month repeat-customer revenue) was $6.23M when the competitor opened (Mar 2024). It fell every month to a low of **$5.53M in Feb 2025**, then rose to **$6.67M in Oct 2026**: +21% from the low, **+6% above the pre-competitor level ($6.29M in Feb 2024, the last full month before the competitor; same baseline as A F12)**. By age band, ARR from Feb 2024 to Oct 2026 was **18–24 −46%**, 25–34 +9%, 35–44 +29%, 45–54 +20%, 55+ +20%.
- **Evidence:** `analysis/d_customers_arr/d1_arr.ipynb`, sections 1 and 3.
- **Chart:** `results/d_customers_arr/d1_arr_line.png` (slide 3)
- **Confidence / caveats:** high for the numbers. ARR is a 12-month rolling total, so it lags real changes by up to a year. The low in Feb 2025 is when the last pre-competitor month drops out of the window, so don't read the timing of the turn as "the Pilates push or repairs caused it". Use F2 for timing.
- **So what for the recommendation:** sets the headline number. The question for B and C is how much of the $1.14M recovery each program earned.
- **Handed to D?** yes (own stream)

## Open questions
- How much of the rise in spend per customer is loyalty vs the shift to older customers? (B-1)
- ARR split by member / repair user was left out on purpose: "ever a member" is decided after the fact, so that split mostly shows who stayed. B-1 and C-1 handle the comparison properly.

## Decisions needed (also log them in `docs/decisions_log.md`)
-
