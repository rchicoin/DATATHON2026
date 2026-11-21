# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
# ---

# %% [markdown]
# # Lululime — Should leadership scrap repairs and expand loyalty?
# Dataverse 2026 · Final notebook. Edit `summary.py`, then generate the notebook with:
# `jupytext --to notebook summary.py -o summary.ipynb`, and run it top to bottom.

# %% [markdown]
# ## 1. Problem framing
# A competitor opened across the street in **March 2024** and targeted younger customers with lower prices.
# Lululime responded with a loyalty program (Jun 2024), a Pilates campaign (Jan–Mar 2025) and free repairs (Apr 2025).
# Revenue has since recovered. Leadership credits loyalty and plans to **expand loyalty perks and shut down free repairs**,
# believing repairs only cost money and cannibalize outerwear sales.
#
# We test that plan through two numbers:
# - **ARR:** revenue from repeat customers (any visit after their signup date) over the trailing 12 months.
# - **Profit:** revenue − production costs − repair costs − redeemed points ($1 per 20 points).

# %%
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
import pandas as pd

from src import config as C
from src.metrics import load

# Shared chart style (validated palette: blue / orange; recessive grid)
BLUE, ORANGE = "#2a78d6", "#eb6834"
INK, INK2, GRID = "#0b0b0b", "#5f5e5a", "#e4e3df"
plt.rcParams.update({
    "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb", "font.size": 11,
    "axes.edgecolor": GRID, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "axes.axisbelow": True,
    "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False,
    "lines.linewidth": 2,
})
EVENT_LABELS = {
    "competitor_open": "Competitor opens", "loyalty_launch": "Loyalty launch",
    "pilates_start": "Pilates push", "repairs_launch": "Free repairs",
    "website_launch": "Website", "new_manager": "New manager",
}


def mark_events(ax, ymax):
    """Dashed vertical line and label for each initiative."""
    for i, (key, label) in enumerate(EVENT_LABELS.items()):
        d = C.EVENTS[key]
        ax.axvline(d, color=INK2, lw=0.8, ls=(0, (3, 3)), zorder=1)
        ax.text(d, ymax * (0.995 - 0.035 * (i % 2)), " " + label, color=INK2, fontsize=9, va="top")
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 5, 9]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))

# %% [markdown]
# ## 2. Data & methodology
# All cleaning and joining lives in `src/` (rules in `docs/data_notes.md`, decisions in `docs/decisions_log.md`):
# 1. **Clean:** drop 1,016 exact duplicate sales rows; blank tier before the loyalty launch = "Pre-loyalty"; blank points = 0.
# 2. **Join:** sales → items on `item_id`, → customers on `customer_id` (left joins, one-to-one lookup check).
# 3. **Baskets:** lines grouped by `transaction_id` into visits; `points_redeemed` summed per transaction.
# 4. **Metrics:** profit per line; repair cost at drop-off only (unpicked drop-offs still count); returns and repair
#    pickups linked to their original on `original_transaction_id` + `item_id`.
#
# The build below reruns every step from the raw CSVs and prints the integrity checks.

# %%
from src.tables import build_all
_ = build_all(write=False)

# %%
lines = load()                      # one row per sales line (the shared, cleaned, joined table)
visits = load("visits")             # one row per transaction (basket)
customers = load("customers")       # one row per customer: churn, ARR, repair use, membership
customer_month = load("customer_month")
print(f"{len(lines):,} lines · {len(visits):,} visits · {len(customers):,} customers")

# %% [markdown]
# ## 3. ARR over time (Stream D, slide 3)
# ARR fell for a year after the competitor opened, then recovered to a new high. Plotted from Nov 2023, the first
# month with a full 12 months of history. ARR is a rolling total, so it lags real changes by up to a year.

# %%
arr = customer_month.groupby("month")["arr_12m"].sum()
arr = arr[arr.index >= "2023-11-01"]
trough_m = arr.idxmin()

pd.Series({
    "ARR at competitor open, Mar 2024 ($M)": arr[C.COMPETITOR_OPEN] / 1e6,
    f"ARR low, {trough_m:%b %Y} ($M)": arr.min() / 1e6,
    "ARR Oct 2026 ($M)": arr.iloc[-1] / 1e6,
    "Change from low to Oct 2026 (%)": (arr.iloc[-1] / arr.min() - 1) * 100,
}).round(2)

