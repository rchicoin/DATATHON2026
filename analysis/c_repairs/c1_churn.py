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
# # C-1 · Do repair users churn less? Does turnaround matter? (Q8)
# Stream C, slide 7. Method: `docs/who_answers_what.md` (Person C).
#
# - **Cohort:** customers with a visit in the year before repairs launched (2024-04-01 to 2025-03-31).
# - **Matching:** compare users vs non-users within age band × pre-period spend quartile, then weight each cell by its number of repair users. This gives the gap for the kind of customer who uses repairs.
# - **Robustness checks:** (a) churn from purchase visits only, because a pickup trip counts as a visit; (b) only customers who still bought something after launch, because many non-users had already lapsed before repairs existed.

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
from src import tables as T
from src.metrics import load

OUT = C.RESULTS_DIR / "c_repairs"
OUT.mkdir(parents=True, exist_ok=True)

# Load the shared CSV once and build the tables from it (same code as load("visits") etc.)
lines = load()
visits = T.build_visits(lines)
links = T.build_links(lines)
customers = load("customers").set_index("customer_id")

# %% [markdown]
# ## Cohort: active in the year before launch

# %%
PRE_START = C.REPAIRS_LAUNCH - pd.DateOffset(years=1)
PRE_END = C.REPAIRS_LAUNCH - pd.Timedelta(days=1)

pre = visits[visits["date"].between(PRE_START, PRE_END)]
coh = customers.loc[pre["customer_id"].unique()].copy()
coh["pre_spend"] = pre.groupby("customer_id")["revenue"].sum()
# rank first so ties don't break the quartile edges
coh["spend_q"] = pd.qcut(coh["pre_spend"].rank(method="first"), 4, labels=["Q1", "Q2", "Q3", "Q4"])

# Churn from purchase visits only (robustness: pickups and drop-offs don't keep you "active")
last_purchase = visits[visits["has_purchase"]].groupby("customer_id")["date"].max()
coh["churned_purchase"] = (C.AS_OF_DATE - coh.index.map(last_purchase)).days > C.CHURN_DAYS

# Purchases after launch (robustness: was the customer still around when repairs existed?)
post = visits[(visits["date"] >= C.REPAIRS_LAUNCH) & visits["has_purchase"]]
coh["post_purchases"] = post.groupby("customer_id").size().reindex(coh.index).fillna(0)

print(f"Cohort: {len(coh):,} customers, {coh['used_repair'].sum():,} repair users "
      f"(of {customers['used_repair'].sum():,} total)")
print(f"Non-users whose last visit was before repairs launched: "
      f"{(coh.loc[~coh['used_repair'], 'last_visit'] < C.REPAIRS_LAUNCH).mean():.0%}")

# %% [markdown]
# ## Matched churn gap

# %%
def matched_churn(d: pd.DataFrame, col: str = "churned") -> dict:
    """Churn of users vs non-users within age band × spend quartile, weighted by users per cell."""
    g = (d.groupby(["age_band", "spend_q", "used_repair"], observed=True)[col]
          .agg(["mean", "size"]).unstack("used_repair").dropna())
    w = g[("size", True)]
    users = (g[("mean", True)] * w).sum() / w.sum()
    non = (g[("mean", False)] * w).sum() / w.sum()
    return {"users": users, "non_users": non, "gap": users - non,
            "n_users": int(w.sum()), "n_non_users": int(g[("size", False)].sum())}

still_buying = coh[coh["post_purchases"] >= 1]
rows = {
    "Raw (whole cohort)": {
        "users": coh.loc[coh["used_repair"], "churned"].mean(),
        "non_users": coh.loc[~coh["used_repair"], "churned"].mean(),
        "n_users": int(coh["used_repair"].sum()), "n_non_users": int((~coh["used_repair"]).sum())},
    "Matched": matched_churn(coh),
    "Matched, purchase visits only": matched_churn(coh, "churned_purchase"),
    "Matched, still buying after launch": matched_churn(still_buying),
    "Matched, still buying, purchase visits only": matched_churn(still_buying, "churned_purchase"),
}
churn_tbl = pd.DataFrame(rows).T
churn_tbl["gap"] = churn_tbl["users"] - churn_tbl["non_users"]
churn_tbl.to_csv(OUT / "c1_churn_gap.csv")
churn_tbl.style.format({"users": "{:.1%}", "non_users": "{:.1%}", "gap": "{:+.1%}",
                        "n_users": "{:,.0f}", "n_non_users": "{:,.0f}"})

