# Lululime Datathon (Dataverse 2026)

Should Lululime scrap its free repair program and expand loyalty perks? We answer that through the program's effect on **ARR** (revenue from repeat customers over the trailing 12 months) and **profit**.

**Deliverables:** a slide deck with at most 10 content slides (`slides/`) and one Jupyter notebook (`summary.ipynb`, generated from `summary.py`).

## Setup

```bash
git clone <repo-url> && cd lululime-datathon
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
nbstripout --install          # REQUIRED — strips notebook outputs before commit
python -m src.tables          # builds data/processed/*.parquet and runs integrity checks
```

In any notebook:

```python
from src.metrics import load
from src import config as C
visits = load("visits")
```

## Layout

| Path | What |
|---|---|
| `docs/` | Case brief, work plan, who answers what, `definitions.md`, `data_notes.md`, `decisions_log.md` |
| `data/raw/` | The 3 CSVs. **Never edited.** |
| `data/processed/` | Parquet tables built by `src/tables.py` (gitignored, rebuild locally) |
| `src/config.py` | Paths, key dates, thresholds, flags. The single source of truth |
| `src/clean.py` | Loading, cleaning and joins |
| `src/tables.py` | Builds `lines`, `visits`, `customers`, `customer_month`, `links` and runs the checks |
| `src/metrics.py` | `load()` plus shared metric helpers (ARR, churn, profit, event periods) |
| `analysis/<stream>/` | Each person's notebooks. Each folder has a `CLAUDE.md` describing its scope |
| `results/<stream>/findings.md` | Findings, written as soon as they exist |
| `scratch/` | Personal throwaway work (gitignored) |
| `slides/` | Deck assets and exports |
| `summary.py` | Final notebook source (jupytext `# %%` cells) |

Streams: `a_competitor`, `b_loyalty`, `c_repairs`, `d_customers_arr` (Person D brings the results together).

## Shared tables

| Table | Grain | Highlights |
|---|---|---|
| `lines` | one sales line | joined item + customer cols, `revenue`, `production_cost_amt`, `repair_cost_amt`, `redeemed_dollars`, `profit` |
| `visits` | one `transaction_id` | revenue, costs, points, redeemed $, profit, tier, `has_*` row-type flags, `is_repeat_visit` |
| `customers` | one customer | first/last visit, visits, `revenue_12m`, `arr_12m`, repair use, `max_tier`, `churned` |
| `customer_month` | customer × month | revenue, `active`, `tier_last_seen`, `arr_12m`, `churned` (as of month end) |
| `links` | one Return / Pickup line | `original_transaction_id`, `original_date`, `days_between`, `resolved` |

## Cleaning notebook (`analysis/lululime_analysis.ipynb`)

Aylin's first pass at cleaning and joining, which writes CSVs to `analysis/clean/` (gitignored). It follows the same core rules as `src/`. It also adds features that `src/` doesn't have yet: categories for the `notes` text, Black Friday and Boxing Week flags, a repair status (open or abandoned) with turnaround, `pre_window_signup`, and a switch to write off defective returns. These will move into `src/` so every stream gets them. Where her notebook and `src/` disagree, see `docs/decisions_log.md` (#12–15).

## Team rules

1. **One branch per stream** (`a_competitor`, `b_loyalty`, `c_repairs`, `d_customers_arr`). Merge to `main` through a PR.
2. **Changes to `src/` need one reviewer.** Any change to a definition or flag also gets an entry in `docs/decisions_log.md`.
3. **Run `nbstripout --install` after cloning**, so notebook outputs never get committed.
4. **Findings go in `results/<stream>/findings.md` as soon as they exist.** Don't hold them until the end.
5. Load data only through `src/`. Never re-clean in a notebook, and never hard-code a date or threshold.
6. Never edit `data/raw/`.

Note: `data/raw/` holds the competition data (`sales.csv` is about 25 MB). Keep the GitHub repo **private**.