# %%
fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(arr.index, arr / 1e6, color=BLUE)
ax.plot([trough_m, arr.index[-1]], [arr.min() / 1e6, arr.iloc[-1] / 1e6], "o", color=BLUE, ms=8,
        mec="#fcfcfb", mew=2, zorder=3)
ax.annotate(f"Low: ${arr.min()/1e6:.2f}M\n({trough_m:%b %Y})", (trough_m, arr.min() / 1e6),
            xytext=(0, -38), textcoords="offset points", ha="center", color=INK, fontsize=10)
ax.annotate(f"${arr.iloc[-1]/1e6:.2f}M", (arr.index[-1], arr.iloc[-1] / 1e6),
            xytext=(-8, 10), textcoords="offset points", ha="right", color=INK, fontsize=10)
ax.set_ylim(5.0, 7.0)
mark_events(ax, 7.0)
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x:.1f}M"))
ax.set_title("ARR fell for a year after the competitor opened, then recovered to a new high",
             loc="left", color=INK, fontsize=13)
ax.set_ylabel("ARR (trailing 12 months, repeat customers)")
fig.tight_layout()
plt.show()

# %% [markdown]
# **What drove the recovery?** Each month's repeat revenue and active repeat customers, compared with the **same
# calendar month in Mar 2023 – Feb 2024** (the year before the competitor), which removes seasonality.
# Revenue is back above pre-competitor levels, but customers are not: the recovery is fewer customers spending more.

# %%
rv = visits[visits["is_repeat_visit"]]
g = rv.groupby("month").agg(revenue=("revenue", "sum"), customers=("customer_id", "nunique"))
base = g.loc["2023-03-01":"2024-02-01"].copy()
base.index = base.index.month

rows = {}
for name, (a, b) in {"Year 1 (Mar 2024 – Feb 2025)": ("2024-03-01", "2025-02-01"),
                     "Year 2 (Mar 2025 – Feb 2026)": ("2025-03-01", "2026-02-01"),
                     "Year 3 so far (Mar – Oct 2026)": ("2026-03-01", "2026-10-01")}.items():
    p, bm = g.loc[a:b], base.loc[g.loc[a:b].index.month]
    rows[name] = {
        "repeat revenue vs pre-competitor (%)": (p.revenue.sum() / bm.revenue.sum() - 1) * 100,
        "active repeat customers vs pre-competitor (%)": (p.customers.mean() / bm.customers.mean() - 1) * 100,
        "revenue per active customer vs pre-competitor (%)":
            ((p.revenue.sum() / p.customers.sum()) / (bm.revenue.sum() / bm.customers.sum()) - 1) * 100,
    }
pd.DataFrame(rows).T.round(1)

# %%
post = g.loc["2024-03-01":]
idx = (post.div(base.loc[post.index.month].values) * 100).rolling(3, min_periods=1).mean()

fig, ax = plt.subplots(figsize=(11, 5))
ax.axhline(100, color=INK2, lw=1)
for col, colr, lab in [("revenue", BLUE, "Repeat revenue"), ("customers", ORANGE, "Active repeat customers")]:
    ax.plot(idx.index, idx[col], color=colr, label=lab)
    ax.annotate(f"{lab}: {idx[col].iloc[-1]:.0f}", (idx.index[-1], idx[col].iloc[-1]), xytext=(6, 0),
                textcoords="offset points", va="center", color=INK, fontsize=10)
ax.text(pd.Timestamp("2026-10-01"), 99, "Pre-competitor level = 100", color=INK2, fontsize=9, va="top", ha="right")
ax.set_ylim(70, 125)
mark_events(ax, 125)
ax.legend(loc="lower right", frameon=False)
ax.set_xlim(idx.index[0], idx.index[-1] + pd.Timedelta(days=200))
ax.set_title("Revenue is back above pre-competitor levels, but customers are not", loc="left", color=INK, fontsize=13)
ax.set_ylabel("Index vs same month, Mar 2023 – Feb 2024 (3-month avg)")
fig.tight_layout()
plt.show()

# %% [markdown]
# ## 4. Competitor impact & seasonality (Stream A, slide 4)

# %%

# %% [markdown]
# ## 5. Loyalty program: revenue vs profit, points-funded returns (Stream B, slides 5-6)

# %%

# %% [markdown]
# ## 6. Repairs: churn and cost vs ARR at risk, with scenarios (Stream C, slides 7-8)

# %%

