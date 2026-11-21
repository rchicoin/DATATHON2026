# Stream A — Competitor impact & seasonality

> **DRAFT scope.** `who_answers_what.md` was missing at setup, so this was inferred from the case's guiding questions.
> Replace the *Questions* section with this person's section from `docs/who_answers_what.md`.

## Questions
- How did sales change after the competitor opened? Were some demographics (age band, home area, channel) or product categories hit harder? (GQ 1)
- Are there noticeable seasonal patterns, including the Black Friday and Boxing Week discounts? (GQ 2)
- Confirm or replace the **competitor open date** (`COMPETITOR_OPEN`, currently an estimate). This is decision #6.

## Tables you use
- `lines`: category, activity, season, revenue by date. Customer demographics are already joined.
- `visits`: visit counts and revenue over time.
- `customers`: `age_band`, `home_area`, `acquisition_channel`, `interest_*`.
- `metrics.period()` for before/after cuts.

## Definitions you rely on (`docs/definitions.md`)
Revenue, Visit, Key dates (competitor, loyalty launch), Repeat visit.

## What you hand to Person D
- The confirmed competitor date and a baseline: revenue, visits and customers before vs after.
- Which segments and categories were hit hardest, with the size of the effect.
- Seasonality to control for, so D doesn't read a seasonal bump as a program effect.

## Rules
- Load data with `from src.metrics import load`. Take dates and thresholds from `src.config`. Never re-clean.
- Notebooks live here. Write findings to `results/a_competitor/findings.md` as soon as you have them.
- Need a new column or a change to a definition? Open a PR to `src/` (one reviewer) and log it in `docs/decisions_log.md`.
