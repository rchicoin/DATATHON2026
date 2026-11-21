# Stream C — Free repair program

> **DRAFT scope.** `who_answers_what.md` was missing at setup, so this was inferred from the case's guiding questions.
> Replace the *Questions* section with this person's section from `docs/who_answers_what.md`.

## Questions
- Who uses the repair program? (Behaviour)
- What is the true cost of repairs vs the value of the customers who use them? (Money)
- Do repairs cannibalize jacket and outerwear sales, as management believes?
- Do repair users churn less? Does turnaround time matter? (GQ 8)
- If repairs shut down tomorrow, what happens to retention and ARR? (GQ 9)

## Tables you use
- `lines`: `repair_cost_amt` (drop-offs only; pickups are $0), R01 outerwear / R02 activewear, and Outerwear category sales.
- `links` (`link_type == "repair"`): Pickup → Drop-off, `days_between` = turnaround. 259 drop-offs were never picked up.
- `customers`: `used_repair`, `n_repair_dropoffs`, `first_repair_date`, `churned`, `arr_12m`.
- `customer_month`: before/after repair-use panels.

## Definitions you rely on (`docs/definitions.md`)
Repair cost (at drop-off, $45 / $18), Churn (180 days), ARR, repairs launch 2025-04-01.

## What you hand to Person D
- Total repair cost vs the ARR and profit retained from repair users.
- Churn of repair users vs comparable non-users, and how turnaround time affects it.
- Evidence for or against outerwear cannibalization.
- A scenario estimate: ARR and retention if the program is shut down.

## Rules
- Load data with `from src.metrics import load`. Take dates and thresholds from `src.config`. Never re-clean.
- Notebooks live here. Write findings to `results/c_repairs/findings.md` as soon as you have them.
- Need a new column or a change to a definition? Open a PR to `src/` (one reviewer) and log it in `docs/decisions_log.md`.
