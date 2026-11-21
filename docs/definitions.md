# Agreed definitions

These values are implemented in `src/config.py`. If you change one there, change it here too and log the change in `decisions_log.md`.

## Money
| Term | Definition | Where |
|---|---|---|
| Revenue | `quantity × unit_price_paid`. Returns are negative (qty −1). Repairs are $0 | `lines.revenue` |
| Production cost | `quantity × production_cost` on Purchase rows. On Return rows it reverses only if `RETURN_COST_REVERSES` (currently **True**, a placeholder) | `lines.production_cost_amt` |
| Repair cost | Item cost on **Drop-off** rows only (R01 outerwear $45, R02 activewear $18). Pickup = $0. Unpicked drop-offs still count | `lines.repair_cost_amt` |
| Redeemed points ($) | `points_redeemed / 20`, summed per `transaction_id` | `visits.redeemed_dollars` |
| **Profit** | **Revenue − Production Costs − Repair Costs − Redeemed Points** | `profit` columns, `metrics.profit()` |

## Customers
| Term | Definition | Where |
|---|---|---|
| Visit | One `transaction_id` (any row type, including return-only and repair-only visits) | `visits` |
| Repeat visit | A visit dated **after** the customer's `signup_date` | `is_repeat_visit` |
| **ARR** | Repeat-customer revenue over the **trailing 12 months** | `customers.arr_12m` (as of 2026-10-31), `customer_month.arr_12m`, `metrics.company_arr()` |
| **Churned** | **No visit in 180 days** (as of `AS_OF_DATE` = 2026-10-31, or as of month end in `customer_month`) | `churned` |
| Member | `loyalty_join_date` is not null | `customers.is_member` |

## Key dates
| Event | Date |
|---|---|
| Sales data starts / ends | 2022-11-01 / 2026-10-31 (`signup_date` goes back to 2018) |
| Competitor opens | **2024-03-15** (confirmed). `C.COMPETITOR_OPEN_DAY` = 2024-03-15; `C.COMPETITOR_OPEN` = 2024-03-01, the month it opened, for monthly analysis (March 2024 is the first competitor month) |
| Loyalty launch | 2024-06-01 |
| Pilates push | 2025-01-06 to 2025-03-31 |
| Free repairs launch | 2025-04-01 |
| Website redesign | 2025-11-17 |
| New store manager | 2026-02-02 |

`metrics.period(dates)` labels each date with the most recent event before it.

## Loyalty program: who is a member, and when
These rules come from the case organisers and are **checked against the data** (see `data_notes.md`):
1. **Before 2024-06-01 (launch):** the program didn't exist. `tier_at_purchase` is blank, and there are no points. `src/` labels these rows `Pre-loyalty` (never "Non-member").
2. **After launch, everyone starts as a `Non-member`.** A customer becomes a member only on their `loyalty_join_date` (in `customers.csv`). From that visit on, their tier is `Member`, `Silver` or `Gold`. Customers join in store: every join date is a day they shopped.
3. **Points are only collected after joining.** Non-member purchases earn no points and can't redeem any (`src/` sets their points to 0).

**Watch out: `is_member` is not "member at the time of this purchase".** It means "joined at some point by Oct 2026", a fixed property of the customer. Someone who joined in 2026 has `is_member = True` on their 2024 purchases too. For anything time-based, use membership **at the visit**:
```python
member_at_visit = df["loyalty_join_date"].notna() & (df["date"] >= df["loyalty_join_date"])
# or, equivalently, from the tier recorded at the visit:
member_at_visit = df["tier_at_purchase"].isin(["Member", "Silver", "Gold"])
```
**Comparing members with non-members:** because joining happens during a visit, everyone who joined was, by definition, still shopping after launch, while many non-members had simply stopped shopping. Compare customers who were **active in both periods**, or the comparison mostly measures "kept shopping vs stopped".

## Loyalty tiers
- Members earn 1 pt/$. Silver earns 1.25 pts/$ and Gold 1.5 pts/$.
- Thresholds: **Silver 600, Gold 2000** points earned over the trailing 365 days, checked at each visit.
- 20 points = $1 off.
- **Organisers' update (2026-11-21): ignore the case's rule that points are redeemed "in groups of 100".** Don't build any check or calculation on it. (In our cleaned data, per-transaction totals happen to be multiples of 100, but single rows aren't, because redemptions are spread across a transaction's rows. See `data_notes.md`.)
- Tier is only recorded at a visit, so a lapsed member never shows a lower tier. `customer_month.tier_last_seen` is forward-filled, so treat it with this in mind.
- Tier labels in order: `Pre-loyalty` < `Non-member` < `Member` < `Silver` < `Gold`.
