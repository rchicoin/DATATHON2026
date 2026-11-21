# Stream B — Loyalty program

## Questions (4-hour scope; full method in `docs/who_answers_what.md`, Person B)
- **B-1 Must (60 min):** revenue vs profit change per customer, members vs non-members, matched on age band, 12 months before vs after launch. Redemption cost % of member revenue (Q4).
- **B-2 Must (30 min):** return rate by points-share bucket (Q5).
- **B-3 Should (45 min):** average basket by distance to the next tier (Q3).
- **Cut:** Q6 demoted Silver members (list tier retention as a KPI instead).
- Slides: 5, 6.

## Tables you use
- `visits`: `tier`, `points_earned`, `points_redeemed`, `redeemed_dollars`, `points_balance_after` (never sum it), `profit`.
- `customer_month`: `tier_last_seen` (forward-filled; lapsed members never show a lower tier), `active`, `arr_12m`.
- `links` (`link_type == "return"`): returns joined to the original purchase visit, to get its redeemed $.
- `customers`: `is_member`, `loyalty_join_date`, `max_tier`.

## Definitions you rely on (`docs/definitions.md`)
Profit, Redeemed points ($ = pts/20), tiers (Silver 600 / Gold 2000 over trailing 365 days), Pre-loyalty vs Non-member, `RETURN_COST_REVERSES`.

## What you hand to Person D
- Loyalty's effect on revenue vs profit (the $ cost of redeemed points).
- Member vs non-member ARR and churn, plus the tier dynamics (demotion outcomes).
- A KPI list for the recommendations slide.

## Rules
- Load data with `from src.metrics import load`. Take dates and thresholds from `src.config`. Never re-clean.
- Notebooks live here. Write findings to `results/b_loyalty/findings.md` as soon as you have them.
- `src/` is frozen for the 4-hour sprint: compute new columns in your own notebook. Only fix a real bug, and tell the team chat first.
- Only touch `analysis/<this stream>/`, `results/<this stream>/` and your section of `summary.py`; commit to `main` with `git pull --rebase && git push`.
