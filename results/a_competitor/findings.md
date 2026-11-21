# Findings — Competitor impact & seasonality

Owner: Person A (Aylin) · Branch: `main` · Last updated: 2026-11-21

<!-- Add a finding as soon as you have it. Copy this block for each one. Newest at the top. -->

All A-1 numbers come from `analysis/a_competitor/a1_competitor_impact.ipynb`. They use purchase lines only (`row_type == Purchase`) and compare Mar–Oct each year with Mar–Oct 2023, which cancels out seasonality.

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

## F1. The data confirms the competitor opened in March 2024, and 18–24s took most of the hit
- **Claim:** 18–24 revenue was up year over year through February 2024, then fell 25% in March and 45–54% from April to August. That's the first month it drops below −20%, which matches the working date in `config.py`. Store revenue for Mar–Oct 2024 was −17% (−$681K) vs. 2023, and **18–24s account for 53% of the lost revenue while being only 19% of 2023 revenue**. Restricting to Mar–May (before loyalty launched) gives the same pattern: 18–24 −40%, 25–34 −22%, other ages −10% to −15%.
- **Evidence:** YoY table and the Mar–May robustness check, sections 1–2
- **Chart:** `results/a_competitor/a1_yoy_by_age.png`
- **Confidence / caveats:** high on the timing. We have no external confirmation of the opening date, so describe it as "inferred from the data".
- **So what for the recommendation:** whenever another stream compares "before vs. after loyalty" (June 2024), the competitor shock three months earlier distorts it. They should use the same months a year earlier and control for age band.
- **Handed to D?** yes

## Open questions
- Does the 2026 18–24 dip (index 53) mean they're still drifting away, or is it noise? A quick check on 18–24 new sign-ups per month (A "should") would answer it.
- A-2 (seasonality heatmap) is not started yet.

## Decisions needed (also log them in `docs/decisions_log.md`)
- None. The competitor date of 2024-03-01 is **confirmed** by the data, so `config.py` needs no change.