# %%
# Gap handed to C-2. Conservative choice: matched AND non-users still buying after launch,
# so we don't credit repairs for customers who left before the program existed.
GAP_FOR_C2 = churn_tbl.loc["Matched, still buying after launch", "gap"]
print(f"Churn gap used in C-2: {GAP_FOR_C2:+.1%} "
      f"(plain matched gap: {churn_tbl.loc['Matched', 'gap']:+.1%})")

# %% [markdown]
# ## Turnaround: each user's median days from drop-off to pickup

# %%
rep = links[(links["link_type"] == "repair") & links["resolved"]]
median_days = rep.groupby("customer_id")["days_between"].median()
BUCKETS = ["≤10 days", "11–20 days", ">20 days"]
users_t = customers.loc[median_days.index].assign(
    bucket=pd.cut(median_days, [-np.inf, 10, 20, np.inf], labels=BUCKETS))
turn_tbl = users_t.groupby("bucket", observed=True).agg(
    churn=("churned", "mean"), n=("churned", "size"), avg_dropoffs=("n_repair_dropoffs", "mean"))
turn_tbl.to_csv(OUT / "c1_churn_turnaround.csv")
print(f"Turnaround: median {rep['days_between'].median():.0f} days, "
      f"{rep['days_between'].min():.0f}–{rep['days_between'].max():.0f} range")
turn_tbl.style.format({"churn": "{:.1%}", "n": "{:,.0f}", "avg_dropoffs": "{:.1f}"})

# %% [markdown]
# ## Charts (slide 7)

# %%
USERS, NON, INK, MUTED, SURFACE = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#fcfcfb"
plt.rcParams.update({"font.size": 11, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED, "figure.facecolor": SURFACE,
                     "axes.facecolor": SURFACE})

def tidy(ax):
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.yaxis.grid(True, color="#e4e3df", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0%}")

show = ["Raw (whole cohort)", "Matched", "Matched, still buying after launch"]
labels = ["Raw", "Matched on age\n+ pre-launch spend", "Matched, and still\nbuying after launch"]
x = np.arange(len(show)); wbar = 0.36
fig, ax = plt.subplots(figsize=(8, 4.5))
for off, col, colour, name in [(-wbar / 2, "users", USERS, "Repair users"),
                               (wbar / 2, "non_users", NON, "Non-users")]:
    vals = churn_tbl.loc[show, col].astype(float)
    ax.bar(x + off, vals, wbar - 0.02, color=colour, label=name)
    for xi, v in zip(x + off, vals):
        ax.text(xi, v + 0.015, f"{v:.0%}", ha="center", color=INK, fontsize=10)
ax.set_xticks(x, labels)
ax.set_ylim(0, 1)
ax.set_ylabel("Churned (no visit in 180 days)")
ax.set_title("Repair users churn far less, even against similar customers",
             loc="left", color=INK, fontsize=13)
ax.legend(frameon=False, loc="upper right")
tidy(ax)
fig.tight_layout()
fig.savefig(OUT / "c1_churn_matched.png", dpi=200)

# %%
fig, ax = plt.subplots(figsize=(6.5, 4.2))
bars = ax.bar(turn_tbl.index.astype(str), turn_tbl["churn"], 0.55, color=USERS)
for b, (_, r) in zip(bars, turn_tbl.iterrows()):
    ax.text(b.get_x() + b.get_width() / 2, r["churn"] + 0.006,
            f"{r['churn']:.0%}\n(n={r['n']:,.0f})", ha="center", color=INK, fontsize=10)
ax.set_ylim(0, max(0.3, turn_tbl["churn"].max() * 1.3))
ax.set_ylabel("Churned (no visit in 180 days)")
ax.set_xlabel("User's median repair turnaround")
ax.set_title("Churn roughly doubles when repairs take over 20 days",
             loc="left", color=INK, fontsize=13)
tidy(ax)
fig.tight_layout()
fig.savefig(OUT / "c1_churn_turnaround.png", dpi=200)
