# Stream D — Customers, ARR & synthesis

## Questions (4-hour scope; full method in `docs/who_answers_what.md`, Person D)
- **D-0 Must (0:00, 15 min):** 10-slide skeleton from `docs/work_plan.md`.
- **D-1 Must (30 min):** company ARR line from Nov 2023, split by member and repair user, events marked.
- **D-2 Must (45 min):** Pilates (Jan to Mar 2025 signups) vs other channels: retention at 3/6/12 months (Q7).
- **D-3 Must (from 2:10):** KPI table (Q10), recommendation, slides 1/2/3/9/10, and running `summary.py` end to end.

## Tables you use
- `customer_month`: `arr_12m`, `active`, `churned` per month. `metrics.company_arr()`.
- `customers`: `acquisition_channel` (Pilates Campaign), `interest_pilates`, `first_visit`, `n_visits`, `churned`.
- `visits`: `is_repeat_visit`.
- All of `results/*/findings.md`.

## Definitions you rely on (`docs/definitions.md`)
ARR, Repeat visit, Churn, Visit (decision #9 is open and yours), all key dates.

## Inputs & outputs
You receive the handoffs from A, B and C (see their `CLAUDE.md` files). You produce:
- `summary.py` → `summary.ipynb` (the single submitted notebook).
- The deck storyline: problem, data & method, insights, customer story, financial impact, recommendations, risks.

## Rules
- Load data with `from src.metrics import load`. Take dates and thresholds from `src.config`. Never re-clean.
- Notebooks live here. Write findings to `results/d_customers_arr/findings.md` as soon as you have them.
- `src/` is frozen for the 4-hour sprint: compute new columns in your own notebook. Only fix a real bug, and tell the team chat first.
- Only touch `analysis/<this stream>/`, `results/<this stream>/` and your section of `summary.py`; commit to `main` with `git pull --rebase && git push`.
