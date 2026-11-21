# Decisions log

Every choice that changes a number goes here: newest at the bottom, with a date, an owner and a status (`decided` / `open`). If it touches `src/config.py`, link the PR.

| # | Date | Decision | Why | Status | Owner |
|---|---|---|---|---|---|
| 1 | 2026-11-21 | Drop 1,016 exact duplicate sales rows (`keep="first"`) | They are double entries, and the points balance counts each item once | decided | team |
| 2 | 2026-11-21 | Blank tier before 2024-06-01 → `"Pre-loyalty"` | Loyalty didn't exist yet, so these customers weren't "Non-members" | decided | team |
| 3 | 2026-11-21 | Repair cost counted at Drop-off only. Pickup rows cost $0 | The brief says the cost is incurred at drop-off, and unpicked drop-offs still count | decided | team |
| 4 | 2026-11-21 | Link Pickup → Drop-off on transaction_id **and** item_id | A transaction can hold more than one repair item | decided | team |
| 5 | 2026-11-21 | `RETURN_COST_REVERSES = True` (the production cost of a returned item is reversed) | Placeholder. Does a returned item go back to stock? | **open** | ? |
| 6 | 2026-11-21 | Competitor open date = 2024-03-01 | Working estimate. The brief says only "recently" | **open** | Person A |
| 7 | 2026-11-21 | Profit = Revenue − Production − Repair − Redeemed pts/20 | Given in the brief | decided | team |
| 8 | 2026-11-21 | Repeat visit = a visit after `signup_date`. ARR = trailing-12-month repeat revenue. Churn = no visit in 180 days | Agreed definitions | decided | team |
| 9 | 2026-11-21 | A "visit" is any `transaction_id`, including return-only and repair-only visits (this affects churn and visit counts) | Default in `src/tables.py`. Revisit if a stream needs purchase-only visits | **open** | Person D |
| 10 | 2026-11-21 | 141 returns with no `original_transaction_id` (Nov 2022) are kept, with `resolved=False` | The original purchase predates the data. Their revenue and cost still count | decided | team |
| 11 | 2026-11-21 | `AS_OF_DATE` = 2026-10-31 (last sales date) for churn and trailing-12-month metrics | Last date in the data | decided | team |
