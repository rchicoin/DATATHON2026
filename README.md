# Lululime — Dataverse 2026 Datathon (WiDS x USS)

Data analysis for the Lululime case. Lululime is a Vancouver athleisure store, and a competitor recently opened across the street.
Leadership wants to **expand the loyalty program** and **shut down the free repair program**.
We test that plan against **ARR** (revenue from repeat customers over the trailing 12 months) and **profit**:

> Profit = Revenue − Production cost − Repair cost − Redeemed points (20 pts = $1)

## Repository layout
```
lululime_analysis.ipynb   # main notebook (all code)
data/                     # raw case data: customers.csv, sales.csv, items.csv
clean/                    # cleaned tables written by the notebook (git-ignored)
requirements.txt
```

## How to run
```bash
pip install -r requirements.txt
jupyter notebook lululime_analysis.ipynb
```
Put the three case CSVs in `data/`, then run all cells. The cleaning section writes these tables to `clean/`:

| File | Grain |
|---|---|
| `sales_clean.csv` | one row per line item, with revenue, cost and repair cost per line |
| `transactions.csv` | one row per visit, with profit and points cost |
| `customers_clean.csv` | one row per customer, with lifetime stats and repair / member flags |
| `repairs.csv` | one row per repaired item (drop-off → pickup), with turnaround |
| `items_clean.csv` | product catalogue with margins |

## Status
- [x] 1. Data cleaning & joining
- [ ] 2. Behaviour: competitor impact, seasonality, behaviour near a tier threshold
- [ ] 3. Financials: loyalty's effect on revenue vs. profit, points & returns
- [ ] 4. Segments: Silver demotion, Pilates campaign, repair users & churn
- [ ] 5. Strategy: ARR/profit scenarios, KPIs

## Key cleaning decisions
- Dropped 1,016 exact duplicate sales rows (items scanned twice).
- Rows from before 2024-06-01 get tier `Pre-program`. Non-member points are set to 0.
- `points_redeemed` is summed per transaction. `points_balance_after` is taken once per transaction.
- Returned items are assumed to go back into stock, so their production cost is reversed. A switch in the notebook can write off defective returns instead.
- Repair cost is charged at drop-off. The 259 unpicked repairs are all from October 2026, so they're still open.
