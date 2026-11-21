# Stream D — Customers, ARR & synthesis

> **DRAFT scope.** `who_answers_what.md` was missing at setup, so this was inferred from the case's guiding questions.
> Replace the *Questions* section with this person's section from `docs/who_answers_what.md`.

## Questions
- Build the company ARR series and attribute changes to the initiatives (competitor, loyalty, Pilates, repairs, website, new manager).
- Did the Pilates campaign attract engaged long-term customers or single-visit shoppers? (GQ 7)
- Churn and retention by segment.
- **Bring A, B and C together** into the strategy recommendation: scrap repairs and expand loyalty? Then own `summary.py` → `summary.ipynb` and the slide storyline.

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
- Need a new column or a change to a definition? Open a PR to `src/` (one reviewer) and log it in `docs/decisions_log.md`.
