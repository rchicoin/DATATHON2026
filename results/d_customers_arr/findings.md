# Findings — Customers, ARR & synthesis

Owner: Person D · Branch: `main` · Last updated: 2026-11-21

<!-- Add a finding as soon as you have it. Copy this block for each one. Newest at the top. -->

## F4. DRAFT recommendation: keep repairs, fix loyalty's profit before expanding it
- **Claim:** Leadership's plan (expand loyalty, scrap repairs) rests on "loyalty drove the recovery". The evidence so far says revenue came back from **fewer, older customers spending more** (D-1 F2, A F4/F9), and campaigns didn't keep new customers (D-2 F3). Loyalty lifts member revenue, but only **~30–34%** of the extra reaches profit (B early: 25–34 +$232 revenue / +$69 profit; 35–44 +$382 / +$131), vs the store's **57%** margin since launch. Redeemed points cost **$797K (5.0% of revenue)** since launch.
- **Repairs (C, confirmed):** repair users churn 15% vs 66% for matched non-users still buying (C F1). Scrapping saves $134K a year but risks $366K–$1.47M of profit; it only pays off if repairs cause under 9% of the gap (C F3). Over-20-day turnaround goes with 24% churn vs 11–13% (C F2).
- **Draft answer:** keep free repairs with a 20-day turnaround target. Don't expand loyalty as it stands; redesign it to reward visits and retention. Judge campaigns on 12-month retention. Win back 18–24s on undercut staples (leggings).
- **Evidence:** `summary.py` section 8; B's `results/b_loyalty/loyalty_analysis.ipynb` (early, not yet in B's findings).
- **Confidence / caveats:** medium. B's numbers are early and not yet matched on pre-launch spend; the member definition still needs checking. The repairs half rests on C's 25/50/100% scenarios: it holds unless repairs cause under 9% of the churn gap.
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
- **Claim:** ARR (trailing-12-month repeat-customer revenue) was $6.23M when the competitor opened (Mar 2024). It fell every month to a low of **$5.53M in Feb 2025**, then rose to **$6.67M in Oct 2026**: +21% from the low, +7% above the pre-competitor level. By age band, ARR from Feb 2024 to Oct 2026 was **18–24 −46%**, 25–34 +9%, 35–44 +29%, 45–54 +20%, 55+ +20%.
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
