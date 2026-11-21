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
# # B · Loyalty program: revenue vs profit, points-funded returns, behaviour near the next tier (Q3, Q4, Q5)
# Consolidated version of `analysis/b_loyalty/loyalty_analysis.ipynb`, rebuilt on the shared table (`load()`) with the
# agreed definitions. Two changes from the first pass:
# 1. **B-1 is now a matched difference-in-differences.** The first pass compared "ever a member" with everyone else,
#    averaged over whoever happened to shop in each year. Here we keep only customers who shopped in **both** the 12
#    months before launch and the 12 months after, define members as those who **joined during that first year**, and
#    compare the change within age band × pre-launch spend quartile.
# 2. Charts are saved to `results/b_loyalty/` for slides 5–6.

# %%
import sys
from pathlib import Path

ROOT = Path.cwd().resolve()
while not (ROOT / "src").exists():
    ROOT = ROOT.parent
sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src import config as C
from src.metrics import load

OUT = C.RESULTS_DIR / "b_loyalty"
OUT.mkdir(exist_ok=True)
BLUE, ORANGE, INK2, GRID = "#2a78d6", "#eb6834", "#5f5e5a", "#e4e3df"
plt.rcParams.update({"axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
                     "grid.color": GRID, "axes.axisbelow": True, "font.size": 11})

df = load()
visits = df.groupby("transaction_id").agg(
    customer_id=("customer_id", "first"), date=("date", "first"),
    revenue=("revenue", "sum"), profit=("profit", "sum"), redeemed_dollars=("redeemed_dollars", "sum"),
).reset_index()

# %% [markdown]
# ## B-1 · Did loyalty raise revenue, and how much of it reached profit? (Q4)

# %%
L = C.LOYALTY_LAUNCH
pre = visits[(visits.date >= L - pd.DateOffset(years=1)) & (visits.date < L)]
post = visits[(visits.date >= L) & (visits.date < L + pd.DateOffset(years=1))]
cust = df[["customer_id", "age_band", "loyalty_join_date"]].drop_duplicates("customer_id").set_index("customer_id")

cols = ["revenue", "profit", "redeemed_dollars"]
t = (pre.groupby("customer_id")[cols].sum().add_suffix("_pre")
     .join(post.groupby("customer_id")[cols].sum().add_suffix("_post"), how="inner")   # active in both years
     .join(cust))
t["member"] = t.loyalty_join_date.notna() & (t.loyalty_join_date < L + pd.DateOffset(years=1))
t["spend_q"] = pd.qcut(t.revenue_pre, 4, labels=False)
t["d_rev"] = t.revenue_post - t.revenue_pre
t["d_prof"] = t.profit_post - t.profit_pre
print(f"Customers active in both years: {len(t):,} ({t.member.sum():,} joined in year 1)")

# Within each age band x spend quartile: member change minus non-member change, weighted by members
cell = t.groupby(["age_band", "spend_q", "member"])[["d_rev", "d_prof"]].mean().unstack("member")
w = t[t.member].groupby(["age_band", "spend_q"]).size()
did = pd.DataFrame({k: (cell[k][True] - cell[k][False]) for k in ["d_rev", "d_prof"]}).dropna()
w = w.reindex(did.index)
did_total = (did.mul(w, axis=0).sum() / w.sum()).rename({"d_rev": "revenue", "d_prof": "profit"})
did_age = did.mul(w, axis=0).groupby("age_band").sum().div(w.groupby("age_band").sum(), axis=0)
did_age.columns = ["revenue", "profit"]

raw = t.groupby("member")[["revenue_pre", "revenue_post", "profit_pre", "profit_post", "redeemed_dollars_post"]].mean()
print(raw.round(0))
print("Matched DiD per member ($/yr):", did_total.round(0).to_dict(),
      f"-> {did_total['profit'] / did_total['revenue']:.0%} of the extra revenue reaches profit")
print(did_age.round(0))

# %%
fig, ax = plt.subplots(figsize=(8, 4.5))
x = np.arange(len(did_age))
ax.bar(x - 0.2, did_age.revenue, 0.4, color=BLUE, label="Extra revenue per member")
ax.bar(x + 0.2, did_age.profit, 0.4, color=ORANGE, label="Extra profit per member")
ax.set_xticks(x, did_age.index)
ax.set_ylabel("$ per member, year after launch\nvs similar non-members")
ax.set_title("Members grew spend more than similar non-members, but they were already\n"
             "the keenest shoppers, so this is an upper bound on loyalty's effect", loc="left", fontsize=11)
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(OUT / "b1_matched_did.png", dpi=200)

# %% [markdown]
# **Cost of points over time.** Redeemed points as a share of revenue, by quarter.

