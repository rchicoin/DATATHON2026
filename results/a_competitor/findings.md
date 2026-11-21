# Findings — Competitor impact & seasonality

Owner: Person A (Aylin) · Branch: `main` · Last updated: 2026-11-21

<!-- Add a finding as soon as you have it. Copy this block for each one. Newest at the top. -->

All A-1 numbers come from `analysis/a_competitor/a1_competitor_impact.ipynb`. They use purchase lines only (`row_type == Purchase`) and compare Mar–Oct each year with Mar–Oct 2023, which cancels out seasonality.
A-2 numbers (F6–F8) come from `analysis/a_competitor/a2_seasonality.ipynb`. They also use purchases only. Every calendar month appears exactly 4 times in the data (Nov 2022 – Oct 2026), so the monthly averages are balanced.
A-3 numbers (F9–F10, the Stream A should-have) come from `analysis/a_competitor/a3_signups_retention.ipynb`. New customers are counted only from Nov 2022, because the customer file has no one who stopped shopping before then.

## F10. 18–24s still dwindling in 2026: fewer new customers and fewer returning ones
- **Claim:** Active 18–24 customers (Mar–Oct) went **1,513 (2023) → 1,106 → 858 → 725 (2026)**, down 52% in three years. In 2026, new 18–24s fell again (244 → 201), and returning ones kept shrinking (614 → 524), because each year fewer new young customers join to replace those who leave. In the first year (2023 → 2024), the 407 lost active customers split almost evenly: 195 fewer new and 212 fewer returning.
- **Evidence:** new vs. returning table, section 3
- **Chart:** `results/a_competitor/a3_18_24_new_vs_returning.png`
- **Confidence / caveats:** high. This answers the open question from F4: the 2026 dip (index 53) is real and ongoing, not noise.
- **So what for the recommendation:** without new young customers coming in, the 18–24 segment keeps shrinking every year. Neither loyalty (Jun 2024) nor repairs (Apr 2025) reversed it. Leadership's plan doesn't address the segment the competitor targeted. KPI to track: new 18–24 customers per quarter.
- **Handed to D?** yes

## F9. The competitor halved new young customers AND made existing ones less loyal
- **Claim (acquisition):** New 18–24 customers in Mar–Oct fell from **420 (2023) to 225 (2024), −46%**, and stayed down: 244 in 2025, 201 in 2026. Their share of all new customers fell from **26% to 15%**. New customers aged 25+ grew 5% over the same period. Nearly every acquisition channel halved for 18–24s (walk-in 233 → 117, social media 106 → 58, referral 81 → 50).
- **Claim (retention):** Before the competitor, 18–24s were **as loyal as everyone else**: 56% of those who bought in Nov 2022 – Feb 2023 bought again the next winter, vs. 54% for ages 25+. Across the competitor's opening, this fell to **35% vs. 44%**, and afterwards it was **44% vs. 52%**. Every age band's retention dropped when the competitor opened, but young customers dropped twice as much (−21 points vs. −10). They have stayed ~9 points behind since.
- **Evidence:** new-customer table and retention tables (Nov–Feb windows give the pre-competitor benchmark; Mar–Oct windows match A-1), sections 1–2
- **Chart:** `results/a_competitor/a3_new_customers_by_age.png`, `results/a_competitor/a3_retention_by_age.png`
- **Confidence / caveats:** high on direction. The pre-competitor benchmark is a single year-on-year transition, because the data starts Nov 2022. Retention = bought again in the same months a year later, so seasonality cancels out.
- **So what for the recommendation:** the competitor's lasting damage is a **broken pipeline of young customers**, not just a one-off loss. Expanding perks for existing members doesn't fix acquisition. A targeted 18–24 offer (or matching on staples like leggings, see F2) would address the actual gap.
- **Handed to D?** yes

## F8. Black Friday + Boxing Week are 9 days and ~5% of yearly revenue; they don't drive the December peak
- **Claim:** Each year has 3 Black Friday days (25% off) and 6 Boxing Week days (30% off). Together they bring in **5.2% of annual revenue** (4.8%–5.8% across years) and cost about **$142K a year in discounts**. A sale day sells ~2.5× a normal Jan–Oct day, but only **~1.4× other Nov–Dec days** ($42.9K and $38.5K per day vs. $29.1K). Most of the holiday peak is full-price gift and winter shopping.
- **Evidence:** promo table and daily-revenue comparison, section 3 of the A-2 notebook. Sales are flagged from price paid vs. list price, and the only discounts are exactly 25% and 30%.
- **Chart:** `results/a_competitor/a2_promo_days.png`
- **Confidence / caveats:** high. Sale days may pull purchases forward from nearby days; we don't measure that.
- **So what for the recommendation:** don't treat Nov–Dec revenue (26–30% of each year) as a program effect. Any period comparison must cover the same months.
- **Handed to D?** yes

