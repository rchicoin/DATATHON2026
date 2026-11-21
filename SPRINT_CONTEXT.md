# Sprint context: read this first

**Lululime Datathon, 4-hour sprint (2026-11-21).** One page for everyone on the team, and for any Claude session.
Details: `docs/work_plan.md` (timeline, slides, rubric) and `docs/who_answers_what.md` (method per question).

## The question
Should leadership **scrap free repairs and expand loyalty**? We answer it with **ARR** (trailing-12-month revenue from repeat customers) and **profit** (revenue − production − repair − redeemed points/20).
Deliverables: **at most 10 content slides** and **one notebook** (`summary.py` → `summary.ipynb`).

## Setup (5 min)
```bash
git pull
pip install -r requirements.txt
nbstripout --install
python -c "from src.metrics import load; print(load().shape)"   # (350998, 40)
```

## The data: one joined table
`data/processed/lululime_clean.csv.gz` is **sales + items + customers joined and cleaned**: one row per sales line, 350,998 rows × 40 columns. Excel users can unzip it.
- Each row is one item line in a transaction: a Purchase, Return, Repair Drop-off or Repair Pickup (`row_type`).
- Ready-made columns: `revenue` (qty × price), `production_cost_amt`, `repair_cost_amt` (drop-offs only), `redeemed_dollars` (points/20), `profit`, `is_repeat_visit`, `month`, `is_member`, `interest_*`.
- Load it in Python with `from src.metrics import load; df = load()` (IDs as text, dates parsed).

## Cheat sheet: same definitions for everyone
Copy these instead of writing your own, so every stream gets the same numbers (checked: ARR $6.67M, repair churn 13% vs 77%).
```python
import pandas as pd
from src.metrics import load
from src import config as C
df = load()

# Visits (baskets): one row per transaction
visits = df.groupby("transaction_id").agg(
    customer_id=("customer_id", "first"), date=("date", "first"), month=("month", "first"),
    revenue=("revenue", "sum"), profit=("profit", "sum"),
    redeemed_dollars=("redeemed_dollars", "sum"), is_repeat_visit=("is_repeat_visit", "first"),
).reset_index()

# Customers: one row per customer, with churn and ARR as of 2026-10-31
customers = (df[["customer_id", "signup_date", "age_band", "home_area", "acquisition_channel", "is_member"]]
             .drop_duplicates("customer_id").set_index("customer_id"))
customers["last_visit"] = visits.groupby("customer_id")["date"].max()
customers["churned"] = (C.AS_OF_DATE - customers["last_visit"]).dt.days > C.CHURN_DAYS
since = C.AS_OF_DATE - pd.DateOffset(months=12)
rep = visits[visits["is_repeat_visit"] & (visits["date"] > since)]
customers["arr_12m"] = rep.groupby("customer_id")["revenue"].sum()
customers["arr_12m"] = customers["arr_12m"].fillna(0)
customers["first_repair_date"] = df[df["row_type"] == C.DROPOFF].groupby("customer_id")["date"].min()
customers["used_repair"] = customers["first_repair_date"].notna()

# Company ARR by month (plot from Nov 2023)
arr = visits[visits["is_repeat_visit"]].groupby("month")["revenue"].sum().rolling(12, min_periods=1).sum()

# Repair turnaround: pickup matched to its drop-off on transaction_id + item_id
drop = df[df["row_type"] == C.DROPOFF][["transaction_id", "item_id", "date"]].drop_duplicates(["transaction_id", "item_id"])
pick = df[df["row_type"] == C.PICKUP][["customer_id", "original_transaction_id", "item_id", "date"]]
repairs = pick.merge(drop, left_on=["original_transaction_id", "item_id"],
                     right_on=["transaction_id", "item_id"], suffixes=("_pickup", "_dropoff"))
repairs["turnaround_days"] = (repairs["date_pickup"] - repairs["date_dropoff"]).dt.days
```
Returns link to their purchase the same way: `row_type == "Return"`, matched on `original_transaction_id` + `item_id`.
In the plan docs, `visits`, `customers` and `links` mean the tables built with this cheat sheet.

