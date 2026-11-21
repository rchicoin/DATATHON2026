# Data notes

Facts about the raw data, and how `src/` handles each one. Add new quirks here as you find them.

## Sizes (after cleaning)
| | rows |
|---|---|
| sales (raw) | 352,014 |
| sales (deduped) | 350,998 |
| visits (`transaction_id`) | 190,156 |
| customers | 14,440 (all have at least one sale) |
| items | 38 (incl. R01, R02 repairs) |

Total revenue after dedup: **$26,204,614.30**

## Joins
- sales LEFT JOIN items on `item_id`, then customers on `customer_id`, `validate="many_to_one"`. All keys match 100%.
- All IDs are read as strings.
- Grain = one row per sales line. `quantity` can be 1–4 on Purchases, so always use `quantity × price`, not a row count, for units and revenue.

## Duplicates
- 1,016 exact duplicate rows in sales are double entries (the points balance counts the item once). They are dropped with `drop_duplicates(keep="first")`.

## Blank values are expected
| Column | Blank when | Handling |
|---|---|---|
| `tier_at_purchase` | Every row before 2024-06-01 (loyalty launch), and only then | → `"Pre-loyalty"` (never "Non-member") |
| `points_*` | Pre-launch and Non-members | → 0 |
| `original_transaction_id` | Everything except Returns and Repair Pickups | kept as NA |
| `notes` | optional free text | lowercased, trimmed, whitespace collapsed (`"GIFT"`, `" gift"` → `"gift"`) |
| `age_band`, `home_area` | 276 / 423 customers | → `"Unknown"` |
| `loyalty_join_date` | 7,722 non-members | `is_member = False` |

`interests` (e.g. `"Yoga;Lifestyle"`) is split into `interest_run/yoga/pilates/outdoor/lifestyle` 0/1 columns.

## Row types
| row_type | rows | qty | price | notes |
|---|---|---|---|---|
| Purchase | 323,703 raw | 1–4 | list or discounted | |
| Return | 17,576 raw | −1 | positive (so revenue is negative) | `points_earned` is negative |
| Repair Drop-off | 5,480 deduped | 1 | $0 | cost incurred here |
| Repair Pickup | 5,221 deduped | 1 | $0 | **cost set to 0**. Links to drop-off on `transaction_id` + `item_id` |

- 6,488 transactions mix row types: Purchase + Drop-off (4,128) or Purchase + Pickup (2,360). Visit-level `has_*` flags capture this.
- Repair rows have 0 points earned and redeemed.

## Links (`links` table)
- **Returns → Purchase:** all 17,387 returns with an `original_transaction_id` resolve (matched on transaction_id + item_id). **141 returns have no `original_transaction_id`.** All 141 fall between 2022-11-01 and 2022-11-24, so the original purchase predates the data. `resolved=False` marks them, with a reason.
- **Pickups → Drop-off:** 5,221 / 5,221 resolve.
- **259 drop-offs were never picked up.** All of them were dropped off in the last weeks of the data, so they're most likely still open, not abandoned (the longest turnaround seen is 47 days). Their repair cost still counts.
- 68 drop-offs include 2 items, and a pickup can be split across visits. A repair = one item in one drop-off.

## Customers / dates
- Sales start 2022-11-01, but `signup_date` goes back to 2018-03-01. For the 9,611 customers who signed up on or after 2022-11-01, the first visit in the data equals `signup_date` in 100% of cases.
- Customers who signed up before the data window have no "first visit" in the data, and `first_visit` is just the first one we can see.
- `tier_at_purchase` has mixed types in pandas' default CSV reader. `src/clean.py` reads it as a string.

## Loyalty membership: checked against the data
The organisers' rules (see `definitions.md`, "Loyalty program") hold in the data (sales deduplicated):
| Check | Result |
|---|---|
| `tier_at_purchase` and points blank before 2024-06-01 | 100% of pre-launch rows; never blank after launch |
| Rows after launch but before the customer's `loyalty_join_date` (or never joined) | 24,646 rows, **all** `Non-member`, **no** points earned or redeemed |
| Rows on or after the join date | `Member` 47,103 · `Silver` 42,421 · `Gold` 107,236 · `Non-member` 10 |
| Those 10 `Non-member` rows | All on the join day itself (the customer likely joined at the till after paying). Harmless |
| Join dates | Earliest 2024-06-01; every join date is a day the customer shopped; 2,201 of 6,718 members joined on their very first visit |
