"""Slide 8 (financial impact): where the profit is, per year.

Numbers come from the reconciled findings (decisions #20-22), not recomputed here:
- Closing repairs: net +$57K (boosted trees) to -$67K (logistic) a year  -> D F5, d3_churn_model.ipynb section 5
- Loyalty points redeemed, last 12 months: $413K (5.9% of revenue)        -> B F1, analysis/b_loyalty/b_loyalty.py
- Win back half the lost 18-24 shoppers: +$212K profit a year             -> A F12, A-4 notebook
Run from the repo root:  python analysis/d_customers_arr/d5_money_chart.py
"""
from pathlib import Path

import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[2] / "results" / "d_customers_arr"
BLUE, ORANGE, GREY = "#2a78d6", "#eb6834", "#8a8a85"
INK, INK2, GRID = "#0b0b0b", "#5f5e5a", "#e4e3df"
plt.rcParams.update({
    "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb", "font.size": 12,
    "axes.edgecolor": GRID, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "axes.axisbelow": True,
    "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False, "text.parse_math": False,
})

rows = [  # label, left, width, colour, value label
    ("Win back half the lost\n18–24 shoppers", 0, 212, BLUE, "+$212K profit"),
    ("Close free repairs\n(net, two models)", -67, 124, GREY, "−$67K to +$57K"),
    ("Loyalty points redeemed\n(last 12 months)", -413, 413, ORANGE, "−$413K (5.9% of revenue)"),
]
fig, ax = plt.subplots(figsize=(11, 4.6))
for i, (lab, left, width, colr, txt) in enumerate(rows):
    ax.barh(i, width, left=left, color=colr, height=0.55)
    end = left + width
    if left < 0 and end <= 0:      # all-negative bar: label to the left
        ax.annotate(txt, (left, i), xytext=(-8, 0), textcoords="offset points", ha="right", va="center",
                    color=INK, fontsize=11)
    else:
        ax.annotate(txt, (end, i), xytext=(8, 0), textcoords="offset points", ha="left", va="center",
                    color=INK, fontsize=11)
ax.axvline(0, color=INK2, lw=1)
ax.set_yticks(range(len(rows)), [r[0] for r in rows])
ax.set_xlim(-800, 450)
ax.set_xticks([-400, -200, 0, 200, 400])
ax.set_xticklabels(["−$400K", "−$200K", "$0", "+$200K", "+$400K"])
ax.set_xlabel("Effect on Lululime's profit per year")
ax.grid(axis="y", visible=False)
fig.suptitle("Repairs barely move profit; points cost $413K a year; young shoppers are worth $212K",
             x=0.01, ha="left", color=INK, fontsize=13)
fig.tight_layout()
fig.savefig(OUT / "d5_money.png", dpi=200)
print("saved")
