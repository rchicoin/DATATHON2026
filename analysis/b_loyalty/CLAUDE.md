# Stream B — Loyalty program

> **DRAFT scope.** `who_answers_what.md` was missing at setup, so this was inferred from the case's guiding questions.
> Replace the *Questions* section with this person's section from `docs/who_answers_what.md`.

## Questions
- Who uses the loyalty program (by demographic and tier)? (Behaviour)
- Does purchase behaviour change when a customer is close to the next tier? (GQ 3)
- How did loyalty affect top-line revenue vs bottom-line profit, net of redeemed points? (GQ 4)
- Are items paid for mostly with points returned more often? (GQ 5)
- What happens to demoted Silver members? Do they keep shopping? (GQ 6)
- Which KPIs show whether loyalty is genuinely working? (GQ 10)

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
- Need a new column or a change to a definition? Open a PR to `src/` (one reviewer) and log it in `docs/decisions_log.md`.
