# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # C-3 · Do free repairs cannibalize outerwear sales? (Stream C should-have)
# Leadership believes repairs "cannibalize outerwear sales": a fixed jacket is a new jacket not bought.
#
# 1. **Store level:** did outerwear revenue fall after repairs launched, compared with other categories?
# 2. **Customer level:** did customers who repaired outerwear buy less outerwear afterwards? The comparison group
#    is customers who repaired **only activewear**. They're similar people (engaged enough to use repairs, repair
#    timing spread over the same months), but their repairs can't replace a jacket. If outerwear repairs
#    cannibalize, outerwear repairers' outerwear spend should fall *more* than this group's.
#
# Windows are the 12 months before vs the 12 months after each customer's first repair, so every customer is
# compared over a full year and seasonality cancels out. Only customers whose first repair was at least 12 months
# before the data ends (by Oct 2025) are included.

# %%
import sys
from pathlib import Path

ROOT = Path.cwd().resolve()
while not (ROOT / "src").exists():
    ROOT = ROOT.parent
sys.path.insert(0, str(ROOT))

import pandas as pd
import matplotlib.pyplot as plt

from src import config as C
from src.metrics import load

OUT = C.RESULTS_DIR / "c_repairs"
lines = load()
customers = load("customers").set_index("customer_id")

OUTERWEAR_REPAIR = [k for k, v in C.REPAIR_ITEMS.items() if v == "outerwear"][0]
ACTIVEWEAR_REPAIR = [k for k, v in C.REPAIR_ITEMS.items() if v == "activewear"][0]

# Net sales (purchases minus returns), excluding repair rows
sales = lines[lines["row_type"].isin([C.PURCHASE, C.RETURN])].copy()
sales["m"] = sales["date"].dt.to_period("M")
sales["is_outerwear"] = sales["category"] == "Outerwear"

# %% [markdown]
# ## 1. Store level: 12 months before vs after launch, by category

# %%
YEAR = pd.DateOffset(years=1)
before = sales["date"].between(C.REPAIRS_LAUNCH - YEAR, C.REPAIRS_LAUNCH - pd.Timedelta(days=1))
after = sales["date"].between(C.REPAIRS_LAUNCH, C.REPAIRS_LAUNCH + YEAR - pd.Timedelta(days=1))
cat = pd.DataFrame({"Before ($)": sales[before].groupby("category")["revenue"].sum(),
                    "After ($)": sales[after].groupby("category")["revenue"].sum()})
cat["Change (%)"] = (cat["After ($)"] / cat["Before ($)"] - 1) * 100
cat = cat.sort_values("Change (%)")

# Who drove the outerwear drop? Split outerwear revenue by whether the customer ever used repairs.
ow = sales[sales["is_outerwear"]].copy()
ow["group"] = ow["customer_id"].map(customers["used_repair"]).map({True: "Repair users", False: "Never used repairs"})
ow_split = pd.DataFrame({"Before ($)": ow[before[ow.index]].groupby("group")["revenue"].sum(),
                         "After ($)": ow[after[ow.index]].groupby("group")["revenue"].sum()})
ow_split["Change (%)"] = (ow_split["After ($)"] / ow_split["Before ($)"] - 1) * 100
display(cat.round(0))
ow_split.round(0)

# %% [markdown]
# ## 2. Customer level: outerwear repairers vs activewear-only repairers

# %%
dropoffs = lines[lines["row_type"] == C.DROPOFF]
first_ow = dropoffs[dropoffs["item_id"] == OUTERWEAR_REPAIR].groupby("customer_id")["date"].min().dt.to_period("M")
first_aw = dropoffs[dropoffs["item_id"] == ACTIVEWEAR_REPAIR].groupby("customer_id")["date"].min().dt.to_period("M")
first_aw_only = first_aw[~first_aw.index.isin(first_ow.index)]
LAST_START = (C.AS_OF_DATE - pd.DateOffset(months=12)).to_period("M")   # need 12 full months after
MONTHS = pd.period_range(C.DATA_START, C.AS_OF_DATE, freq="M")

ow_m = sales[sales["is_outerwear"]].groupby(["customer_id", "m"])["revenue"].sum()
all_m = sales.groupby(["customer_id", "m"])["revenue"].sum()


