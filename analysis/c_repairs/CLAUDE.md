# Stream C — Free repair program

## Questions (4-hour scope; full method in `docs/who_answers_what.md`, Person C)
- **C-1 Must (60 min):** churn of repair users vs matched non-users (customers active Apr 2024 to Mar 2025 only), and churn by turnaround bucket (Q8). The raw gap (13% vs 77%) is likely mostly selection: report the matched gap.
- **C-2 Must (45 min):** yearly repair cost vs ARR and profit at risk, at 25/50/100% causal share; break-even sentence (Q9). This is our scenario-testing bonus.
- **Should:** outerwear cannibalization; repair-user profile.
- **Cut:** turnaround modelling beyond buckets.
- Slides: 7, 8.

## Tables you use
- `lines`: `repair_cost_amt` (drop-offs only; pickups are $0), R01 outerwear / R02 activewear, and Outerwear category sales.
- `links` (`link_type == "repair"`): Pickup → Drop-off, `days_between` = turnaround. 259 drop-offs were never picked up.
- `customers`: `used_repair`, `n_repair_dropoffs`, `first_repair_date`, `churned`, `arr_12m`.
- `customer_month`: before/after repair-use panels.

## Definitions you rely on (`docs/definitions.md`)
Repair cost (at drop-off, $45 / $18), Churn (180 days), ARR, repairs launch 2025-04-01.

## What you hand to Person D
- Total repair cost vs the ARR and profit retained from repair users.
- Churn of repair users vs comparable non-users, and how turnaround time affects it.
- Evidence for or against outerwear cannibalization.
- A scenario estimate: ARR and retention if the program is shut down.

## Rules
- Load data with `from src.metrics import load`. Take dates and thresholds from `src.config`. Never re-clean.
- Notebooks live here. Write findings to `results/c_repairs/findings.md` as soon as you have them.
- `src/` is frozen for the 4-hour sprint: compute new columns in your own notebook. Only fix a real bug, and tell the team chat first.
- Only touch `analysis/<this stream>/`, `results/<this stream>/` and your section of `summary.py`; commit to `main` with `git pull --rebase && git push`.