## Timeline
| Time | What |
|---|---|
| 0:00–0:15 | Setup. D puts the 10 slide titles in the deck |
| 0:15–2:00 | **Must-haves only.** Save charts as PNGs in `results/<stream>/` |
| 2:00–2:10 | **Check-in:** each person reads out headline numbers; agree on the recommendation |
| 2:10–3:00 | Finish must-haves, then should-haves; write `results/<stream>/findings.md` |
| **3:00** | **Analysis freeze.** No new questions |
| 3:00–3:40 | Build your own slides; paste your key cells into your section of `summary.py` |
| 3:40–4:00 | D runs `summary.py` end to end and generates the notebook; one read-through; submit |

## Who does what
| | Must (by 2:00) | Should | Cut | Slides |
|---|---|---|---|---|
| **A** Competitor | A-1 YoY revenue by age band, hardest-hit categories and areas (Q1) · A-2 category × month heatmap (Q2) | Sign-ups and visits per customer by age band | Formal date test | 4 |
| **B** Loyalty | B-1 revenue vs profit, members vs matched non-members, 12 months before vs after launch (Q4) · B-2 return rate by points-share bucket (Q5) | B-3 basket near the next tier (Q3) | Q6 demotion | 5, 6 |
| **C** Repairs | C-1 churn of users vs matched non-users, plus turnaround buckets (Q8) · C-2 repair cost vs ARR at risk at 25/50/100% (Q9) | Outerwear cannibalization; who uses repairs | — | 7, 8 |
| **D** ARR & strategy | Slide skeleton · D-1 ARR line with events · D-2 Pilates retention at 3/6/12 months (Q7) · D-3 KPIs (Q10), recommendation, `summary.py` | — | — | 1, 2, 3, 9, 10 |

5th person: B-3 and C's cannibalization, then deck design from 3:00.

## Slides (one chart + one headline number each)
1 Question and answer · 2 Data, method, assumptions · 3 ARR over time · 4 Competitor and seasonality · 5 Loyalty revenue vs profit · 6 Loyalty behaviour · 7 Repair users churn less? · 8 Cost saved vs ARR at risk (scenarios) · 9 Pilates · 10 Recommendation, KPIs, risks

## Rules for the sprint
1. **`src/` is frozen.** Compute new columns in your own notebook. Only fix a real bug, and tell the chat first.
2. **Only touch your own folders:** `analysis/<stream>/`, `results/<stream>/`, your section of `summary.py`. Commit to `main` with `git pull --rebase && git push`. Push at least at 2:00 and 3:00.
3. Load data with `from src.metrics import load`. Dates and thresholds come from `from src import config as C`. Never hard-code them.
4. Open decisions are **closed** (`docs/decisions_log.md`). Don't reopen them; state the assumption on slide 2.
5. Each must-have has a time box. When you hit it, ship what you have with a caveat. Stuck for more than 10 minutes? Ask, or simplify.

## Traps to avoid
- **Seasonality:** compare year over year (same month last year), not month to month.
- **Repair churn:** raw churn is 13% for users vs 77% for non-users, which is mostly selection. Compare only customers active Apr 2024 to Mar 2025, matched on age band and spend. A pickup trip counts as a visit, so also check churn using purchase visits only.
- **Loyalty:** members choose to join. Compare like with like (age band, pre-launch spend) and say so.
- **ARR** before Nov 2023 has less than 12 months of history, so plot it from Nov 2023.
- Use `quantity × price` (`revenue`), never row counts. Never sum `points_balance_after`.

## Key numbers and dates
Competitor 2024-03-15 (`C.COMPETITOR_OPEN_DAY`; `C.COMPETITOR_OPEN` = 2024-03-01 is the month) · Loyalty 2024-06-01 · Pilates 2025-01-06 to 03-31 (360 customers) · Repairs 2025-04-01 (2,175 users, 5,480 drop-offs; $45 outerwear / $18 activewear at drop-off) · Website 2025-11-17 · New manager 2026-02-02 · Data 2022-11-01 to 2026-10-31 · Churn = no visit in 180 days · Silver 600 / Gold 2,000 points over trailing 365 days.