def before_after(first: pd.Series) -> pd.DataFrame:
    """Per customer: outerwear and total spend in the 12 months before vs from the month of their first repair."""
    first = first[first <= LAST_START]
    ids = list(first.index)
    o = ow_m[ow_m.index.isin(ids, level=0)].unstack().reindex(index=ids, columns=MONTHS).fillna(0)
    a = all_m[all_m.index.isin(ids, level=0)].unstack().reindex(index=ids, columns=MONTHS).fillna(0)
    rows = []
    for cid, m in first.items():
        pre, post = pd.period_range(m - 12, m - 1, freq="M"), pd.period_range(m, m + 11, freq="M")
        rows.append({"customer_id": cid, "ow_before": o.loc[cid, pre].sum(), "ow_after": o.loc[cid, post].sum(),
                     "all_before": a.loc[cid, pre].sum(), "all_after": a.loc[cid, post].sum()})
    return pd.DataFrame(rows).set_index("customer_id")


def summarise(r: pd.DataFrame) -> dict:
    m = r.mean()
    other_before, other_after = m["all_before"] - m["ow_before"], m["all_after"] - m["ow_after"]
    return {"Customers": len(r),
            "Outerwear $/customer, before": m["ow_before"], "Outerwear $/customer, after": m["ow_after"],
            "Outerwear change (%)": (m["ow_after"] / m["ow_before"] - 1) * 100,
            "Other categories change (%)": (other_after / other_before - 1) * 100,
            "Outerwear share of spend, before (%)": m["ow_before"] / m["all_before"] * 100,
            "Outerwear share of spend, after (%)": m["ow_after"] / m["all_after"] * 100,
            "Bought any outerwear, before (%)": (r["ow_before"] > 0).mean() * 100,
            "Bought any outerwear, after (%)": (r["ow_after"] > 0).mean() * 100}


cust_tbl = pd.DataFrame({"Repaired outerwear": summarise(before_after(first_ow)),
                         "Repaired activewear only": summarise(before_after(first_aw_only))})
cust_tbl.loc["Outerwear share change (pts)"] = (cust_tbl.loc["Outerwear share of spend, after (%)"]
                                                - cust_tbl.loc["Outerwear share of spend, before (%)"])
cust_tbl.to_csv(OUT / "c3_cannibalization.csv")
cust_tbl.round(1)

# %% [markdown]
# ## Chart

# %%
BLUE, ORANGE, INK, MUTED, GRID, SURFACE = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
plt.rcParams.update({"font.size": 11, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED,
                     "ytick.color": MUTED, "figure.facecolor": SURFACE, "axes.facecolor": SURFACE})

fig, ax = plt.subplots(figsize=(8, 4.6))
groups = ["Repaired outerwear", "Repaired activewear only"]
rows_ = ["Outerwear change (%)", "Other categories change (%)"]
x = range(len(groups)); w = 0.36
for i, (row, colour, name) in enumerate([(rows_[0], ORANGE, "Outerwear spend"),
                                          (rows_[1], BLUE, "Spend on everything else")]):
    xs = [xi + (i - 0.5) * w for xi in x]
    vals = cust_tbl.loc[row, groups].astype(float)
    ax.bar(xs, vals, w - 0.02, color=colour, label=name)
    for xi, v in zip(xs, vals):
        ax.text(xi, v + (1.5 if v >= 0 else -4.5), f"{v:+.0f}%", ha="center", color=INK, fontsize=10)
ax.axhline(0, color=MUTED, linewidth=1)
ax.set_ylim(-28, 48)
ax.tick_params(axis="x", length=0, pad=10)
ax.set_xticks(list(x), [f"{g}\n(n={cust_tbl.loc['Customers', g]:,.0f})" for g in groups])
ax.spines[["top", "right", "left"]].set_visible(False)
ax.yaxis.grid(True, color=GRID, linewidth=0.8)
ax.set_axisbelow(True)
ax.yaxis.set_major_formatter(lambda v, _: f"{v:+.0f}%")
ax.set_ylabel("12 months after first repair vs 12 before")
ax.set_title("Repairing a jacket didn't cut jacket buying more than\nfor other repair users",
             loc="left", color=INK, fontsize=13)
ax.legend(frameon=False, loc="upper right", ncol=2)
fig.tight_layout()
fig.savefig(OUT / "c3_cannibalization.png", dpi=200)