# %%
since = visits[visits.date >= L].assign(qtr=lambda d: d.date.dt.to_period("Q"))
q = since.groupby("qtr")[["redeemed_dollars", "revenue"]].sum()
q["pct"] = q.redeemed_dollars / q.revenue * 100
last12 = visits[visits.date > C.AS_OF_DATE - pd.DateOffset(months=12)]
print(f"Redeemed points since launch: ${since.redeemed_dollars.sum():,.0f} "
      f"({since.redeemed_dollars.sum() / since.revenue.sum():.1%} of revenue); "
      f"last 12 months: ${last12.redeemed_dollars.sum():,.0f} "
      f"({last12.redeemed_dollars.sum() / last12.revenue.sum():.1%})")
print(q.pct.round(1))

fig, ax = plt.subplots(figsize=(8, 3.5))
q = q.iloc[1:-1]   # drop the partial first (Jun only) and last (Oct only) quarters
ax.plot(q.index.astype(str), q.pct, color=BLUE, marker="o")
ax.set_ylim(0, None)
ax.set_ylabel("Redeemed points, % of revenue")
ax.set_title("The cost of points keeps rising as balances build up", loc="left", fontsize=11)
fig.tight_layout()
fig.savefig(OUT / "b1_redemption_cost.png", dpi=200)

# %% [markdown]
# ## B-2 · Are items paid mostly with points returned more often? (Q5)

# %%
buy = df[df.row_type == C.PURCHASE].groupby("transaction_id").agg(revenue=("revenue", "sum"))
buy = buy.join(visits.set_index("transaction_id")["redeemed_dollars"])
buy = buy[buy.revenue > 0]
buy["points_share"] = (buy.redeemed_dollars / buy.revenue).clip(upper=1)
buy["bucket"] = pd.cut(buy.points_share, [-0.001, 0, 0.25, 0.5, 1.0], labels=["0%", "1–25%", "26–50%", ">50%"])
returned = set(df.loc[df.row_type == "Return", "original_transaction_id"].dropna())
buy["returned"] = buy.index.isin(returned)
b2 = buy.groupby("bucket", observed=True).agg(visits=("returned", "size"), return_rate=("returned", "mean"))
print(b2)

fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(b2.index.astype(str), b2.return_rate * 100, color=[BLUE] * 3 + [ORANGE])
for i, (r, n) in enumerate(zip(b2.return_rate, b2.visits)):
    ax.text(i, r * 100 + 0.5, f"{r:.0%}\n(n={n:,})", ha="center", fontsize=9, color=INK2)
ax.set_xlabel("Share of the purchase paid with points")
ax.set_ylabel("% of purchase visits with a return")
ax.set_title("Purchases paid mostly with points are returned 2.4× as often", loc="left", fontsize=11)
fig.tight_layout()
fig.savefig(OUT / "b2_return_rate_points.png", dpi=200)

# %% [markdown]
# ## B-3 · Do members spend more when they're close to the next tier? (Q3)

# %%
mv = df.assign(gross=np.where(df.row_type == C.PURCHASE, df.revenue, 0),
               is_buy=df.row_type == C.PURCHASE).groupby("transaction_id").agg(
    customer_id=("customer_id", "first"), date=("date", "first"), time=("time", "first"),
    join_date=("loyalty_join_date", "first"), points=("points_earned", "sum"),
    basket=("gross", "sum"), has_buy=("is_buy", "any"))
mv["ts"] = pd.to_datetime(mv.date.dt.strftime("%Y-%m-%d") + " " + mv.time.astype(str))
mv = mv.sort_values(["customer_id", "ts"]).reset_index()
mv["trailing"] = (mv.set_index("ts").groupby("customer_id")["points"]
                  .rolling(f"{C.TIER_WINDOW_DAYS}D", closed="left").sum().fillna(0).values)
m = mv[mv.has_buy & mv.join_date.notna() & (mv.date >= mv.join_date) & (mv.date >= L)].copy()
m["gap"] = np.where(m.trailing < C.SILVER_THRESHOLD, C.SILVER_THRESHOLD - m.trailing,
                    np.where(m.trailing < C.GOLD_THRESHOLD, C.GOLD_THRESHOLD - m.trailing, np.nan))
m = m.dropna(subset=["gap"])
m["bucket"] = pd.cut(m.gap, [0, 50, 100, 200, 400, np.inf], labels=["0–50", "50–100", "100–200", "200–400", "400+"],
                     right=False)
b3 = m.groupby("bucket", observed=True).agg(visits=("basket", "size"), basket=("basket", "mean"))
print(b3.round(0))

fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(b3.index.astype(str), b3.basket, color=BLUE)
ax.set_xlabel("Points still needed for the next tier")
ax.set_ylabel("Average basket ($)")
ax.set_title("Being close to the next tier doesn't change what members spend", loc="left", fontsize=11)
fig.tight_layout()
fig.savefig(OUT / "b3_basket_near_tier.png", dpi=200)