# %% [markdown]
# ## 7. Pilates campaign (Stream D, slide 9)
# Customers who signed up during the campaign (Jan 6 – Mar 31, 2025): the 360 from the Pilates campaign vs the 417
# from other channels in the **same weeks**, so season and store conditions match. The data has no campaign cost,
# so this measures value delivered, not ROI.

# %%
cohort = customers[customers["signup_date"].between(C.PILATES_START, C.PILATES_END)].copy()
cohort["group"] = cohort["acquisition_channel"].eq("Pilates Campaign").map(
    {True: "Pilates Campaign", False: "Other channels, same weeks"})

pv = visits.merge(cohort[["customer_id", "group"]], on="customer_id")
pv["days"] = (pv["date"] - pv["signup_date"]).dt.days
for d in [90, 180, 365]:
    cohort[f"came_back_{d}d"] = cohort["customer_id"].isin(pv.loc[pv["days"].between(1, d), "customer_id"])
cohort["one_visit_only"] = cohort["n_visits"] == 1
cohort["last_visit_in_campaign"] = cohort["last_visit"] <= C.PILATES_END

first_year = (pv[pv["days"] <= 365].groupby(["customer_id", "group"])
              .agg(revenue=("revenue", "sum"), profit=("profit", "sum")).reset_index())
pilates = pd.concat([
    cohort.groupby("group")[["came_back_90d", "came_back_180d", "came_back_365d", "one_visit_only",
                             "last_visit_in_campaign", "churned"]].mean().mul(100).round(1),
    first_year.groupby("group")[["revenue", "profit"]].mean().round(0).add_prefix("first_year_").add_suffix("_per_customer"),
    cohort.groupby("group")["arr_12m"].mean().round(0).rename("arr_now_per_customer"),
], axis=1)
pilates.T

# %%
pv["month_after"] = pv["days"] // 30
curve = (pv[pv["month_after"].between(1, 18)].groupby(["group", "month_after"])["customer_id"].nunique()
         .unstack(0).div(cohort.groupby("group").size()) * 100)

fig, ax = plt.subplots(figsize=(11, 5))
for name, colr in [("Other channels, same weeks", BLUE), ("Pilates Campaign", ORANGE)]:
    ax.plot(curve.index, curve[name], color=colr, label=name, marker="o", ms=5, mec="#fcfcfb", mew=1.5)
    ax.annotate(f"{name}: {curve[name].iloc[-1]:.0f}%", (curve.index[-1], curve[name].iloc[-1]), xytext=(8, 0),
                textcoords="offset points", va="center", color=INK, fontsize=10)
ax.set_xlim(0.5, 24)
ax.set_xticks(range(1, 19, 2))
ax.set_ylim(0, 35)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax.set_xlabel("Months after signup")
ax.set_ylabel("Share of customers who visited that month")
ax.legend(loc="upper right", frameon=False)
p, o = pilates.loc["Pilates Campaign"], pilates.loc["Other channels, same weeks"]
ax.set_title(f"Pilates-campaign customers didn't stick: {p['came_back_365d']:.0f}% came back within a year "
             f"vs {o['came_back_365d']:.0f}%", loc="left", color=INK, fontsize=13)
fig.tight_layout()
plt.show()

# %% [markdown]
# ## 8. Recommendation, KPIs & risks (Stream D, slide 10)
# *To fill after the 2:00 check-in, from every stream's `results/<stream>/findings.md`.*
#
# **Recommendation:** [one line]
#
# | Area | Recommendation | KPI to track (target) | Risk to watch |
# |---|---|---|---|
# | Repairs | [keep / scrap / fix turnaround, from C-2] | [churn of repair users vs non-users; turnaround ≤ __ days] | [repair cost growing faster than retained ARR] |
# | Loyalty | [expand / redesign, from B-1] | [profit per member after redemptions; redemption cost ≤ __% of revenue] | [points-funded purchases returned more (B-2)] |
# | Acquisition | Judge campaigns on retention, not sign-ups | 6- and 12-month return rate of new customers (Pilates: 52% vs 81%) | Campaign customers churn after the offer ends |
# | Customer base | [win back 18–24s, from A-1] | ARR and active repeat customers vs pre-competitor level (now 94) | Growth depends on fewer, older customers spending more |
#
# **Limitations:** members and repair users choose to take part, so matched comparisons reduce but don't remove
# selection bias; ARR lags real changes by up to 12 months; the data has no campaign or program running costs
# beyond repairs and redeemed points.
