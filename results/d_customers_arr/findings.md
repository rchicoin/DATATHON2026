# Findings — Customers, ARR & synthesis

Owner: Person D · Branch: `main` · Last updated: 2026-11-21

<!-- Add a finding as soon as you have it. Copy this block for each one. Newest at the top. -->

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
