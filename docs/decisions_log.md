# Decisions log

Every choice that changes a number goes here: newest at the bottom, with a date, an owner and a status (`decided` / `open`). If it touches `src/config.py`, link the PR.

| # | Date | Decision | Why | Status | Owner |
|---|---|---|---|---|---|
| 1 | 2026-11-21 | Drop 1,016 exact duplicate sales rows (`keep="first"`) | They are double entries, and the points balance counts each item once | decided | team |
| 2 | 2026-11-21 | Blank tier before 2024-06-01 → `"Pre-loyalty"` | Loyalty didn't exist yet, so these customers weren't "Non-members" | decided | team |
| 3 | 2026-11-21 | Repair cost counted at Drop-off only. Pickup rows cost $0 | The brief says the cost is incurred at drop-off, and unpicked drop-offs still count | decided | team |
| 4 | 2026-11-21 | Link Pickup → Drop-off on transaction_id **and** item_id | A transaction can hold more than one repair item | decided | team |
| 5 | 2026-11-21 | `RETURN_COST_REVERSES = True` (the production cost of a returned item is reversed) | Assume returned items go back to stock. State it on slide 2 | decided (4-hour freeze) | team |
| 6 | 2026-11-21 | Competitor open date = 2024-03-01 | Working estimate. The brief says only "recently". A-1 checks it with the YoY chart; if it differs, A says so on slide 4 (`config.py` stays frozen) | decided (4-hour freeze) | Person A |
| 7 | 2026-11-21 | Profit = Revenue − Production − Repair − Redeemed pts/20 | Given in the brief | decided | team |
| 8 | 2026-11-21 | Repeat visit = a visit after `signup_date`. ARR = trailing-12-month repeat revenue. Churn = no visit in 180 days | Agreed definitions | decided | team |
| 9 | 2026-11-21 | A "visit" is any `transaction_id`, including return-only and repair-only visits (this affects churn and visit counts) | Default in `src/tables.py`. Kept. Stream C also checks churn with purchase visits only, because a pickup trip counts as a visit | decided (4-hour freeze) | Person D |
| 10 | 2026-11-21 | 141 returns with no `original_transaction_id` (Nov 2022) are kept, with `resolved=False` | The original purchase predates the data. Their revenue and cost still count | decided | team |
| 11 | 2026-11-21 | `AS_OF_DATE` = 2026-10-31 (last sales date) for churn and trailing-12-month metrics | Last date in the data | decided | team |
| 12 | 2026-11-21 | Tier label for blank tier before launch: `Pre-loyalty` (`src/`) vs `Pre-program` (Aylin's notebook) | `Pre-loyalty` (the `src/` label) everywhere | decided (4-hour freeze) | team |
| 13 | 2026-11-21 | Repeat customer: a visit after `signup_date` (agreed) vs 2 or more purchase visits (Aylin's notebook) | The agreed definition (visit after `signup_date`), since ARR depends on it | decided (4-hour freeze) | team |
| 14 | 2026-11-21 | 259 unpicked drop-offs: Aylin found they're all from the last weeks of the data, so they're "open", not abandoned. Abandoned = no pickup after 45 days (the longest turnaround is 47) | Affects how Stream C describes them. Cost still counts | decided | Person C |
| 15 | 2026-11-21 | Blank `points_balance_after`: 0 (`src/`) vs left blank (Aylin's notebook) | Keep 0 (`src/`). Doesn't affect profit | decided (4-hour freeze) | team |
| 16 | 2026-11-21 | 4-hour sprint: `src/` frozen, all open decisions closed with defaults, scope cut to must/should per `docs/who_answers_what.md` | Time box. Get to a finished analysis | decided | team |
| 17 | 2026-11-21 | Share ONE joined table (`lululime_clean.csv.gz`) instead of 5 parquet tables. Visits, customers, ARR and churn come from the `SPRINT_CONTEXT.md` cheat sheet (checked to match the old tables exactly) | Simpler for the team | decided | team |