## F7. Outerwear and hoodies make ~half their year's sales in Nov–Jan; the repair program launched in their slowest season
- **Claim:** Outerwear peaks in December at 2.7× an average month and bottoms out in Jun–Jul at 0.3×. **49% of its yearly revenue comes in Nov–Jan.** Hoodies follow the same pattern (Dec 2.9×, Jun 0.2×). Shorts and tank tops are the mirror image: 1.7–1.85× in May–Aug, ~0.3× in Jan–Feb. Leggings, sports bras, tops and accessories are fairly flat apart from the December gift peak (1.6–1.9×).
- **Evidence:** the category × month heatmap and peaks table, section 2
- **Chart:** `results/a_competitor/a2_seasonality_heatmap.png`
- **Confidence / caveats:** high
- **So what for the recommendation (for Stream C):** repairs launched **1 April 2025**, right as outerwear enters its quietest months (Apr 0.6×, Jun–Jul 0.3×). A before/after-launch comparison of outerwear would show a big "drop" that is pure seasonality. Cannibalization tests must compare **the same months year over year**, or repair users vs. similar non-users in the same months.
- **Handed to D?** yes, and **to C**

## F6. Store-wide seasonality is strong and stable: December ≈ 1.9×, February/June/July ≈ 0.76×
- **Claim:** Seasonal index (100 = average month): Dec 194, Nov 127, Sep–Oct 106–107 (back to school / fall), Jan 98. The low point is Feb and Jun (76) and Jul (78). The profile is almost identical (correlation 1.00) in the single pre-competitor year (Mar 2023 – Feb 2024), so the competitor didn't change *when* people shop, only *how many* shop.
- **Evidence:** store-level index table, section 1. **Robustness (section 1b):** four methods agree within 6 points: simple average month, revenue per open day, ratio to a 12-month moving average, and a regression with trend and a competitor-year flag. The biggest gap is February (76 simple vs. 82 per open day), because February has only 28 days.
- **Side result:** the regression estimates the **competitor year cost about 14% of revenue** after controlling for seasonality and trend (a simple comparison of Mar 2024–Feb 2025 with the year before gives −12%). The underlying trend is about +3% a year. This independently supports F1.
- **Chart:** bottom row of `results/a_competitor/a2_seasonality_heatmap.png`
- **Confidence / caveats:** high. The regression uses only 48 monthly points, so treat −14% as an estimate, not a precise figure.
- **So what for the recommendation:** **every stream should compare the same months year over year** (or use these indices to adjust). A launch-month comparison would be skewed by up to 2.5×: for example, loyalty launched in June (index 76) and repairs in April (82), both quiet months.
- **Handed to D?** yes

## F5. The 2025 outerwear dip comes from losing 18–24s, not (yet) evidence of repair cannibalization
- **Claim:** Outerwear revenue in Mar–Oct 2025 was 10% below 2023, while most other categories grew. Almost all of the gap is 18–24 customers (−46%). For other ages, outerwear is roughly flat: 25–34 −8%, 35–44 −5%, 45–54 +1%, 55+ up.
- **Evidence:** the outerwear row of the age × category table, section 5 of the notebook
- **Chart:** none (table in notebook)
- **Confidence / caveats:** medium. Repairs launched in April 2025, so 2025 overlaps with the repair program. This only shows the dip lines up with the age mix. Stream C's before/after test on repair users is still needed.
- **So what for the recommendation:** management's claim that repairs "cannibalize outerwear" can't rest on the overall outerwear decline. That decline is explained by the competitor taking young customers.
- **Handed to D?** yes, and **to C**

