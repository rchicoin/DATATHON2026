# Work plan: 4 hours to a finished analysis

**The question:** Should leadership scrap free repairs and expand loyalty? We answer it with **ARR** and **profit**.
**What we hand in:** at most 10 content slides (`slides/`) and one notebook (`summary.py` → `summary.ipynb`).

The shared tables (`lines`, `visits`, `customers`, `customer_month`, `links`) are **already built and frozen**.
Nobody cleans data in the next 4 hours. Everyone starts analysing at minute 15.

## The story we are building (one sentence per slide)

| # | Slide | Owner | Comes from |
|---|---|---|---|
| 1 | The question and our answer up front | D | everyone |
| 2 | Data and method: cleaning, profit and ARR definitions, assumptions | D | `docs/definitions.md`, `docs/data_notes.md` |
| 3 | ARR over time, with each initiative marked | D | D-1 |
| 4 | The competitor hit young customers; seasonality to control for | A | A-1, A-2 |
| 5 | Loyalty grows revenue, but what does it do to profit? | B | B-1 |
| 6 | Loyalty behaviour: points-funded returns and tier effects | B | B-2 (B-3 if done) |
| 7 | Repair users churn less | C | C-1 |
| 8 | Scrapping repairs saves $X but puts $Y of ARR at risk (scenarios) | C | C-2 |
| 9 | Pilates campaign: engaged customers or one-time visitors? | D | D-2 |
| 10 | Recommendation, KPIs and risks | D | everyone + D-3 |

Every slide has **one chart and one headline number**. If a finding doesn't fit a slide, it goes to the appendix or nowhere.

## Timeline

| Time | Everyone | Output |
|---|---|---|
| **0:00–0:15** | Pull `main`, `pip install -r requirements.txt`, check `load("visits")` works. Read your section in `who_answers_what.md`. D puts the 10 slide titles in the deck with placeholders. | Everyone can load data |
| **0:15–2:00** | **Must-haves only.** Work in `analysis/<stream>/`. Save each chart to `results/<stream>/` as a PNG. | 2 must-have charts per person |
| **2:00–2:10** | **Check-in.** Each person reads out their headline numbers. D writes them into the slides. Agree on the recommendation direction. | Draft answer |
| **2:10–3:00** | Finish any missing must-haves first. Then do should-haves. Write `results/<stream>/findings.md`. | Findings written |
| **3:00** | **Analysis freeze.** No new questions after this. | |
| **3:00–3:40** | Each person builds their own slides (final chart, headline, 2–3 bullets) and pastes their key cells into their section of `summary.py`. D writes slides 1, 2, 10. | Deck + notebook |
| **3:40–4:00** | Run `summary.py` top to bottom, generate `summary.ipynb`, do one read-through of the deck, submit. | Submitted |

**Time rules.** Each must-have has a time box in `who_answers_what.md`. If you hit it, ship what you have with a caveat and move on.
Stuck for more than 10 minutes? Ask in the team chat, or simplify the method.

## Scope

- **Must:** needed for the story. Done by the 2:00 check-in.
- **Should:** makes the story stronger. Only after the must-haves are done.
- **Cut:** not done in 4 hours. Mention it as a limitation or next step on slide 10 if it matters.

The bonus marks (advanced techniques) come from **C-2's scenario test** (low/mid/high churn effect) and **B-1's matched comparison**. No one needs a separate modelling task.

## Process for 4 hours (simplified)

1. **`src/` is frozen.** Need a new column? Compute it in your own notebook. Only fix `src/` for a real bug, and tell the team chat first.
2. **Only touch your own folders**: `analysis/<stream>/`, `results/<stream>/`, and your section of `summary.py`. This means nobody gets merge conflicts, so commit straight to `main`: `git pull --rebase && git push`. Push at least at 2:00 and 3:00.
3. **Open decisions are closed** with the defaults in `decisions_log.md` (#5, 6, 9, 12, 13, 15). Don't reopen them. Write the assumption on slide 2 instead.
4. Run `nbstripout --install` once, so notebook outputs never get committed.
5. Load data only with `from src.metrics import load`, and take dates and thresholds from `src.config`.

## Rubric check (where each mark comes from)

| Rubric line | Pts | Covered by |
|---|---|---|
| Data quality & structure | 10 | `src/` cleaning, slide 2 |
| Analytical rigour (true profit, ARR) | 10 | D-1, B-1, C-2 |
| Awareness & assumptions (causal vs seasonal) | 10 | A-1 year-over-year, matched comparisons in B-1 and C-1, slide 2 |
| Customer journey | 10 | C-1 churn, D-2 retention curve, B-3 tiers |
| Contextual depth | 15 | A-1 competitor, D-2 Pilates |
| Utility | 15 | C-2 bridge, slide 10 KPIs |
| Visualisation + clarity | 30 | one chart + one headline per slide |
| Bonus: advanced techniques | 10 | C-2 scenarios, B-1 matching |
