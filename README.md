# Lululime Datathon (Dataverse 2026)

Should Lululime scrap its free repair program and expand loyalty perks? We answer that through the program's effect on **ARR** (revenue from repeat customers over the trailing 12 months) and **profit**.

**Deliverables:** a slide deck with at most 10 content slides (`slides/`) and one Jupyter notebook (`summary.ipynb`, generated from `summary.py`).

## Setup

```bash
git clone <repo-url> && cd lululime-datathon
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
nbstripout --install          # REQUIRED — strips notebook outputs before commit
python -m src.tables          # rebuilds data/processed/lululime_clean.csv.gz and runs integrity checks
```

In any notebook:

```python
from src.metrics import load
from src import config as C
df = load()   # sales + items + customers joined, one row per sales line
```

## Layout

| Path | What |
|---|---|
| `docs/` | Case brief, work plan, who answers what, `definitions.md`, `data_notes.md`, `decisions_log.md` |
| `data/raw/` | The 3 CSVs. **Never edited.** |
| `data/processed/` | Parquet tables built by `src/tables.py` (gitignored, rebuild locally) |
| `src/config.py` | Paths, key dates, thresholds, flags. The single source of truth |
| `src/clean.py` | Loading, cleaning and joins |
| `src/tables.py` | Builds the joined table, runs the checks, and writes `lululime_clean.csv.gz` |
| `src/metrics.py` | `load()` plus shared metric helpers (ARR, churn, profit, event periods) |
| `analysis/<stream>/` | Each person's notebooks. Each folder has a `CLAUDE.md` describing its scope |
| `results/<stream>/findings.md` | Findings, written as soon as they exist |
| `scratch/` | Personal throwaway work (gitignored) |
| `slides/` | Deck assets and exports |
| `summary.py` | Final notebook source (jupytext `# %%` cells) |

Streams: `a_competitor`, `b_loyalty`, `c_repairs`, `d_customers_arr` (Person D brings the results together).

## Shared data

One file: `data/processed/lululime_clean.csv.gz`. It's sales + items + customers, joined and cleaned, with one row per sales line (350,998 × 40).
Columns include joined item and customer fields, `revenue`, `production_cost_amt`, `repair_cost_amt`, `redeemed_dollars`, `profit`, `is_repeat_visit` and `month`.
Visits, customers, ARR, churn and repair turnaround come from the cheat sheet in `SPRINT_CONTEXT.md`.

## Cleaning history

Aylin's first-pass cleaning notebook was folded into `src/` (differences resolved in `docs/decisions_log.md` #12–15) and removed; it's still in git history.

## Team rules

We are working in a **4-hour sprint**. Timeline and slides are in `docs/work_plan.md`, and each person's scope is in `docs/who_answers_what.md`.

1. **Work only in your own folders** (`analysis/<stream>/`, `results/<stream>/`, your section of `summary.py`) and commit straight to `main` with `git pull --rebase && git push`. Push at least at 2:00 and 3:00.
2. **`src/` is frozen.** Only fix a real bug, and tell the team chat first. Open decisions are closed with defaults (`docs/decisions_log.md`).
3. **Run `nbstripout --install` after cloning**, so notebook outputs never get committed.
4. **Findings go in `results/<stream>/findings.md` as soon as they exist.** Don't hold them until the end.
5. Load data only through `src/`. Never re-clean in a notebook, and never hard-code a date or threshold.
6. Never edit `data/raw/`.

Note: `data/raw/` holds the competition data (`sales.csv` is about 25 MB). Keep the GitHub repo **private**.
