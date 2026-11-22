"""Deck chart set: "field journal" style, built for a non-technical audience.

Run from the repo root:  python slides/deck_charts.py   -> PNGs in slides/charts/
Numbers follow the reconciled versions (docs/decisions_log.md #20-22).

Design rules (accessibility):
- Every chart says in plain words what it shows (the question it answers) at the top-left,
  and its axes are labelled in plain words ("out of 100 customers", not "churn rate").
- Data colours pass WCAG 3:1 against the paper background and were checked with the
  dataviz colour-blind validator. The two series colours (ink and brick) differ strongly in
  lightness, so they stay distinct for colour-blind viewers. Green and brick never encode
  two series in the same chart.
- Every coloured mark is also labelled with its value or name, so colour is never the only cue.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from src import config as C
from src.metrics import load

OUT = ROOT / "slides" / "charts"
OUT.mkdir(exist_ok=True)

PAPER = "#F4F1E8"     # background
INK = "#1B2A22"       # main text and the "comparison" series (13.3:1 on paper)
INK2 = "#4F564E"      # secondary text (6.7:1)
NEUTRAL = "#8F8A7A"   # context bars (3.1:1)
RULE = "#D9D4C5"      # gridlines only
BRICK = "#C9452A"     # the series we're warning about (4.3:1)
BRICK_TXT = "#B23A20" # brick for text (5.3:1)
GREEN = "#3D7A1E"     # gains / the program working (passes 3:1)
GREEN_LT = "#A9C98F"  # range shading for green

plt.rcParams.update({
    "figure.facecolor": PAPER, "axes.facecolor": PAPER, "savefig.facecolor": PAPER,
    "font.family": ["Segoe UI", "DejaVu Sans"], "font.size": 16,
    "text.color": INK, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "axes.edgecolor": RULE, "axes.grid": True, "axes.grid.axis": "y", "grid.color": RULE,
    "grid.linewidth": 0.8, "axes.axisbelow": True,
    "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False,
    "xtick.major.size": 0, "ytick.major.size": 0, "lines.solid_capstyle": "round", "text.parse_math": False,
})


def header(fig, question, note=None):
    """Plain-language 'what this chart shows' line (and optional how-to-read note)."""
    fig.text(0.012, 0.975, question, ha="left", va="top", fontsize=19, fontweight="bold", color=INK)
    if note:
        fig.text(0.012, 0.915, note, ha="left", va="top", fontsize=14, color=INK2)


def save(fig, name, top=0.84):
    fig.tight_layout(rect=(0, 0, 1, top))
    fig.savefig(OUT / name, dpi=200)
    plt.close(fig)
    print("saved", name)


df = load()
visits = df.groupby("transaction_id").agg(
    customer_id=("customer_id", "first"), date=("date", "first"), month=("month", "first"),
    revenue=("revenue", "sum"), redeemed_dollars=("redeemed_dollars", "sum"),
    is_repeat_visit=("is_repeat_visit", "first"),
).reset_index()

# ---------------------------------------------------------------- 1. timeline (slide 3)
events = [("Competitor opens\nacross the street", C.COMPETITOR_OPEN_DAY, BRICK_TXT, True),
          ("Loyalty program\nlaunches", C.LOYALTY_LAUNCH, GREEN, False),
          ("Pilates ad\ncampaign", C.PILATES_START, INK, False),
          ("Free repairs\nlaunch", C.REPAIRS_LAUNCH, GREEN, False),
          ("New website", C.WEBSITE_LAUNCH, INK, False),
          ("New store\nmanager", C.NEW_MANAGER, INK, False)]
fig, ax = plt.subplots(figsize=(16, 3.8))
ax.grid(False)
ax.axhline(0, color=INK, lw=2.5)
ax.axvspan(C.PILATES_START, C.PILATES_END, ymin=0.44, ymax=0.56, color=RULE)
for i, (lab, d, col, bold) in enumerate(events):
    up = i % 2 == 0
    ax.plot([d, d], [0, 0.5 if up else -0.5], color=col, lw=1.6)
    ax.scatter([d], [0], s=150, color=col, zorder=3, edgecolor=PAPER, linewidth=2)
    when = f"{d.day} {d:%b %Y}" if bold else f"{d:%b %Y}"
    ax.text(d, 0.58 if up else -0.58, f"{lab}\n{when}", ha="center", va="bottom" if up else "top",
            fontsize=14, color=col, fontweight="bold" if bold else "normal", linespacing=1.15)
for d, lab, ha in [(C.DATA_START, "Our data starts\nNov 2022", "left"), (C.DATA_END, "Today\nOct 2026", "right")]:
    ax.text(d, -0.14, lab, ha=ha, va="top", fontsize=12, color=INK2)
ax.set_xlim(C.DATA_START - pd.Timedelta(days=20), C.DATA_END + pd.Timedelta(days=20))
ax.set_ylim(-1.6, 1.6)
ax.axis("off")
save(fig, "s2_timeline.png", top=1)

# ---------------------------------------------------------------- 2. ARR (slide 5)
arr = visits[visits.is_repeat_visit].groupby("month")["revenue"].sum().rolling(12, min_periods=1).sum()
arr = arr[arr.index >= "2023-11-01"] / 1e6
fig, ax = plt.subplots(figsize=(14, 6.6))
ax.plot(arr.index, arr.values, color=INK, lw=3.5)
for d, lab in [(C.COMPETITOR_OPEN_DAY, "Competitor"), (C.LOYALTY_LAUNCH, "Loyalty"),
               (C.PILATES_START, "Pilates ads"), (C.REPAIRS_LAUNCH, "Repairs"),
               (C.WEBSITE_LAUNCH, "Website"), (C.NEW_MANAGER, "New manager")]:
    ax.axvline(d, color=NEUTRAL, lw=1, ls=(0, (2, 3)))
    ax.text(d + pd.Timedelta(days=6), 6.98, lab, color=INK2, fontsize=12, rotation=90, va="top")
pts = {"2024-02-01": ("$6.29M before\nthe competitor", "left", INK, 1),
       "2025-02-01": ("$5.53M low point", "center", BRICK_TXT, -1),
       "2026-10-01": ("$6.67M today", "right", INK, -2.5)}
for m, (lab, ha, col, up) in pts.items():
    v = arr[pd.Timestamp(m)]
    ax.scatter([pd.Timestamp(m)], [v], s=120, color=col, zorder=4, edgecolor=PAPER, linewidth=2)
    ax.text(pd.Timestamp(m), v + 0.09 * up, lab, ha=ha, va="bottom" if up > 0 else "top",
            fontsize=15, fontweight="bold", color=col)
ax.set_ylim(5.0, 7.0)
ax.set_yticks([5.0, 5.5, 6.0, 6.5, 7.0])
ax.yaxis.set_major_formatter(lambda x, _: f"${x:.1f}M")
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
header(fig, "Yearly sales from returning customers (ARR)",
       "Each point adds up the past 12 months of sales from customers who had shopped here before.")
save(fig, "s4_arr.png")

# ---------------------------------------------------------------- 3. 18-24 vs 25+ (slide 6)
buys = df[(df.row_type == C.PURCHASE) & df.date.dt.month.between(3, 10)].copy()
buys["grp"] = np.where(buys.age_band == "18-24", "Shoppers aged 18–24", "Shoppers aged 25+")
idx = buys.groupby([buys.date.dt.year, "grp"])["revenue"].sum().unstack()
chg = (idx / idx.loc[2023] - 1) * 100
fig, ax = plt.subplots(figsize=(8.5, 6.6))
for g, col in [("Shoppers aged 25+", INK), ("Shoppers aged 18–24", BRICK)]:
    ax.plot(chg.index, chg[g], color=col, lw=4, marker="o", ms=11, markeredgecolor=PAPER, markeredgewidth=2)
    v = chg[g].iloc[-1]
    ax.text(chg.index[-1] + 0.12, v, f"{g.replace('Shoppers aged ', 'Aged ')}\n{v:+.0f}%",
            color=col if col == INK else BRICK_TXT, fontsize=15, fontweight="bold", va="center")
ax.axhline(0, color=INK2, lw=1.2)
ax.text(2023, 3, "2023 level", color=INK2, fontsize=13)
ax.set_xticks(chg.index, [str(y) for y in chg.index])
ax.set_xlim(2022.8, 2026.75)
ax.set_ylim(-60, 35)
ax.yaxis.set_major_formatter(lambda x, _: "0%" if x == 0 else f"{x:+.0f}%")
ax.set_ylabel("Sales vs 2023")
header(fig, "How much each age group buys, compared with 2023",
       "Same months each year (March–October), so seasons don't distort it.")
save(fig, "s5_age_recovery.png")

# ---------------------------------------------------------------- 4. Pilates retention (slide 6)
cust = df[["customer_id", "signup_date", "acquisition_channel"]].drop_duplicates("customer_id")
cust = cust[cust.signup_date.between(C.PILATES_START, C.PILATES_END)]
v = visits.merge(cust, on="customer_id")
first_repeat = v[v.date > v.signup_date].groupby("customer_id")["date"].min()
cust["days"] = (cust.customer_id.map(first_repeat) - cust.signup_date).dt.days
cust["pil"] = cust.acquisition_channel == "Pilates Campaign"
ret = pd.DataFrame({m: cust.groupby("pil")["days"].apply(lambda s: (s <= m * 30.44).mean() * 100)
                    for m in [3, 6, 12]}).T
print("Pilates retention:\n", ret.round(0))
fig, ax = plt.subplots(figsize=(8.5, 6.6))
x = np.arange(3)
ax.bar(x - 0.21, ret[False], 0.4, color=INK, label="Other new customers (same weeks)")
ax.bar(x + 0.21, ret[True], 0.4, color=BRICK, label="Customers from the Pilates ads")
for i in range(3):
    ax.text(i - 0.21, ret[False].iloc[i] + 1.5, f"{ret[False].iloc[i]:.0f}", ha="center", fontsize=15, fontweight="bold")
    ax.text(i + 0.21, ret[True].iloc[i] + 1.5, f"{ret[True].iloc[i]:.0f}", ha="center", fontsize=15,
            fontweight="bold", color=BRICK_TXT)
ax.set_xticks(x, ["Within 3 months", "Within 6 months", "Within a year"])
ax.set_ylim(0, 100)
ax.set_ylabel("Out of 100 new customers")
ax.legend(frameon=False, loc="upper left", fontsize=13)
header(fig, "How many new customers came back for a second visit?")
save(fig, "s5_pilates.png", top=0.9)

# ---------------------------------------------------------------- 5. points cost (slide 7)
since = visits[visits.date >= C.LOYALTY_LAUNCH]
q = since.groupby(since.date.dt.to_period("Q"))[["redeemed_dollars", "revenue"]].sum()
q = (q.redeemed_dollars / q.revenue * 100).iloc[1:-1]
labels = [f"{'JASO'[0] if False else ''}{p.year}\nQ{p.quarter}" for p in q.index]
fig, ax = plt.subplots(figsize=(11, 6.2))
ax.bar(range(len(q)), q.values, 0.62, color=BRICK)
for i, v_ in enumerate(q.values):
    ax.text(i, v_ + 0.12, f"${v_:.1f}", ha="center", fontsize=14, fontweight="bold")
ax.set_xticks(range(len(q)), labels, fontsize=13)
ax.set_ylabel("$ of every $100 in sales")
ax.set_ylim(0, 7.8)
header(fig, "How much of every $100 in sales is paid with loyalty points",
       "It rose in the first year as more members reached Gold (now 69% of member spending), and has held at about $6 since.")
save(fig, "s6_points_cost.png")

# ---------------------------------------------------------------- 6. returns by points share (slide 7)
buy = df[df.row_type == C.PURCHASE].groupby("transaction_id")["revenue"].sum().to_frame()
buy = buy.join(visits.set_index("transaction_id")["redeemed_dollars"])
buy = buy[buy.revenue > 0]
buy["b"] = pd.cut((buy.redeemed_dollars / buy.revenue).clip(upper=1), [-0.001, 0, 0.25, 0.5, 1],
                  labels=["No points", "Up to\n1/4", "1/4 to\n1/2", "More than\nhalf"])
buy["ret"] = buy.index.isin(set(df.loc[df.row_type == "Return", "original_transaction_id"].dropna()))
r = buy.groupby("b", observed=True)["ret"].mean() * 100
fig, ax = plt.subplots(figsize=(7.5, 6.2))
ax.bar(r.index.astype(str), r.values, 0.6, color=[NEUTRAL] * 3 + [BRICK])
for i, v_ in enumerate(r.values):
    ax.text(i, v_ + 0.6, f"{v_:.0f}", ha="center", fontsize=17, fontweight="bold",
            color=BRICK_TXT if i == 3 else INK)
ax.set_xlabel("How much of the purchase was paid with points")
ax.set_ylabel("Out of 100 purchases")
ax.set_ylim(0, 28)
header(fig, "How many purchases get returned?")
save(fig, "s6_returns.png", top=0.9)

# ---------------------------------------------------------------- 7. repair effect (slide 8)
# Gap = extra customers (out of 100) who stopped shopping among non-users vs repair users.
fig, ax = plt.subplots(figsize=(10, 6.6))
ax.grid(axis="y", visible=False)
ax.grid(axis="x", color=RULE)
# Middle bar: review landmark design (decision #25): users = repaired by Sep 2025, among customers buying
# Apr-Sep 2025; matched on age x pre-launch spend x Apr-Sep 2025 visit frequency (-15.8 pts).
rows = [("All customers", 69.4, 69.4, NEUTRAL, "69"),
        ("Similar customers\n(same age, spending\n& visits)", 15.8, 15.8, NEUTRAL, "16"),
        ("Model-adjusted\nassociation\n(prediction model)", 5.3, 8.6, GREEN, "5 to 9")]
for i, (lab, lo, hi, col, txt) in enumerate(rows):
    y = len(rows) - 1 - i
    ax.barh(y, lo, 0.56, color=col)
    if hi > lo:
        ax.barh(y, hi - lo, 0.56, left=lo, color=GREEN_LT)
    ax.text(hi + 1.2, y, txt, va="center", fontsize=18, fontweight="bold", color=GREEN if col == GREEN else INK)
ax.set_yticks(range(len(rows)), [r_[0] for r_ in rows][::-1], fontsize=15, color=INK)
ax.set_xlim(0, 80)
ax.set_xlabel("Extra customers out of 100 who stopped shopping, without repairs")
header(fig, "How many more customers stop shopping if they don't use repairs?",
       "Most of the raw gap is because repair users were already keen shoppers. What's left still\n"
       "beats break-even: repairs pay for themselves if they keep 4.6 more customers in 100.")
ax.axvline(4.6, color=INK, lw=1.2, ls=(0, (2, 3)))
ax.text(5.2, 2.45, "Break-even (4.6)", color=INK2, fontsize=12)
ax.set_ylim(-0.5, 2.6)
save(fig, "s7_churn_gap.png", top=0.8)

# ---------------------------------------------------------------- 8. turnaround (slide 8)
t = pd.read_csv(ROOT / "results" / "c_repairs" / "c1_churn_turnaround.csv")
tv = t.iloc[:, :2].copy()
tv.columns = ["bucket", "churn"]
tv["churn"] *= 100
fig, ax = plt.subplots(figsize=(7.5, 6.2))
ax.bar(["10 days\nor less", "11 to 20\ndays", "More than\n20 days"], tv.churn, 0.58, color=[NEUTRAL, NEUTRAL, BRICK])
for i, v_ in enumerate(tv.churn):
    ax.text(i, v_ + 0.6, f"{v_:.0f}", ha="center", fontsize=17, fontweight="bold",
            color=BRICK_TXT if i == 2 else INK)
ax.set_xlabel("How long the repair took")
ax.set_ylabel("Out of 100 repair customers")
ax.set_ylim(0, 28)
header(fig, "How many repair customers stopped shopping?")
save(fig, "s7_turnaround.png", top=0.9)

# ---------------------------------------------------------------- 9. options compared (slide 9)
rev12 = visits[visits.date > C.AS_OF_DATE - pd.DateOffset(months=12)]
points_cut = rev12.redeemed_dollars.sum() - 0.05 * rev12.revenue.sum()
print(f"Bringing points back to 5% of sales saves ${points_cut:,.0f}")
# Win-back: 912 lost 18-24 buyers x $429 profit per young buyer today x 50% = $195K; lost revenue x today's
# margin x 50% = $166K; lost 18-24 ARR x margin x 50% = $154K (decision #23). Points: $0 if members cut
# spending in step, +$62K if they don't (decision #24).
# Repairs: 90% bootstrap range of the net effect across both churn models (d3 section 5 / summary section 6):
# logistic 5th pct -$123K, boosted-trees 95th pct +$83K. Central estimates: -$67K (logistic), +$55K (trees).
opts = [("Close free repairs\n(leadership's plan)", -123, 83, NEUTRAL,
         "−$123K to +$83K: about break-even,\nwith more room to lose than to gain"),
        ("Bring points back to\n5% of sales", 0, points_cut / 1e3, GREEN,
         f"$0 to +${points_cut / 1e3:.0f}K, depending on\nhow members respond"),
        ("Win back half of the\nlost 18–24 shoppers", 154, 195, GREEN,
         "+$154K to +$195K, before\nthe cost of the offer")]   # summary.ipynb section 9
fig, ax = plt.subplots(figsize=(14, 6.4))
ax.grid(axis="y", visible=False)
ax.grid(axis="x", color=RULE)
for i, (lab, lo, hi, col, txt) in enumerate(opts):
    y = len(opts) - 1 - i
    ax.barh(y, hi - lo, 0.5, left=lo, color=col, hatch="//", edgecolor=PAPER)
    ax.text(max(hi, 0) + 6, y, txt, va="center", fontsize=15, fontweight="bold", color=INK)
ax.axvline(0, color=INK, lw=1.5)
ax.text(2, 2.45, "No change", color=INK2, fontsize=12)
ax.set_yticks(range(len(opts)), [o[0] for o in opts][::-1], fontsize=15, color=INK)
ax.set_xlim(-150, 400)
ax.set_ylim(-0.5, 2.6)
ax.xaxis.set_major_formatter(lambda x, _: f"{'+' if x > 0 else ''}{'-' if x < 0 else ''}${abs(x):.0f}K")
ax.set_xlabel("Change in yearly profit")
header(fig, "What each option would do to yearly profit",
       "Right of the line = more profit. Repairs: 90% range across two prediction models. Others: low to high estimate.")
save(fig, "s8_financial.png")

# ---------------------------------------------------------------- 10. method diagram (slide 4)
from matplotlib.patches import FancyBboxPatch, Circle

fig = plt.figure(figsize=(17.2, 6.6))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 172)
ax.set_ylim(0, 66)
ax.axis("off")
cols = [
    (2, "Combine", "We joined the store's three files into one table, so every item sold is linked to who bought it and what it is."),
    (60, "Clean", None),
    (118, "Check", None),
]
for x0, title, _ in cols:
    ax.add_patch(FancyBboxPatch((x0, 2), 52, 60, boxstyle="round,pad=0,rounding_size=1.5", fc="#FFFDF7", ec=RULE, lw=1.2))
    ax.add_patch(Circle((x0 + 6, 55), 3.4, color=INK))
    ax.text(x0 + 6, 55, str(cols.index((x0, title, _)) + 1), color=PAPER, ha="center", va="center", fontsize=22, fontweight="bold")
    ax.text(x0 + 12, 55, title, ha="left", va="center", fontsize=26, fontweight="bold", color=INK)

# 1. Combine: three source boxes -> one table -> shopping trips
src = [("Sales", "351K transaction lines"), ("Products", "what each item is"), ("Customers", "14.4K people")]
for i, (a, b) in enumerate(src):
    y = 41 - i * 7.5
    ax.add_patch(FancyBboxPatch((6, y - 2.8), 20, 5.6, boxstyle="round,pad=0,rounding_size=0.8", fc=PAPER, ec=NEUTRAL, lw=1))
    ax.text(16, y + 0.9, a, ha="center", va="center", fontsize=14, fontweight="bold", color=INK)
    ax.text(16, y - 1.2, b, ha="center", va="center", fontsize=11, color=INK2)
    ax.annotate("", xy=(31, 33.5), xytext=(26.3, y), arrowprops=dict(arrowstyle="-", color=NEUTRAL, lw=1.2))
ax.add_patch(FancyBboxPatch((31, 29.5), 19, 8, boxstyle="round,pad=0,rounding_size=0.8", fc="#B8E62E", ec="none"))
ax.text(40.5, 33.5, "One table", ha="center", va="center", fontsize=16, fontweight="bold", color=INK)
ax.text(6, 17, "Then grouped into 190K shopping trips,\nso we can follow each customer over time.",
        ha="left", va="top", fontsize=14, color=INK, linespacing=1.5)

# 2. Clean
clean = ["Removed 1,016 sales that were\nrecorded twice",
         "Counted each repair's cost when\nthe item is dropped off",
         "Linked returns to purchases\nand pickups to drop-offs",
         "Added up loyalty points per trip\n(they were split across items)"]
for i, line in enumerate(clean):
    y = 45 - i * 10.5
    ax.text(64, y, "✓", ha="left", va="top", fontsize=18, color=GREEN, fontweight="bold")
    ax.text(68.5, y, line, ha="left", va="top", fontsize=14.5, color=INK, linespacing=1.4)

# 3. Check
check = [("Same months, every year", "December sells twice a normal month,\nso we never compare different seasons."),
         ("Similar customers only", "People choose to join programs, so we\ncompare them with look-alikes (age, spend)."),
         ("A prediction model + what-ifs", "To separate what a program causes from\nwho was going to stay anyway.")]
for i, (h, b) in enumerate(check):
    y = 46 - i * 14
    ax.text(122, y, h, ha="left", va="top", fontsize=15, fontweight="bold", color=INK)
    ax.text(122, y - 3.6, b, ha="left", va="top", fontsize=13, color=INK2, linespacing=1.4)
fig.savefig(OUT / "s3_method.png", dpi=200)
plt.close(fig)
print("saved s3_method.png")

# ---------------------------------------------------------------- 11. appendix A1/A2 (same numbers as summary.py section 11)
# Each chart fills one panel on the appendix slides (813 x 439 px, panel colour #F0EFE6); the slide carries the title.
PANEL = "#F0EFE6"
vfull = load("visits")
cust = load("customers").set_index("customer_id")


def panel():
    fig, ax = plt.subplots(figsize=(8.136, 4.392))
    fig.set_facecolor(PANEL)
    ax.set_facecolor(PANEL)
    for t in ax.get_xticklabels() + ax.get_yticklabels():
        t.set_fontsize(13)
    return fig, ax


def save_panel(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=200, facecolor=PANEL)
    plt.close(fig)
    print("saved", name)


# A1 left: profit per $100 of sales, members vs non-members, 12 months before vs after the loyalty launch
L = C.LOYALTY_LAUNCH
pre = vfull[(vfull.date >= L - pd.DateOffset(years=1)) & (vfull.date < L)]
post = vfull[(vfull.date >= L) & (vfull.date < L + pd.DateOffset(years=1))]
both = (pre.groupby("customer_id")[["revenue", "profit"]].sum().add_suffix("_pre")
        .join(post.groupby("customer_id")[["revenue", "profit"]].sum().add_suffix("_post"), how="inner"))
both["member"] = both.index.map(cust.loyalty_join_date).notna() & (both.index.map(cust.loyalty_join_date) < L + pd.DateOffset(years=1))
s = both.groupby("member")[["revenue_pre", "profit_pre", "revenue_post", "profit_post"]].sum()
p100 = pd.DataFrame({"before": s.profit_pre / s.revenue_pre * 100, "after": s.profit_post / s.revenue_post * 100})
fig, ax = panel()
x = np.arange(2)
for j, (col, colr, lab) in enumerate([("before", NEUTRAL, "12 months before launch"), ("after", GREEN, "12 months after launch")]):
    vals = [p100.loc[True, col], p100.loc[False, col]]
    ax.bar(x + (j - 0.5) * 0.36, vals, 0.34, color=colr, label=lab)
    for xi, v_ in zip(x, vals):
        ax.text(xi + (j - 0.5) * 0.36, v_ + 1, f"${v_:.1f}", ha="center", fontsize=14, fontweight="bold", color=INK)
ax.set_xticks(x, [f"Members\n(sales ${s.revenue_pre[True]/1e6:.2f}M → ${s.revenue_post[True]/1e6:.2f}M)",
                  f"Non-members\n(sales ${s.revenue_pre[False]/1e6:.2f}M → ${s.revenue_post[False]/1e6:.2f}M)"], fontsize=13, color=INK)
ax.set_ylim(0, 80)
ax.set_ylabel("Profit per $100 of sales", fontsize=13)
ax.legend(frameon=False, loc="upper right", fontsize=12, ncol=2)
save_panel(fig, "a1_profit_per_100.png")
print(f"Members: ${p100.loc[True, 'before']:.1f} -> ${p100.loc[True, 'after']:.1f} per $100")

# A1 right: basket index vs points still needed for the next tier
tx = (df.assign(gross=df.revenue.where(df.row_type == C.PURCHASE, 0), is_buy=df.row_type == C.PURCHASE)
      .groupby("transaction_id").agg(customer_id=("customer_id", "first"), datetime=("datetime", "first"),
                                     join_date=("loyalty_join_date", "first"), points=("points_earned", "sum"),
                                     basket=("gross", "sum"), has_buy=("is_buy", "any")))
tx = tx.sort_values(["customer_id", "datetime"]).reset_index()
tx["trailing"] = (tx.set_index("datetime").groupby("customer_id")["points"]
                  .rolling(f"{C.TIER_WINDOW_DAYS}D", closed="left").sum().fillna(0).values)
m = tx[tx.has_buy & tx.join_date.notna() & (tx.datetime >= tx.join_date) & (tx.datetime >= L)
       & (tx.trailing < C.GOLD_THRESHOLD)].copy()
m["silver"] = m.trailing < C.SILVER_THRESHOLD
m["gap"] = np.where(m.silver, C.SILVER_THRESHOLD, C.GOLD_THRESHOLD) - m.trailing
m["idx"] = m.basket / m.groupby("customer_id").basket.transform("mean") * 100
GAPS = ["0–50", "50–100", "100–200", "200–400", "400+"]
m["b"] = pd.cut(m.gap, [0, 50, 100, 200, 400, np.inf], labels=GAPS, right=False)
t = m.groupby(["silver", "b"], observed=True).idx.mean().unstack(0)
fig, ax = panel()
ax.axhline(100, color=INK2, lw=1.2, ls=(0, (3, 3)))
for silver, colr, lab in [(True, GREEN, "Member → Silver (600 pts)"), (False, BRICK, "Silver → Gold (2,000 pts)")]:
    ax.plot(range(5), t[silver].reindex(GAPS), marker="o", ms=8, lw=2.5, color=colr, label=lab)
ax.set_xticks(range(5), GAPS, fontsize=13, color=INK)
ax.set_xlabel("Points still needed for the next tier", fontsize=13)
ax.set_ylabel("Basket, % of own usual", fontsize=13)
ax.set_ylim(85, 115)
ax.text(-0.15, 92, "Dashed line = the customer's usual basket (100)", fontsize=11, color=INK2, ha="left")
ax.legend(frameon=False, loc="upper left", fontsize=12)
save_panel(fig, "a1_basket_vs_tier.png")

# A2 left: sales by category, Mar-Oct 2026 vs 2023, 18-24 vs 25+
p = df[(df.row_type == C.PURCHASE) & df.date.dt.month.between(3, 10) & df.date.dt.year.isin([2023, 2026])]
p = p.assign(yr=p.date.dt.year, grp=np.where(p.age_band == "18-24", "Aged 18–24", "Aged 25+"))
cat = p.groupby(["category", "grp", "yr"]).revenue.sum().unstack("yr")
cat = ((cat[2026] / cat[2023] - 1) * 100).unstack("grp").sort_values("Aged 18–24", ascending=False)
fig, ax = panel()
y = np.arange(len(cat))
ax.grid(axis="y", visible=False)
ax.grid(axis="x", color=RULE)
ax.barh(y + 0.2, cat["Aged 18–24"], 0.38, color=BRICK, label="Aged 18–24")
ax.barh(y - 0.2, cat["Aged 25+"], 0.38, color=INK, label="Aged 25+")
for yi, (a_, b_) in enumerate(zip(cat["Aged 18–24"], cat["Aged 25+"])):
    ax.text(a_ - 1.5, yi + 0.2, f"{a_:.0f}%", va="center", ha="right", fontsize=11, color=BRICK_TXT, fontweight="bold")
    ax.text(b_ + (1.5 if b_ >= 0 else -1.5), yi - 0.2, f"{b_:+.0f}%", va="center", ha="left" if b_ >= 0 else "right",
            fontsize=11, color=INK, fontweight="bold")
ax.axvline(0, color=INK, lw=1.2)
ax.set_yticks(y, cat.index, fontsize=12, color=INK)
ax.set_xlim(-80, 60)
ax.xaxis.set_major_formatter(lambda v, _: f"{v:+.0f}%" if v else "0%")
ax.set_xlabel("Change in sales, Mar–Oct 2026 vs Mar–Oct 2023", fontsize=13)
ax.legend(frameon=False, loc="upper right", fontsize=12)
save_panel(fig, "a2_categories.png")

# A2 right: sales by calendar month, 2023 and 2025 combined, average month = 100
v2 = vfull[vfull.date.dt.year.isin([2023, 2025])]
mon = v2.groupby(v2.date.dt.month).revenue.sum()
mon = mon / mon.mean() * 100
fig, ax = panel()
cols = [NEUTRAL] * 10 + [GREEN, GREEN]
ax.bar(range(12), mon.values, 0.7, color=cols)
for i, v_ in enumerate(mon.values):
    ax.text(i, v_ + 3, f"{v_:.0f}", ha="center", fontsize=11, color=INK, fontweight="bold" if i >= 10 else "normal")
ax.axhline(100, color=INK2, lw=1.2, ls=(0, (3, 3)))
ax.set_xticks(range(12), ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
              fontsize=12, color=INK)
ax.set_ylim(0, 225)
ax.set_ylabel("Sales index (average month = 100)", fontsize=13)
save_panel(fig, "a2_months.png")
