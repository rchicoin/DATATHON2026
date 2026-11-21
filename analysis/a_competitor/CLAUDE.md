# Stream A — Competitor impact & seasonality

## Questions (4-hour scope; full method in `docs/who_answers_what.md`, Person A)
- **A-1 Must (45 min):** YoY revenue % by age band, competitor date marked. Hardest-hit categories and areas (Q1). Confirms `COMPETITOR_OPEN`.
- **A-2 Must (30 min):** heatmap of category x calendar month; Black Friday / Boxing Week (Q2).
- **Should:** sign-ups and visits per customer by age band, before vs after.
- **Cut:** formal change-point test.
- Slide: 4.

## Tables you use
All of these come from the one joined table (`df = load()`) via the cheat sheet in `SPRINT_CONTEXT.md`. `lines` = `df` itself.
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
- `src/` is frozen for the 4-hour sprint: compute new columns in your own notebook. Only fix a real bug, and tell the team chat first.
- Only touch `analysis/<this stream>/`, `results/<this stream>/` and your section of `summary.py`; commit to `main` with `git pull --rebase && git push`.