## F4. 18–24s never came back: revenue is still about 45% below 2023 in 2025 and 2026
- **Claim:** Indexed to Mar–Oct 2023 = 100, 18–24 revenue is 55 (2024), 58 (2025) and 53 (2026). Every other age band recovered and grew: 25–34 → 115, 35–44 → 132, 45–54 → 122, 55+ → 128. Store-wide revenue was back to +2% vs. 2023 in 2025.
- **Evidence:** recovery index table, section 4
- **Chart:** `results/a_competitor/a1_recovery_index.png`
- **Confidence / caveats:** high for the revenue numbers. **Watch out:** from March 2025, each month is compared with a post-competitor month, so 2025 YoY jumps (+20% to +60%) are partly a bounce from a low base. Always compare against 2023, the year before the competitor.
- **So what for the recommendation:** the "revenue recovery" that leadership credits to loyalty is driven by customers aged 25 and over. The young segment the competitor took is still gone, and neither loyalty nor repairs won it back. Any ARR or loyalty uplift claim must be checked for this age mix.
- **Handed to D?** yes

## F3. The competitor took 18–24 customers and their visits, not their basket size
- **Claim:** In Mar–Oct 2024 vs. 2023, 18–24s had 27% fewer active customers and 25% fewer visits per customer, while spend per visit was unchanged ($113). In 2025, visit frequency for the 18–24s who stayed recovered (+4%), but the customer count fell further (−43% vs. 2023).
- **Evidence:** the drivers table, section 3 (revenue = customers × visits per customer × spend per visit)
- **Chart:** `results/a_competitor/a1_18_24_drivers.png`
- **Confidence / caveats:** high. This is descriptive, and the "active customers" count only includes customers who bought something.
- **So what for the recommendation:** this is a customer-acquisition and retention problem, not a basket-size problem. Richer loyalty perks mainly reward people who already shop here. They don't obviously bring back lost young customers. A KPI worth tracking: active 18–24 customers.
- **Handed to D?** yes

## F2. Leggings fell hardest (−30%), across every age band; Burnaby and Richmond pulled back most
- **Claim:** Leggings lost $310K in Mar–Oct 2024 vs. 2023 (−30%), about double any other category (shorts −15%, tank tops and sports bras −14%). The leggings drop shows up in **every** age band (−16% to −58%), and only 35% of it came from 18–24s. Leggings fit the case's description of a staple item the competitor undercut. By home area, Burnaby (−26%) and Richmond (−25%) fell most, vs. −10% to −17% for the other neighbourhoods.
- **Evidence:** the category, home area and age × category tables, section 2
- **Chart:** `results/a_competitor/a1_hardest_hit_category_area.png`
- **Confidence / caveats:** high on the size of the drop. "Undercut staples" is the case's description; we have no competitor price data.
- **So what for the recommendation:** leggings are the most exposed category to price competition, so protect them rather than spending on store-wide perks. In 2025, leggings recovered for ages 35+ (around 0% to −8%) but not for 18–24 (−61%).
- **Handed to D?** yes

## F1. Sales dropped the day the competitor opened (15 March 2024), and 18–24s took most of the hit
- **Claim:** The competitor opened on **15 March 2024**. 18–24 revenue was normal from 1–14 March (+2% vs the same days of 2023), then fell **50% from 15–31 March** and 45–54% from April to August. Over the whole of March it was only −25%, because half the month was before the opening. Store revenue for Mar–Oct 2024 was −17% (−$681K) vs. 2023, and **18–24s account for 53% of the lost revenue while being only 19% of 2023 revenue**. Restricting to Mar–May (before loyalty launched) gives the same pattern: 18–24 −40%, 25–34 −22%, other ages −10% to −15%.
- **Evidence:** YoY table, the day-level check either side of 15 March, and the Mar–May robustness check, sections 1–2
- **Chart:** `results/a_competitor/a1_yoy_by_age.png`
- **Confidence / caveats:** high. The drop starts on the opening day itself. The Mar–Oct window includes two pre-competitor weeks (1–14 March), which slightly understates the drop.
- **So what for the recommendation:** whenever another stream compares "before vs. after loyalty" (June 2024), the competitor shock three months earlier distorts it. They should use the same months a year earlier and control for age band.
- **Handed to D?** yes

## Open questions
- ~~Is the 2026 18–24 dip real?~~ Answered in F10: yes, it's ongoing.
- All Stream A must-haves (A-1, A-2) and the should-have (A-3) are done.

## Decisions needed (also log them in `docs/decisions_log.md`)
- The competitor opened on **2024-03-15**. `config.py` (`COMPETITOR_OPEN`), `docs/definitions.md` and decision #6 still say 2024-03-01 "working estimate". Month-level analyses are unaffected (March 2024 is the first competitor month either way), but the docs and any day-level analysis should use 15 March.
