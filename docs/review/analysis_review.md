# Lululime datathon: independent review of the analysis

**Date:** 21 November 2026 · **Scope:** every stream (A competitor, B loyalty, C repairs, D ARR & synthesis), the shared pipeline in `src/`, `summary.py`, the deck blueprint and the slide charts in `slides/charts/`.
**Reproduce every new number in this review:** `python docs/review/review_checks.py` (read-only; uses `src.metrics.load()`).

This review answers three questions:
1. Do our numbers agree with each other and with the data? (Part 2)
2. Are there methodological errors that change what we can claim? (Part 3)
3. Taken together, what do the analyses say leadership should do? (Part 5)

---

## Contents
- [Executive summary](#executive-summary)
- [Part 1. What was checked, and what holds](#part-1-what-was-checked-and-what-holds)
- [Part 2. Discrepancies between numbers](#part-2-discrepancies-between-numbers)
- [Part 3. Methodological issues](#part-3-methodological-issues)
- [Part 4. What is strong and should be defended](#part-4-what-is-strong-and-should-be-defended)
- [Part 5. What the analyses say about the best move](#part-5-what-the-analyses-say-about-the-best-move)
- [Part 6. Fix list by file](#part-6-fix-list-by-file)
- [Appendix A. Output of the review checks](#appendix-a-output-of-the-review-checks)
- [Appendix B. Glossary](#appendix-b-glossary)

---

## Executive summary

**The foundation is solid.** Cleaning, joins, the profit formula and the headline ARR all reproduce exactly: ARR was $6.29M in Feb 2024, fell to a low of $5.53M in Feb 2025 and reached $6.67M in Oct 2026 (+6.0%). `summary.ipynb` runs all 25 code cells without errors. The main storyline holds up under every check I ran: the competitor took young shoppers, the recovery came from older customers, repairs are not a money-saver to cut, and loyalty is not the engine leadership thinks it is.

**But several headline numbers and framings need to change before we present.**

| # | Issue | Type | Severity | Where it shows up | Fix |
|---|---|---|---|---|---|
| D1 | Win-back value of young shoppers is overstated ($212K → about **$155K–$195K**) | Discrepancy | **High**: on slide 8 | A F12, `slides/charts/s8_financial.png`, `slides/deck_charts.py:253` | Use $195K (today's profit per buyer) or show the $155K–$195K range |
| D2 | "Points cost keeps rising as balances build up" isn't true: it has **levelled off at ~6–7%**, driven by tier mix, not balances | Discrepancy | **High**: slide 6 headline | B F1, `summary.py:340`, `summary.py:671`, `summary.py:686`, blueprint slide 6 | "Points are a fixed cost of ~7% of member revenue because two-thirds of member spend is at Gold" |
| D3 | Slide 8 compares three bars measured in different ways (modelled net, mechanical saving, gross upside) | Discrepancy | Medium | `s8_financial.png` | Label all three, or show all as ranges |
| D4 | Repair effect quoted three ways (5.1–8.6 / 5.3–8.6 / 5.3–8.1 pts) | Discrepancy | Low | C F3, D F5 text vs table, `c2_cost_vs_arr.py` | Say "5–9 pts" everywhere |
| D5 | Stale material still in the repo | Discrepancy | Low | B findings first-pass notes, `deck_b1_profit_members.png` | Delete or mark "superseded" |
| D6 | KPI "repair users vs non-users churn, now 15% vs 66%" uses the biased gap | Discrepancy | Medium | `summary.py:686` KPI table, blueprint slide 9 | Track the landmark gap or the model effect instead |
| M1 | C-1's −51 pt churn gap is inflated by how "repair user" is defined; a fairer version gives **−16 pts** | Method | **High**: slide 7 | C F1, `c1_churn.py`, `s7_churn_gap.png` | Lead with the model effect; show −16 pts as the matched upper estimate |
| M2 | D's churn model controls for a channel repairs work through (visits), and its forecast covers one year only | Method | Medium | D F5, `d3_churn_model.py` | State that the bias runs both ways; add the multi-year point |
| M3 | Loyalty is shown as a cost without counting its (upper-bound) return | Method / framing | **High**: slides 1, 6, 8 | Blueprint slides 1, 6; slide 8 chart | Show cost **and** benefit; the claim is "unproven", not "loss-making" |
| M4 | "Membership has no retention effect (odds ratio 0.99)" is weaker evidence than stated | Method | Medium | D F5, B F1, slide 6 | Say "no independent effect detected" |
| M5 | Returns refund the full price without giving points back: about $70K of points value has gone out as refunds | New finding | Medium | Not in any stream | Add to slide 6 / recommendations, flagged as "policy unconfirmed" |
| M6 | Most of the growth above the pre-competitor level came in 2026, after the website and new manager | Method / framing | Medium | D F1–F2, slide 4, slide 10 | Say so explicitly on slide 4; it weakens "loyalty drove the recovery" further |
| M7 | `age_band` is fixed per customer, not age at purchase | Caveat | Low | All of Stream A | One line on slide 3 or 10 |

**Bottom line for leadership:** **don't scrap free repairs, and don't expand loyalty by making it more generous.** Closing repairs saves at most ~$57K a year and every estimate of the repair effect is at or above break-even. Loyalty probably pays for itself but has no proven causal effect and already costs ~7% of member revenue. The biggest profit gap is the 18–24 segment, which neither program reached. Details and nuances are in Part 5.

---

## Part 1. What was checked, and what holds

### 1.1 Pipeline (`src/`)
| Check | Result |
|---|---|
| Join sales → items → customers, LEFT, `validate="many_to_one"`, IDs as strings | Correct (`src/clean.py`, `join`) |
| 1,016 exact duplicates dropped, `keep="first"` | Correct; `src/tables.py` checks that row counts and revenue tie out |
| Blank tier before 2024-06-01 → `Pre-loyalty`; asserts no blank tier after launch | Correct |
| Repair cost counted only on drop-off rows; pickups $0 | Correct, with a check |
| Returns: quantity −1, revenue negative, production cost reversed (`RETURN_COST_REVERSES = True`) | Correct as decided (decision #5) |
| `points_redeemed` summed per transaction; `points_balance_after` never summed (`"first"`) | Correct |
| Profit = Revenue − Production − Repair − Redeemed/20 | Correct (`build_lines`) |
| Repeat visit = date > `signup_date` | Correct as defined; see the note below |
| ARR Feb 2024 / low / Oct 2026 | **$6,293,878 / $5,526,196 (Feb 2025) / $6,672,617** reproduced exactly |

**Note on the ARR definition (no change needed, but worth knowing):** every visit by customers who signed up before Nov 2022 counts as "repeat", and new customers' first visit (which equals `signup_date` in 100% of cases) is excluded. This is a reasonable reading of the case. Just remember that "repeat revenue" ≈ "all revenue except first-ever visits".

### 1.2 Streams: numbers I reproduced
| Claim | Source | Reproduced? |
|---|---|---|
| ARR $6.29M → $6.67M (+6%), 18–24 ARR −$549K (−46%) | A F12, D F1 | ✅ |
| Loyalty matched DiD +$1,110 revenue / +$609 profit, 3,798 customers, 2,565 members | B F1 | ✅ |
| Points $797K since launch; $413K in the last 12 months (5.9%) | B F1 | ✅ |
| Return rate 23.7% for >50%-points purchases vs 9.5% | B F2 | ✅ (and robust; see Part 4) |
| Repair cost last 12 months $133,542; repair users' ARR $5.12M (77%) | C F3 | ✅ |
| Break-even repair effect 4.6 pts | C F3 | ✅ |
| C-1 cohort 6,694 customers, 1,702 repair users, churn 14.7% | C F1 | ✅ |
| Points-cut bar on slide 8: +$62K | `deck_charts.py:247` | ✅ arithmetic ($61,858); the assumption behind it is questioned in D3 |

### 1.3 Cross-stream consistency that is already fine
- C's slides (`slides/build_c_slides.js`) were updated to "+$57K to −$67K" (decision #20). ✅
- ARR baseline is Feb 2024 everywhere (decision #22). ✅
- A F11 ($1,130 vs $310 = 3.6×) matches B F1's "3.6×". ✅
- C F5 profile (2,086 users × $2,456 + 3,152 others × $494 ≈ $6.68M) adds up to company ARR. ✅

---

## Part 2. Discrepancies between numbers

### D1. The young-shopper win-back value is overstated ($212K → about $155K–$195K)
**Where:** A F12 (`results/a_competitor/findings.md`), `a4_recovery_and_value.ipynb` cells 19–23, slide 8 bar (`slides/deck_charts.py:253`, hard-coded `212`), blueprint slide 8.

**What is claimed:** young shoppers now bring "$424K less profit every year", so winning back half of them adds "about $212K of profit a year (and ~$275K of repeat sales)".

**What the data says:**

| | Mar 2023 – Feb 2024 | Nov 2025 – Oct 2026 |
|---|---|---|
| 18–24 revenue | $1,270,206 | $677,758 |
| 18–24 profit | $804,410 | $380,130 |
| Margin | **63.3%** | **56.1%** |
| Points redeemed | $0 | $39,515 |
| Buyers | 1,799 | 887 |

The $424K profit drop combines **two different things**:
1. fewer young shoppers (the thing we want to value), and
2. a lower margin on the young shoppers who stayed, because points didn't exist in the "before" year.

Winning someone back recovers (1) only, at **today's** margin. Three consistent ways to value half of the lost shoppers:

| Method | 50% win-back, profit/yr |
|---|---|
| 912 lost buyers × $429 profit per young buyer today × 50% | **$195K** |
| Lost revenue ($592K) × today's margin (56.1%) × 50% | $166K |
| Lost 18–24 ARR ($549K) × today's margin × 50% | $154K |
| *Published* | *$212K* |

The published pair ($212K profit on $275K of repeat sales) implies a **77% margin**, which is impossible when the store's margin is 55–57%.

**Fix:** use **"about $195K a year"** (it matches A's own "$430 per shopper" rule) or show "$155K–$195K". Still say "before the cost of the offer". The conclusion doesn't change: it is still the largest single lever on slide 8, and still bigger than the repair program's net effect.

### D2. Points cost has levelled off; it is not "rising as balances build up"
**Where:** B F1, `summary.py:340` ("keeps rising"), `summary.py:671` ("~6% of revenue and rising"), `summary.py:686` risk column ("Points cost rises as balances build"), blueprint slide 6 headline ("its cost keeps rising").

**What the data says (by quarter):**

| Quarter | 24Q3 | 24Q4 | 25Q1 | 25Q2 | 25Q3 | 25Q4 | 26Q1 | 26Q2 | 26Q3 | 26Q4* |
|---|---|---|---|---|---|---|---|---|---|---|
| Points **earned**, % of member revenue | 5.5 | 6.2 | 6.6 | 6.7 | 6.7 | 6.8 | 6.9 | 6.9 | 6.9 | 6.9 |
| Points **redeemed**, % of all revenue | 2.4 | 3.9 | 5.0 | 5.8 | 5.4 | 5.3 | 6.2 | 6.5 | 5.7 | 5.5 |
| **Gold** share of member revenue | 4% | 33% | 50% | 55% | 58% | 64% | 69% | 69% | 69% | 68% |

\*Oct 2026 only.

- **Balances are not building up.** Since launch, members earned $923K of points (net of return claw-backs) and redeemed $797K. The outstanding balance is only **$127K**. Members spend their points about as fast as they earn them.
- **The cost rose in the first year because of tier mix.** Gold earns 1.5 pts/$ (7.5% back), and Gold's share of member revenue went from 4% to 69%. The earn rate rose from 5.5% to 6.9% and has been **flat since mid-2025**. Redemption caught up with it and now moves around 5.5–6.5%.
- **Gold is not exclusive.** 69% of member revenue is Gold. The 2,000-point threshold is roughly $1,330–$2,000 of spend a year, which most regular customers clear.

**Fix (slide 6 headline):** *"Loyalty rewards customers who were already loyal, and it now costs a steady ~7% of member revenue because two-thirds of member spend is at Gold."* Remove "keeps rising" and "as balances build" from `summary.py` §5, §8 and the KPI table.

**Why this matters for the decision:** it makes the argument **stronger**, not weaker. The cost is structural (set by the earn rates and tier thresholds), so "expanding loyalty" (richer tiers, higher earn rates) raises it directly. **Each extra 0.25 pts per $ costs about $81K a year** (member revenue in the last 12 months was $6.5M, 93% of all revenue).

### D3. Slide 8 compares three bars that aren't measured the same way
**Where:** `slides/charts/s8_financial.png`, built in `slides/deck_charts.py:245-253`.

| Bar | What it actually is | How it looks |
|---|---|---|
| Close repairs: −$67K to +$57K | **Modelled net** effect, including lost customers | Hatched range (uncertain) |
| Points back to 5% of sales: +$62K | **Mechanical saving.** Assumes customers spend exactly the same with fewer points | Solid green (looks certain) |
| Win back half of 18–24s: +$212K | **Gross upside** before the cost of the offer, and overstated (D1) | Solid green (looks certain) |

The two green bars are the least certain of the three but are drawn as the most certain. B F1's matched result (members +$1,110 revenue) means a points cut could cost some revenue, so +$62K is the best case.

**Fix options:**
- (a) Draw the two green bars as ranges too: points cut "$0–$62K, depending on how members respond"; win-back "$155K–$195K before the cost of the offer".
- (b) Keep them solid but add a footnote under each bar: "best case: assumes no change in spending" and "before the cost of the offer".

Either way, update the win-back value (D1).

### D4. The repair effect is quoted three ways
- C F3 and `c2_cost_vs_arr.py`: **5.15–8.62 pts** (D's April 2026 snapshot, all customers in the model).
- D F5 text: **5.3–8.6 pts**.
- D F5 forecast table: **5.3 (trees) / 8.1 (logistic)** (current repair users scored in Oct 2026).

These are different populations, so none of them is wrong. But a judge who reads both the notebook and the deck will see three ranges. **Use "5–9 pts" on slides** and footnote which population each comes from.

### D5. Stale material is still in the repo
- `results/b_loyalty/findings.md`: the "First-pass notes" still quote **$870 → $715 vs $340 → $160**, which decision #21 replaced. Add a "SUPERSEDED by F1" line or delete them.
- `results/d_customers_arr/deck_b1_profit_members.png`: the unmatched chart that decision #21 replaced. Delete it, or rename it with `_superseded`, so nobody drops it into the deck.
- `SPRINT_CONTEXT.md` quotes raw repair churn as "13% vs 77%" (all customers), while C F1 reports 14.7% vs 84.2% (cohort). Both are correct for their populations. Just never put both on slides.

### D6. A KPI is built on the biased gap
**Where:** `summary.py:686` KPI table and blueprint slide 9: *"Churn of repair users vs similar non-users (now 15% vs 66%)"*.
Because of M1, this KPI would show a big gap even if repairs did nothing. **Track instead:** the landmark gap (repaired in a period vs not, among customers active in that period, matched on age, spend and visit frequency; now −16 pts), and/or the share of repairs with turnaround over 20 days.

---

## Part 3. Methodological issues

### M1. C-1's −51 pt churn gap is mostly built into the definition (High)
**Where:** `analysis/c_repairs/c1_churn.py`, C F1, slide 7 chart `s7_churn_gap.png` ("Similar customers: 51").

**The problem.** "Repair user" means *anyone who used a repair at any time up to 31 Oct 2026*, and churn is measured *on* 31 Oct 2026. That creates three built-in biases:
1. **Customers can't be counted as churned after starting repairs late.** Churn = no visit in 180 days, so anyone whose first repair came after **4 May 2026** cannot be churned by definition. That is **188 of the 1,702** cohort repair users (11%). Without them, user churn rises from 14.7% to 16.6%.
2. **You have to still be around to become a user.** Becoming a repair user requires shopping after April 2025. C's "still buying after launch" filter applies this to non-users too (gap −66 → −51), which helps, but the timing is still uneven: users are defined over 19 months, non-users had the same 19 months to *not* repair.
3. **The most engaged customers both repair and stay.** Matching on pre-launch spend doesn't capture how often people visit *after* launch.

**A fairer version (landmark design), done in this review.** Take customers active before launch who **bought something between Apr and Sep 2025**. Repair users = those who repaired **by 30 Sep 2025**. Measure purchase-visit churn on 31 Oct 2026. Match on age band × pre-launch spend quartile × **Apr–Sep 2025 purchase-visit quartile**.

| Comparison (3,478 customers, 833 early repair users) | Users | Non-users | Gap |
|---|---|---|---|
| Raw | 17.0% | 50.8% | −33.8 pts |
| Matched age × spend | 17.0% | 42.5% | −25.4 pts |
| **Matched age × spend × visit frequency** | **16.9%** | **32.7%** | **−15.8 pts** |
| *C-1 published (matched, still buying)* | *14.8%* | *65.7%* | *−50.9 pts* |

The "non-users" here include people who started repairing after Sep 2025, which pulls the gap toward zero. So −16 pts is a fair **upper** estimate of what matching alone can show, not a lower one.

**Impact:** about **two-thirds of the −51 pt gap is built in by the definition or comes from engagement.** The conclusion survives (repair users really do churn less), but slide 7's "51 out of 100" overstates it about 3×.

**Fix:**
- In `s7_churn_gap.png`, replace or relabel the 51 bar: "All customers 69 → Similar customers, fair timing 16 → Repairs alone (model) 5 to 9".
- In C F1 and `summary.py` §6, add the landmark result as the main matched estimate and keep −51 as "the naive matched gap".
- C's 25/50/100% what-ifs are all fractions of 51 pts. They are already labelled as appendix what-ifs; keep it that way.

### M2. D's churn model: biases in both directions, and a one-year view (Medium)
**Where:** `analysis/d_customers_arr/d3_churn_model.py`, D F5.

The design is good: features are fixed at a cutoff date, the label is churn over the next 180 days, there's a held-out test set, AUC is 0.84, the purchase-only label is checked, and bootstrap ranges are given. It is our best estimate. But:

1. **It controls for something repairs work through (downward bias).** `visits_12m` and `purchase_visits_12m` cover the 12 months before the cutoff, and those include **repair trips and the purchases made on them** (4,128 transactions combine a purchase with a drop-off). If repairs keep customers partly by bringing them into the store, holding visits fixed removes that path. "Switching off" `used_repair` while keeping the visit count is an impossible customer: someone who never repaired but made the same repair trips.
2. **Engagement we can't measure (upward bias).** The model can't see brand affection, how much someone likes outerwear, and so on.
3. **One-year horizon (understates the cost of closing).** The forecast multiplies a **180-day** churn probability by **12 months** of ARR and stops after one year. A customer kept by repairs is worth several years of profit, so the true cost of closing is higher than the one-year figure.
4. **The cost of the program also grows** (about 1,118 new users a year), and the forecast handles this symmetrically. Fine.

**What a bigger effect would mean (C-2's method: users' ARR × effect × 56.2% margin):**

| Repair effect | Profit at risk | Net of closing (vs $133.5K saved) |
|---|---|---|
| 4.6 pts (break-even) | $132K | ≈ $0 |
| 5.3 pts (trees, average) | $153K | −$19K |
| 8.6 pts (logistic) | $248K | −$114K |
| 15.8 pts (landmark, upper) | $461K | −$327K |

(D's per-customer forecast gives smaller losses, +$57K to −$67K, because the trees model puts the effect on lower-ARR users.)

**Impact:** "roughly break-even" is the cautious, defensible headline. But the risk is **lopsided**: every estimate is at or above break-even, the best case for closing is +$57K, and the plausible downside runs to several hundred thousand. **Add this sentence to slide 8 / slide 10.**

### M3. Loyalty is presented as a cost without its return (High: framing)
**Where:** blueprint slide 1 ("Loyalty: points cost $413K/yr"), slide 6, slide 8 (only the cost appears).

Our profit figure **already subtracts redeemed points**. B-1 measures profit, not revenue:
- Matched members gained **+$609 profit each** over similar non-members in the year after launch. Across 2,565 members that is about **$1.56M**, against points costs that were lower in that first year than the $413K now.
- **I tested the obvious objection** (members joining *during* the "after" year, so their extra spend could come before they joined): comparing only **early joiners (Jun–Aug 2024)** on **Sep 2024 – May 2025**, and dropping later joiners, gives **+$1,239 revenue / +$639 profit**. B-1 is robust to join timing.
- The remaining problem is **self-selection** (joiners spent 3.6× more before launch). So $1.56M is an upper bound. But even if only ~25% of it is really caused by loyalty, the program covers its points cost.

**Impact:** "loyalty has no proven effect" is correct. "Loyalty loses money" or "costs $413K" with nothing on the other side **is not supported**. A judge could turn this against us.

**Fix:** on slide 1, change the loyalty verdict to *"Pays its way at best, unproven at worst. Don't make it more generous."* On slide 6, show the matched +$609 profit (marked as an upper bound) next to the cost.

### M4. "Membership has no retention effect (odds ratio 0.99)" is weaker than stated (Medium)
**Where:** D F5, B F1, blueprint slide 6.

- About **93% of revenue** in the last 12 months came from members (A F11: ~90% from mid-2025). Among active customers, membership barely varies, so the model has little to learn from.
- The same model also includes **tier (silver_or_gold)**, **points redeemed** and **visits**. All three are partly *caused* by membership, so the `member` coefficient only captures what's left after them.
- Points redeemed has an odds ratio of 1.34 (more churn). That fits customers cashing out before they leave, which is a reverse-timing effect, not a loyalty effect.

**Fix:** say *"no separate retention effect detected once engagement is controlled"*, not *"membership has no retention effect"*. The recommendation doesn't change.

### M5. New finding: returns refund the full price but don't give back redeemed points (Medium)
**Where:** not covered by any stream; came out of checking B-2.

- On Return rows, `points_redeemed` is **always 0**, and earned points are clawed back (−1.0M points in total). In 95.5% of member return-only visits the balance moves by exactly *earned − redeemed*, so redeemed points are **not restored**.
- The refund is the full `unit_price_paid`, even when most of the purchase was paid with points.
- Since launch, about **$70K of points-funded value** has gone out inside refunds, **$36K of it from purchases paid >50% with points**: the same group that returns 4× as often (Part 4).

**Interpretation, with care:** if the store refunds those returns in cash or card, **a points-paid purchase followed by a return turns points into cash**. That would also explain why the >50%-points group returns so much more. The data can't confirm the store's actual refund policy, so present it as *"the data suggests…; confirm the refund policy"*.

**Fix / recommendation:** refund the points-funded part of a purchase as points, not cash. It's cheap, quick and low-risk. Add it to the loyalty redesign on slide 9.

### M6. Most of the growth above the pre-competitor level came in 2026 (Medium: framing)
Repeat revenue vs the same months of Mar 2023 – Feb 2024:

| Period | Change |
|---|---|
| Mar 2024 – Feb 2025 | −12.2% |
| Mar 2025 – Feb 2026 | +1.2% |
| **Mar – Oct 2026** | **+10.4%** |

Loyalty launched in **June 2024**. By the end of its second year, revenue had only got back to the pre-competitor level (+1%). The step up to a record came in 2026, right after the **website redesign (Nov 2025)** and the **new store manager (Feb 2026)**. It also coincides with Gold share levelling off and repairs maturing. We can't separate these, but it is one more reason **not** to credit loyalty with the recovery, and the deck should say so on slide 4 (it's currently only listed as a risk on slide 10).

### M7. `age_band` is fixed per customer (Low: caveat)
`customers.csv` holds one `age_band` per customer, not age at the time of each purchase. Over a four-year window some customers will have moved bands. The competitor story doesn't depend on this, because the day-level evidence is decisive (18–24 sales +2% on 1–14 March 2024, then −50% from 15 March, the day the competitor opened). But "18–24 ARR −46%" compares a fixed group of people, and that is worth one line in the caveats.

### Smaller method notes (no action needed, but be ready to answer)
- **C-2's margin (56%, repair users) vs D's (57%, all customers):** documented, and doesn't change anything.
- **Seasonality:** every stream compares the same months or full 12-month windows. ✅ C F4's cannibalization uses full-year windows, so it is fine despite jackets selling 49% of their year in Nov–Jan.
- **C F2 turnaround buckets** are not matched, and users with slow repairs made fewer drop-offs (1.8 vs 2.1–2.9). "Slow repairs go with churn" is a correlation. It's a fine KPI, but not proof that faster repairs cut churn.
- **Pilates (D F3):** solid design (same signup weeks). No campaign cost data, so it measures value, not ROI. Already stated.
- **B-3 tier proximity:** measures basket size, not visit timing. Customers could visit *sooner* when close to a tier. Already stated.

---

## Part 4. What is strong and should be defended

These findings came through every check. Lean on them in Q&A.

1. **The competitor timing is airtight.** The 18–24 drop starts on the opening day itself (+2% on 1–14 Mar vs −50% on 15–31 Mar 2024, compared with the same days of 2023). A seasonal model with a trend gives −14% in year 1, and a simple year-on-year comparison gives −12%: two methods agree.
2. **The recovery came from fewer, older customers spending more.** Active repeat customers are still 5% below pre-competitor levels, while revenue per customer is +17%. 18–24 ARR is −46% and still falling (young shoppers active Mar–Oct: 1,513 → 1,106 → 858 → 725).
3. **B-2 is robust, more than B claimed.** Purchases paid >50% with points have higher return rates at every level:

   | Points share | Visits | Visit return rate | **Unit return rate** | **Single-item baskets** | Avg basket |
   |---|---|---|---|---|---|
   | 0% | 133,425 | 9.5% | 5.0% | 5.1% | $164 |
   | 1–25% | 25,580 | 10.5% | 4.9% | 4.9% | $192 |
   | 26–50% | 5,861 | 9.8% | 6.7% | 6.8% | $102 |
   | **>50%** | **3,617** | **23.7%** | **20.1%** | **21.2%** | **$68** |

   Baskets in that group are *smaller* (1.2 lines), which should make a return at visit level *less* likely, yet the per-item rate is **4×**. This is not a basket-size artefact.
4. **B-1 holds up whenever people joined** (+$1,239 / +$639 for early joiners only). The only caveat left is self-selection.
5. **No outerwear cannibalization** (C F4): repair users' outerwear spend rose 10% while non-users' fell 48%.
6. **D's churn model** is a proper predictive setup (features at a cutoff, held-out AUC 0.84, bootstrapped ranges, purchase-only robustness check). With M2's caveats, it is our strongest causal-ish evidence.
7. **Pilates** (52% vs 81% came back within a year; 90% churned) uses a clean same-weeks comparison.

---

## Part 5. What the analyses say about the best move

### 5.1 The question, restated
Leadership wants to **scrap free repairs** (to save cost, believing they cannibalize outerwear) and **expand loyalty** (believing it drove the recovery). We judge both on **ARR** and **profit**.

### 5.2 What each piece of evidence says

| Evidence | What it says | Strength |
|---|---|---|
| Competitor (A F1–F10) | Took 18–24s from the opening day; they haven't come back; new young shoppers halved (420 → 201) | Strong |
| Recovery (D F1–F2, A F4, F11, M6) | Came from 25+ customers visiting more often; most of it in 2026, overlapping the website and new manager | Strong (the "what"); weak (the "why") |
| Loyalty spend (B F1, M3) | Members +$1,110 revenue / +$609 profit vs matched non-members; robust to join timing; upper bound because of self-selection | Medium |
| Loyalty retention (D F5, M4) | No separate effect detected; weak test | Weak |
| Loyalty cost (B F1, D2) | ~7% of member revenue, structural (tier mix), levelled off; Gold = 69% of member revenue | Strong |
| Tier mechanic (B F3) | Being close to the next tier doesn't change basket size | Medium |
| Points and returns (B F2, M5) | >50%-points purchases are returned 4× as often per item; returns don't give points back (~$70K) | Strong (pattern); policy unconfirmed |
| Repair retention (C F1, M1, D F5, M2) | Real but smaller than the naive gap: 5–9 pts (model) up to ~16 pts (fair matching); break-even 4.6 pts | Medium |
| Repair cost (C F3) | $134K a year | Strong |
| Cannibalization (C F4, A F5) | None found; the outerwear drop came from non-users and from lost 18–24s | Medium |
| Who uses repairs (C F5) | 97% members, 64% Gold, $2,456 ARR each vs $494; 77% of ARR | Strong (descriptive) |
| Pilates (D F3) | Acquisition campaigns didn't keep customers | Strong |
| Young-shopper value (A F12, D1) | Half win-back ≈ $155K–$195K profit a year before the cost of the offer | Medium |

### 5.3 The answer

> **Don't proceed as planned. Keep free repairs, keep loyalty but don't make it more generous (fix it instead), and put the new money into winning back young shoppers.**

#### 1. Keep free repairs, and make them cheaper and faster
- **The money:** closing saves **at most ~$57K a year** (under 1% of revenue) in the most favourable model. Every effect estimate is at or above the 4.6-pt break-even, and the plausible downside is a loss of $67K to $300K+ a year. Over several years (customers kept stay longer), the case for keeping repairs gets stronger. **The risk is lopsided.**
- **Who it protects:** repair users are the core of the business: 77% of ARR, 64% Gold, 97% members. **Scrapping repairs while expanding loyalty takes a perk away from the same Gold members that "expanding loyalty" is meant to reward.** The two halves of leadership's plan contradict each other.
- **Cannibalization:** none found. Leadership's second reason doesn't hold.
- **Make it pay more clearly:**
  - Turnaround target **≤ 20 days** (churn is 24% vs 11–13% for slower repairs; a correlation, but a cheap target).
  - Lower cost per repair (outerwear $45, activewear $18).
  - Consider **making repairs a formal Silver/Gold benefit**. Almost all users are members already, so this costs almost nothing, ties repairs to the loyalty brand, and *is* a way to "expand loyalty" without raising points costs.
  - Optional: a yearly cap per customer if costs grow with the ~1,100 new users a year.

#### 2. Loyalty: keep it, don't make it more generous, fix how it works
- **Don't scrap it:** the matched evidence (robust to join timing) says it at least pays for its points. "No proven effect" is not "loss-making".
- **Don't expand it by giving more:** the cost is structural, ~7% of member revenue. Two-thirds of member spend already earns Gold rates, the tier mechanic doesn't change basket size, and no separate retention effect was detected. **Each +0.25 pts per $ ≈ +$81K a year** with no evidence it would bring in more.
- **Fix it instead:**
  - **Refund points as points on returns** (M5): closes a possible points-to-cash leak (~$70K since launch).
  - **Cap points at 50% of a purchase** (B F2): that group returns 4× as often per item.
  - **Rethink Gold:** a higher threshold, or reward **visit frequency** (A F11: the 25+ recovery came from visiting 22% more often, which is what a loyalty program should encourage), rather than more points per dollar.
  - **Move perks from points to experiences/services** (repairs, early access) that cost less per dollar of perceived value.
- **Test before any expansion:** offer a perk change to a random half of members for 3–6 months and compare profit per member and 6-month retention. With a single store, random assignment by customer is the only clean way to do it.

#### 3. Put new money into the 18–24 gap
- This is the **largest single profit lever** we found: about **$155K–$195K a year** for winning back half the lost young shoppers, before the cost of the offer. Rule of thumb: an offer that costs less than **~$430 per young shopper kept for a year** pays back within the year.
- Neither loyalty nor repairs reached this group, and the decline is **ongoing** (first-time 18–24 shoppers are still falling in 2026).
- **How:** target the staples the competitor undercut (leggings −30%, in every age group; −61% for 18–24s), and the routes into the store that dried up (walk-ins −50%, social −45%, referrals −38%).
- **Learn from Pilates:** acquisition campaigns didn't stick. Judge any youth offer on **6- and 12-month retention**, not sign-ups.
- **Risk:** price-matching staples squeezes margin. Start with one category (leggings) and measure.

#### 4. Measure differently
| Area | KPI | Current | Target / direction |
|---|---|---|---|
| Repairs | Landmark churn gap (repaired vs similar non-repairers, matched incl. visit frequency) | −16 pts | Keep ≥ break-even (4.6 pts) |
| Repairs | Share of repairs with turnaround > 20 days | see C F2 (280 of 2,119 users have a median over 20 days) | ↓ |
| Repairs | Cost per repair, repair cost per $ of repair users' ARR | $134K / $5.12M = 2.6% | ↓ |
| Loyalty | Points earned as % of member revenue | 6.9% | ≤ current; don't let expansions raise it untested |
| Loyalty | Return rate on >50%-points purchases | 23.7% (visit) / 20.1% (unit) | → ~10% after the cap and points-as-points refunds |
| Loyalty | Profit per member vs matched non-members (holdout) | +$609 (upper bound) | Positive in a randomized test |
| Customers | First-time 18–24 shoppers per quarter | falling (201 in Mar–Oct 2026) | ↑ |
| Customers | 18–24 ARR | $641K (−46%) | ↑ |
| Acquisition | 6- and 12-month return rate of new customers | Pilates 52% vs 81% | Use to judge every campaign |

### 5.4 What would change this answer
- **If a randomized test showed loyalty perks raise retention or spend** beyond the matched upper bound → expanding it (carefully) becomes defensible.
- **If the true repair effect is below ~4.6 pts** (e.g. a holdout or a pause in one category showed little churn change) → repairs become cost-neutral to slightly negative. Narrow them (members only, a yearly cap) rather than scrap them outright, because of the Gold-member signal.
- **If the store's refund policy already gives points back as points** → drop M5's leak; the 50% cap still holds.
- **If the 2026 growth turns out to come from the website / new manager** → it supports the "loyalty isn't the engine" story even more, and the website deserves its own analysis (our data has no online/offline channel field).

### 5.5 Risks and honest limits
- **Self-selection everywhere.** Members and repair users choose to take part. Matching and the churn model reduce the bias but don't remove it. All program effects are bounds, not proof.
- **The repair net is close to zero in the central estimates.** The case for keeping repairs rests on the lopsided risk and the Gold-member signal, not on a big profit.
- **ARR lags** real changes by up to 12 months. Track monthly active repeat customers too.
- **Overlapping events in 2026** (website, new manager) can't be separated with this data.
- **No cost data** for campaigns, store operations or offers, so all "value" figures are before those costs.
- **Q6 (demoted Silver members)** wasn't measured: tier is only recorded at a visit.

### 5.6 One-sentence version for slide 1
> **"Free repairs keep our best customers for about what they cost. Loyalty rewards customers who were already loyal, and making it more generous adds cost with no proven return. The money we're missing is the young shoppers the competitor took, and neither program brings them back."**

---

## Part 6. Fix list by file

| File | Change | Issue |
|---|---|---|
| `slides/deck_charts.py:253` + `slides/charts/s8_financial.png` | Win-back 212 → 195 (or the range 155–195); show the green bars as ranges or add footnotes | D1, D3 |
| `slides/deck_charts.py` (slide 7 chart block) + `s7_churn_gap.png` | Relabel / replace "Similar customers 51" with the landmark −16 pts | M1 |
| `slides/deck_blueprint.md` slide 1 | Loyalty verdict: "pays its way at best, unproven at worst" | M3 |
| `slides/deck_blueprint.md` slide 6 | Remove "cost keeps rising"; add "steady ~7% of member revenue, Gold = 69%"; show +$609 (upper bound) next to the cost; add the refund finding | D2, M3, M5 |
| `slides/deck_blueprint.md` slide 7 | Gap: −16 pts fair matched, 5–9 pts model | M1, D4 |
| `slides/deck_blueprint.md` slide 8 | Win-back $195K; add "the risk is lopsided: every estimate ≥ break-even" | D1, M2 |
| `slides/deck_blueprint.md` slide 4 | Note that most above-baseline growth came in 2026 (website, new manager) | M6 |
| `slides/deck_blueprint.md` slide 9 | Replace the "15% vs 66%" KPI; add points-as-points refunds; repairs as a Silver/Gold perk | D6, M5 |
| `summary.py:340`, `:671`, `:686` | Remove "keeps rising" / "as balances build"; replace the KPI | D2, D6 |
| `summary.py` §6 | Add the landmark repair gap as the main matched estimate | M1 |
| `results/a_competitor/findings.md` F12 | $212K → $195K; explain the margin mix | D1 |
| `results/b_loyalty/findings.md` F1 | Fix the "rising" explanation; add the early-joiner check; mark the first-pass notes superseded | D2, M3, D5 |
| `results/c_repairs/findings.md` F1 | Add the late-starter bias (188 users, 11%) and the landmark table | M1 |
| `results/d_customers_arr/findings.md` F5 | "no separate effect detected"; note the visits-control bias and the one-year horizon | M2, M4 |
| `results/d_customers_arr/deck_b1_profit_members.png` | Delete or rename `_superseded` | D5 |
| `docs/decisions_log.md` | Log the changes above as decisions #23+ | — |
| Regenerate | `python slides/deck_charts.py`, then rebuild `summary.ipynb` from `summary.py` | — |

---

## Appendix A. Output of the review checks

Output of `python docs/review/review_checks.py` (21 Nov 2026), condensed:

```
=== 0. Headline ARR ===
ARR Feb 2024 $6,293,878 | low Feb 2025 $5,526,196 | Oct 2026 $6,672,617 (+6.0%)
Revenue last 12 months $7,020,532; margin incl. points & repairs 55.3%

=== 1. Young-shopper value (A F12) ===
Mar 2023-Feb 2024: revenue $1,270,206, profit $804,410, margin 63.3%, buyers 1,799, points $0
Nov 2025-Oct 2026: revenue $677,758, profit $380,130, margin 56.1%, buyers 887, points $39,515
Published: lost profit $424,279; 50% win-back $212,140
Lost buyers 912; profit per buyer today $429
  50% win-back at today's profit per buyer: $195,422
  Lost revenue at today's margin: $332,282 (50%: $166,141)
  18-24 ARR lost $549,382; 50% x today's margin: $154,064
  Implied margin of published pair ($212K profit / $275K ARR): 77%

=== 2. Points cost ===
q                    2024Q2  2024Q3  2024Q4  2025Q1  2025Q2  2025Q3  2025Q4  2026Q1  2026Q2  2026Q3  2026Q4
earned_%_member_rev     5.0     5.5     6.2     6.6     6.7     6.7     6.8     6.9     6.9     6.9     6.9
redeemed_%_all_rev      0.6     2.4     3.9     5.0     5.8     5.4     5.3     6.2     6.5     5.7     5.5
gold_%_member_rev       NaN     3.5    32.5    50.2    55.3    58.2    63.9    68.9    69.3    68.7    67.9
Points earned since launch $923,354; redeemed $796,635; outstanding balance $126,604
Member revenue last 12 months $6,505,636 (93% of revenue); +0.25 pts per $ costs ~$81,320/yr
Points cut to 5% of revenue (slide 8 bar): $61,858

=== 3. Loyalty matched DiD (B-1) ===
Published design: 3,798 customers, 2,565 members: +$1,110 revenue, +$609 profit (55%); x members = $1,562,291
Year-1 joiners by quarter: 2024Q2 871, Q3 1,300, Q4 949, 2025Q1 618, Q2 366
Early joiners (Jun-Aug 2024) vs not joined by May 2025, Sep-May windows: 2,113 customers, 1,297 members:
  +$1,239 revenue, +$639 profit

=== 4. Returns vs points share (B-2) ===
bucket  visits  visit_rate  unit_rate  single_item_rate  avg_lines  avg_basket
0%      133425  0.095       0.050      0.051             1.906      163.97
1-25%    25580  0.105       0.049      0.049             2.165      191.73
26-50%    5861  0.098       0.067      0.068             1.490      102.28
>50%      3617  0.237       0.201      0.212             1.207       68.26
Return rows: points_redeemed total 0 (never restored); points_earned total -1,003,151 (clawed back)
Return-only member visits where balance change = earned - redeemed: 95.5% of 9,979
Points-funded value inside refunds since launch: $70,387 (from >50%-points purchases: $36,171)

=== 5. Repair churn gap (C-1) ===
Cohort repair users 1,702; first repair after 04 May 2026 (cannot count as churned): 188 (11%).
  Churn: all users 14.7%, excluding late starters 16.6%
Landmark sample 3,478 (833 repaired by Sep 2025); purchase-visit churn
  raw:                          users 17.0% vs non-users 50.8% -> -33.8%
  matched age x spend           users 17.0% vs non-users 42.5% -> -25.4%
  matched age x spend x visits  users 16.9% vs non-users 32.7% -> -15.8%

=== 6. Profit at risk at different repair effects ===
Repair users' ARR $5,122,817; margin before repair cost 56.2%; repair cost $133,542; break-even 4.6 pts
  effect 4.6%:  profit at risk $132,400 -> net of closing     +$1,142
  effect 5.3%:  profit at risk $152,548 -> net of closing    -$19,006
  effect 8.6%:  profit at risk $247,531 -> net of closing   -$113,989
  effect 16.0%: profit at risk $460,522 -> net of closing   -$326,980

=== 7. Repeat revenue vs same months of Mar 2023-Feb 2024 ===
  Mar 2024-Feb 2025: -12.2%
  Mar 2025-Feb 2026: +1.2%
  Mar-Oct 2026:      +10.4%
```

## Appendix B. Glossary
- **ARR:** trailing-12-month revenue from repeat visits (visits after `signup_date`).
- **Churned:** no visit in the last 180 days (as of 31 Oct 2026, unless stated otherwise).
- **Matched comparison:** compare like with like within cells (age band × spend quartile, and in this review also × visit frequency), weighting by the number of program users in each cell.
- **Difference-in-differences (DiD):** the change for members minus the change for similar non-members over the same period.
- **Landmark design:** decide who counts as a "user" at a fixed date (here 30 Sep 2025), among customers active up to that date, and only measure outcomes afterwards. This prevents people from being labelled users *because* they were still around.
- **Break-even effect:** the churn reduction (in percentage points) at which the profit repairs protect equals what they cost (4.6 pts).
- **Upper bound:** the true effect is probably smaller, because the people who opt in were already better customers.
