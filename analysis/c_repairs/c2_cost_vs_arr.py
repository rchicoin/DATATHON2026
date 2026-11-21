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
# # C-2 · What happens to ARR and profit if repairs shut down? (Q9)
# Stream C, slide 8. Method: `docs/who_answers_what.md` (Person C).
#
# - **Cost saved** = repair cost in the last 12 months (drop-offs only, $45 outerwear / $18 activewear).
# - **ARR at risk** = repair users' ARR × the churn gap from C-1 (repair users stop being "protected" and churn like similar non-users).
# - **Profit at risk** = ARR at risk × repair users' profit margin *before* repair costs (repair costs are already counted in "cost saved", so they're added back to avoid counting them twice).
# - **Scenarios:** we can't prove how much of the gap repairs *cause*, so we assume 25% / 50% / 100%, and solve for the break-even share.

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
from src import tables as T
from src.metrics import load

OUT = C.RESULTS_DIR / "c_repairs"
lines = load()
visits = T.build_visits(lines)
customers = load("customers").set_index("customer_id")

# Churn gap from C-1 (run c1_churn first). Conservative: matched, non-users still buying after launch.
gap_tbl = pd.read_csv(OUT / "c1_churn_gap.csv", index_col=0)
GAP = -gap_tbl.loc["Matched, still buying after launch", "gap"]          # as a positive share
GAP_PLAIN = -gap_tbl.loc["Matched", "gap"]
print(f"Churn gap: {GAP:.1%} (plain matched: {GAP_PLAIN:.1%})")

# %% [markdown]
# ## Inputs: last 12 months (Nov 2025 to Oct 2026)

# %%
SINCE = C.AS_OF_DATE - pd.DateOffset(months=C.ARR_WINDOW_MONTHS)   # same window as ARR
last12 = lines[lines["date"] > SINCE]
repair_cost = last12["repair_cost_amt"].sum()
dropoffs = last12[last12["row_type"] == C.DROPOFF]["item_id"].map(C.REPAIR_ITEMS).value_counts()

users = customers[customers["used_repair"]]
users_arr = users["arr_12m"].sum()
company_arr = customers["arr_12m"].sum()

uv = visits[(visits["date"] > SINCE) & visits["customer_id"].isin(users.index)]
margin = (uv["profit"] + uv["repair_cost"]).sum() / uv["revenue"].sum()

inputs = pd.Series({
    "Repair cost, last 12 months ($)": repair_cost,
    "Drop-offs, outerwear": dropoffs.get("outerwear", 0),
    "Drop-offs, activewear": dropoffs.get("activewear", 0),
    "Repair users": len(users),
    "Repair users' ARR ($)": users_arr,
    "Company ARR ($)": company_arr,
    "Repair users' share of ARR": users_arr / company_arr,
    "Repair users' margin before repair cost": margin,
    "Churn gap (C-1)": GAP,
})
inputs

# %% [markdown]
# ## Scenarios and break-even

# %%
def scenario(share: float, gap: float = GAP) -> dict:
    arr_lost = users_arr * gap * share
    profit_lost = arr_lost * margin
    return {"ARR lost": arr_lost, "Profit lost": profit_lost,
            "Repair cost saved": repair_cost, "Net profit from scrapping": repair_cost - profit_lost}

SHARES = [0.25, 0.50, 1.00]
scen = pd.DataFrame({f"{s:.0%} caused by repairs": scenario(s) for s in SHARES}).T
scen.to_csv(OUT / "c2_scenarios.csv")

BREAK_EVEN = repair_cost / (users_arr * GAP * margin)
BREAK_EVEN_PLAIN = repair_cost / (users_arr * GAP_PLAIN * margin)
print(f"Scrapping repairs pays off only if less than {BREAK_EVEN:.0%} of the churn gap is caused by repairs "
      f"({BREAK_EVEN_PLAIN:.0%} using the plain matched gap).")
scen.style.format("${:,.0f}")

# %% [markdown]
# ## Chart (slide 8)

# %%
COST, LOST, INK, MUTED, SURFACE = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#fcfcfb"
plt.rcParams.update({"font.size": 11, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED, "figure.facecolor": SURFACE,
                     "axes.facecolor": SURFACE})

labels = ["Cost saved\nby scrapping"] + [f"Profit lost if\n{s:.0%} is causal" for s in SHARES]
vals = [repair_cost] + list(scen["Profit lost"])
fig, ax = plt.subplots(figsize=(8, 4.6))
bars = ax.bar(labels, vals, 0.55, color=[COST] + [LOST] * len(SHARES))
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + max(vals) * 0.015, f"${v / 1e3:,.0f}K",
            ha="center", color=INK, fontsize=10)
ax.axhline(repair_cost, color=COST, linewidth=1.2, linestyle="--")
ax.spines[["top", "right", "left"]].set_visible(False)
ax.yaxis.grid(True, color="#e4e3df", linewidth=0.8)
ax.set_axisbelow(True)
ax.yaxis.set_major_formatter(lambda v, _: f"${v / 1e6:.1f}M")
ax.set_ylabel("Per year")
ax.set_title(f"Scrapping repairs pays off only if under {BREAK_EVEN:.0%} of the churn gap is causal",
             loc="left", color=INK, fontsize=13)
fig.tight_layout()
fig.savefig(OUT / "c2_cost_vs_profit.png", dpi=200)
