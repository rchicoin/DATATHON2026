# Lululime Datathon — context for Claude

Case: Lululime (Vancouver athleisure store). Should leadership scrap free repairs and expand loyalty? Answer through ARR and profit. Brief: `docs/Lululime_Datathon_Case.pdf`.
Plan: `docs/work_plan.md` and `docs/who_answers_what.md`. Definitions: `docs/definitions.md`. Data quirks: `docs/data_notes.md`. Decisions: `docs/decisions_log.md`.

**Always load data via `src/`, never re-clean in notebooks:** `from src.metrics import load; df = load()`. This is the ONE shared dataset, `data/processed/lululime_clean.csv.gz` (sales+items+customers joined, one row per sales line). Derive visits/customers/ARR/churn/repair links with the cheat sheet in `SPRINT_CONTEXT.md`. Constants and dates come from `src/config.py`, never hard-coded. Rebuild the CSV with `python -m src.tables`.

Cleaning rules (implemented in `src/clean.py` + `src/tables.py`):
- Join sales → items → customers, LEFT, `validate="many_to_one"`, IDs as strings. Grain = one row per sales line.
- Drop 1,016 exact duplicate sales rows (`keep="first"`).
- Blank tier before 2024-06-01 = "Pre-loyalty" (not "Non-member"). Blank points = 0.
- Repair cost is counted at Drop-off only. Pickup rows cost $0. Pickups link to drop-offs on transaction_id + item_id.
- Returns: quantity −1. Cost reversal is controlled by `RETURN_COST_REVERSES` (placeholder).
- Sum `points_redeemed` per transaction. Never sum `points_balance_after`.
- Profit = Revenue − Production − Repair − Redeemed points/20.

**4-hour sprint mode:** read `SPRINT_CONTEXT.md` first (timeline, scope, traps; details in `docs/work_plan.md`): scope per person is in `docs/who_answers_what.md` (must / should / cut). Stay inside it.
`src/` is frozen: compute new columns in the stream's notebook. Only touch `analysis/<stream>/`, `results/<stream>/` and that stream's section of `summary.py`.
Findings go in `results/<stream>/findings.md`. Charts are saved as PNGs in `results/<stream>/`.
