# Findings — Competitor impact & seasonality

Owner: Person A (Aylin) · Branch: `main` · Last updated: 2026-11-21

<!-- Add a finding as soon as you have it. Copy this block for each one. Newest at the top. -->

**Where the numbers come from** (all in `analysis/a_competitor/`, purchases only, no returns or repairs):
- F1–F5: `a1_competitor_impact.ipynb`. To remove seasonal swings, these compare **March–October of each year with March–October 2023**, the last year before the competitor.
- F6–F8: `a2_seasonality.ipynb`. The data covers exactly four years, so every month of the year appears four times and the averages are fair.
- F9–F10: `a3_signups_retention.ipynb`. First-time shoppers are only counted from November 2022, because the customer file doesn't include anyone who stopped shopping before then.
- F11–F12: `a4_recovery_and_value.ipynb`.

**Words used below:** *sales* = money customers paid. *ARR* = the case's measure: yearly sales from repeat shoppers (anyone buying again after their first purchase). *Came back* = bought again in the same months one year later.

## F12. The young shoppers we lost are worth about $550K a year in repeat sales and $424K a year in profit
- **Claim:** Yearly sales from repeat 18–24 shoppers (ARR) fell from **$1.19M just before the competitor (Feb 2024) to $0.64M now (Oct 2026): $549K less (−46%)**. The store's total still grew (+6%, from $6.29M to $6.67M) because every older age group grew. Compared with the year before the competitor, young shoppers now bring in **$592K less in sales and $424K less in profit every year**, because about 900 fewer of them shop here. Each young shopper is worth **about $430 of profit a year**. Winning back half of them (about 460 people) would add **about $195K of profit a year** (range $155K–$195K; *corrected from $212K, decision #23*: the $424K profit drop also includes a lower margin, 63% → 56%, because points didn't exist in the before year, and win-backs only recover customers at today's margin; $195K = 912 lost buyers × $429 profit per young buyer today × ½). That's about half of what loyalty points cost over the last 12 months ($413K), and more than the whole repair program ($134K).
- **Evidence:** Part 2 of the A-4 notebook (ARR by age group, value per young shopper, win-back scenarios)
- **Chart:** `results/a_competitor/a4_arr_change_by_age.png`, `results/a_competitor/a4_win_back_value.png`
- **Confidence / caveats:** high on the size of the loss. The win-back numbers assume returning shoppers behave like today's young shoppers, and they don't subtract the cost of whatever offer brings them back.
- **So what for the recommendation:** gives slide 10 a dollar figure. Spending part of the loyalty budget on winning back young shoppers is worth more than adding perks for people who already shop here. Rule of thumb: an offer that costs less than ~$430 per young shopper kept pays for itself within a year.
- **Handed to D?** yes

## F11. Loyalty didn't bring back the shoppers the competitor took, but it probably made older shoppers come more often
- **Claim:** Almost everyone who keeps shopping joins the program: by mid-2025, **about 90% of sales came from members**, in every age group. So "members' sales grew" mostly just shows who kept shopping. **Young shoppers joined almost as often as older ones (66% vs 70%) but still buy about 45% less than before the competitor.** Shoppers aged 25+ recovered: their March–October sales went from 90% of 2023's level in 2024 to 112% (2025) and 123% (2026). They didn't come back in bigger numbers (−4%), but each **came 22% more often** (4.5 → 5.4 shopping trips between March and October; 6.0 in 2026), spending slightly less per trip (−4%). Among 2023 shoppers who stayed, older members spent 27% more by 2025; young members spent about the same (−4%). The people who joined were already the best customers before the program existed (about $1,130 each vs $310 for non-joiners, March–October 2023).
- **Evidence:** Part 1 of the A-4 notebook (members' share of sales, join rates, what changed for each age group, same shoppers before vs after)
- **Chart:** `results/a_competitor/a4_member_share.png`, `results/a_competitor/a4_recovery_drivers.png`
- **Confidence / caveats:** medium. People choose to join, so members were keener shoppers to begin with. "Coming more often" is what points encourage, but older shoppers losing interest in the new competitor would look the same.
- **So what for the recommendation:** leadership gives loyalty too much credit. Its likely benefit (older regulars coming more often) doesn't need bigger perks, and it did nothing for the young shoppers the competitor took. For Aisyah (B), slide 5.
- **Handed to D?** yes, and **to B**

## F10. The number of young shoppers is still shrinking in 2026
- **Claim:** 18–24 year-olds who bought something between March and October: **1,513 (2023) → 1,106 → 858 → 725 (2026)**, down 52% in three years. In 2026, first-time young shoppers fell again (244 → 201), and young repeat shoppers kept falling too (614 → 524), because each year fewer newcomers arrive to replace the ones who drift away. In the first year (2023 → 2024), the loss of 407 young shoppers split almost evenly: 195 fewer first-timers and 212 fewer regulars.
- **Evidence:** first-time vs repeat shoppers table, section 3 of the A-3 notebook
- **Chart:** `results/a_competitor/a3_18_24_new_vs_returning.png`
- **Confidence / caveats:** high. This confirms the 2026 dip in F4 is a real, ongoing decline, not a blip.
- **So what for the recommendation:** without new young shoppers coming in, this group keeps getting smaller every year. Neither loyalty (June 2024) nor free repairs (April 2025) turned it around, and leadership's plan doesn't address the group the competitor targeted. Number to track: first-time 18–24 shoppers every three months.
- **Handed to D?** yes

## F9. The competitor halved the number of young people starting to shop here, and made existing young shoppers less likely to come back
- **Claim (new shoppers):** First-time 18–24 shoppers between March and October fell from **420 (2023) to 225 (2024), −46%**, and stayed low: 244 in 2025, 201 in 2026. Their share of all first-time shoppers fell from **26% to 15%**, while first-time shoppers aged 25+ grew 5%. It happened through every route into the store: walk-ins (233 → 117), social media (106 → 58) and referrals (81 → 50).
- **Claim (coming back):** Before the competitor, young shoppers were **as likely as anyone to come back**: 56% of those who bought something in November 2022 – February 2023 bought again the next winter, vs 54% of shoppers aged 25+. The winter the competitor opened, this fell to **35% vs 44%**, and since then it's been **44% vs 52%**. Every age group came back less when the competitor opened, but young shoppers dropped twice as much (21 points vs 10), and they've stayed about 9 points behind.
- **Evidence:** first-time shopper table and "came back" tables, sections 1–2 of the A-3 notebook. Winters (November–February) are used because that's the only stretch the data covers twice before the competitor opened.
- **Chart:** `results/a_competitor/a3_new_customers_by_age.png`, `results/a_competitor/a3_retention_by_age.png`
- **Confidence / caveats:** high on the direction. The "before the competitor" comparison is a single winter-to-winter pair, because the data starts in November 2022.
- **So what for the recommendation:** the competitor's lasting damage is that **far fewer young people start shopping here and stay**, not just a one-off loss. Bigger perks for existing members don't fix that. A targeted offer for 18–24 year-olds (or matching the competitor's price on basics like leggings, see F2) would.
- **Handed to D?** yes

## F8. The two holiday sales are only 9 days and about 5% of yearly sales; they're not what makes December big
- **Claim:** Each year there are 3 Black Friday days (25% off) and 6 Boxing Week days (30% off). Together they bring in **5.2% of a year's sales** on average (4.8%–5.8% depending on the year) and cost about **$142K a year in discounts**. A sale day sells about 2.5× a normal January–October day, but only **about 1.4× an ordinary November–December day** ($42.9K and $38.5K a day vs $29.1K). Most of the holiday rush is full-price gift and winter shopping.
- **Evidence:** holiday sales table and sales-per-day comparison, section 3 of the A-2 notebook. Sale purchases are found by comparing the price paid with the list price; the only discounts are exactly 25% and 30%.
- **Chart:** `results/a_competitor/a2_promo_days.png`
- **Confidence / caveats:** high. Sales may make people buy a few days earlier than they would have; we don't measure that.
- **So what for the recommendation:** November–December is a quarter or more of every year's sales (26–30%). Don't mistake that seasonal jump for a program working; always compare the same months across years.
- **Handed to D?** yes

## F7. Jackets and hoodies sell about half their year in November–January, and free repairs started just as their quiet season began
- **Claim:** Jackets (outerwear) sell 2.7× an average month in December and only 0.3× in June–July; **49% of their yearly sales happen in November–January.** Hoodies follow the same pattern (2.9× in December, 0.2× in June). Shorts and tank tops are the opposite: 1.7–1.85× in May–August and about 0.3× in January–February. Leggings, sports bras, tops and accessories sell steadily all year, apart from the December gift bump (1.6–1.9×).
- **Evidence:** the product-by-month chart and busiest/quietest month table, section 2 of the A-2 notebook
- **Chart:** `results/a_competitor/a2_seasonality_heatmap.png`
- **Confidence / caveats:** high
- **So what for the recommendation (for Stream C):** free repairs started on **1 April 2025**, just as jacket sales naturally fall (0.6× in April, 0.3× in June–July). Comparing jacket sales "before vs after repairs started" would show a big drop that happens every year anyway. To test whether repairs hurt jacket sales, compare **the same months across years**, or repair users with similar non-users in the same months.
- **Handed to D?** yes, and **to C**

## F6. The store's seasons are strong and haven't changed: December sells about twice a normal month; February, June and July about three-quarters
- **Claim:** Compared with an average month (= 100): December 194, November 127, September–October 106–107 (back to school / autumn), January 98. The quietest are February and June (76) and July (78). The year before the competitor shows the same pattern almost exactly, so the competitor changed *how many* people shop, not *when* they shop.
- **Evidence:** store-wide table, section 1 of the A-2 notebook. **Double-checked (section 1b)** with four different calculation methods, which agree within 6 points. The biggest difference is February (76 vs 82), partly because February only has 28 days.
- **Side result:** the statistical model in that check also estimates that the **first year with the competitor cost about 14% of sales**, after taking out the seasons and the store's normal growth (about +3% a year). A simple comparison of March 2024 – February 2025 with the year before gives −12%. Two methods agreeing supports F1.
- **Chart:** bottom row of `results/a_competitor/a2_seasonality_heatmap.png`
- **Confidence / caveats:** high. The model only has 48 months of data, so treat −14% as approximate.
- **So what for the recommendation:** **every stream should compare the same months across years.** A "before vs after launch" comparison can be thrown off by up to 2.5× just by the season. Loyalty started in June and repairs in April, both quiet months.
- **Handed to D?** yes

## F5. Jacket sales were down in 2025 because young shoppers left, not (as far as we can tell) because of repairs
- **Claim:** Jacket (outerwear) sales from March to October 2025 were 10% below 2023, while most other products grew. Almost all of that gap comes from 18–24 year-olds (−46%). For other ages, jacket sales were about flat: 25–34 −8%, 35–44 −5%, 45–54 +1%, 55+ up.
- **Evidence:** the jacket row of the age-by-product table, section 5 of the A-1 notebook
- **Chart:** none (table in notebook)
- **Confidence / caveats:** medium. Repairs started in April 2025, so 2025 overlaps with the repair program. This only shows that the drop matches who left. Stream C's comparison of repair users is still needed.
- **So what for the recommendation:** management says repairs "steal" jacket sales, but the overall drop in jacket sales doesn't prove that. It's explained by the competitor taking young shoppers.
- **Handed to D?** yes, and **to C**

## F4. Young shoppers never came back: sales to 18–24 year-olds are still about 45% below 2023
- **Claim:** With March–October 2023 = 100, sales to 18–24 year-olds were 55 (2024), 58 (2025) and 53 (2026). Every other age group recovered and now buys more than in 2023: 25–34 at 115, 35–44 at 132, 45–54 at 122, 55+ at 128. The store as a whole was back to +2% vs 2023 in 2025.
- **Evidence:** the "relative to 2023" table, section 4 of the A-1 notebook
- **Chart:** `results/a_competitor/a1_recovery_index.png`
- **Confidence / caveats:** high. **Watch out:** from March 2025, comparing each month with the same month a year earlier means comparing with a weak month right after the competitor opened, so the 2025 jumps (+20% to +60%) look better than reality. Compare with 2023 instead.
- **So what for the recommendation:** the "recovery" that leadership credits to loyalty comes entirely from shoppers aged 25 and over. The young shoppers the competitor took are still gone, and neither loyalty nor repairs won them back. Any claim that loyalty boosted sales should be checked against this age split.
- **Handed to D?** yes

## F3. The competitor took young shoppers and their shopping trips, not their spending per trip
- **Claim:** Between March and October 2024, compared with 2023: 27% fewer 18–24 year-olds shopped here, and those who did came 25% less often. What they spent per trip didn't change ($113). In 2025, the young shoppers who stayed came as often as before (+4%), but there were even fewer of them (−43% vs 2023).
- **Evidence:** section 3 of the A-1 notebook (sales = number of shoppers × trips per shopper × spend per trip)
- **Chart:** `results/a_competitor/a1_18_24_drivers.png`
- **Confidence / caveats:** high. Only people who bought something count as shoppers.
- **So what for the recommendation:** the problem is getting young people to come (and come back), not what they buy once they're here. Bigger perks mostly reward people who already shop here; they don't obviously bring lost young shoppers back. Number to track: 18–24 year-olds who shop here.
- **Handed to D?** yes

## F2. Leggings lost the most sales (−30%), in every age group; shoppers from Burnaby and Richmond cut back the most
- **Claim:** Leggings sales from March to October 2024 were $310K (30%) below 2023, about double any other product (shorts −15%, tank tops and sports bras −14%). The drop shows up in **every** age group (−16% to −58%), and only 35% of it came from 18–24 year-olds. That fits the case's description of the competitor undercutting prices on basic items. By where shoppers live, Burnaby (−26%) and Richmond (−25%) cut back most, against −10% to −17% elsewhere.
- **Evidence:** the product, neighbourhood and age-by-product tables, section 2 of the A-1 notebook
- **Chart:** `results/a_competitor/a1_hardest_hit_category_area.png`
- **Confidence / caveats:** high on the size of the drop. "Undercut basic items" comes from the case; we have no data on the competitor's prices.
- **So what for the recommendation:** leggings are where price competition hurts most, so protect them rather than spending on store-wide perks. By 2025 leggings sales had recovered for shoppers 35 and over (about 0% to −8%) but not for 18–24 year-olds (−61%).
- **Handed to D?** yes

## F1. Sales dropped the day the competitor opened (15 March 2024), and 18–24 year-olds took most of the hit
- **Claim:** The competitor opened on **15 March 2024**. Young shoppers (18–24) spent normally on 1–14 March (+2% vs the same days of 2023), then **50% less on 15–31 March**, and 45–54% less each month from April to August. March as a whole only shows −25%, because half the month came before the opening. Store sales from March to October 2024 were 17% ($681K) below 2023, and **18–24 year-olds caused 53% of that drop while making up only 19% of 2023 sales**. Looking only at March–May (before the loyalty program existed) gives the same picture: 18–24 −40%, 25–34 −22%, other ages −10% to −15%.
- **Evidence:** the month-by-month table, the day-by-day check either side of 15 March, and the March–May check, sections 1–2 of the A-1 notebook
- **Chart:** `results/a_competitor/a1_yoy_by_age.png`
- **Confidence / caveats:** high. The drop starts on the opening day itself. The March–October window includes two weeks before the opening (1–14 March), so it slightly understates the drop.
- **So what for the recommendation:** any "before vs after loyalty" comparison (loyalty started in June 2024) is distorted by the competitor arriving three months earlier. Compare the same months a year earlier, and look at each age group separately.
- **Handed to D?** yes

## Open questions
- ~~Is the 2026 drop in young shoppers real?~~ Answered in F10: yes, it's ongoing.
- All Stream A work is done: A-1, A-2 (must-haves), A-3 (should-have) and A-4 (did loyalty drive the recovery, and what young shoppers are worth).

## Decisions needed (also log them in `docs/decisions_log.md`)
- None. The competitor's opening date (15 March 2024) is now in `config.py` as `COMPETITOR_OPEN_DAY` and in the docs (decision #18).
