"""Appendix chart in the deck's "field journal" style (matches slides/deck_charts.py).

K-means segments (F12, analysis/d_customers_arr/d8_matching_segments.ipynb, Part B):
share of customers vs share of ARR, and how many in each group use free repairs.
Numbers are copied from that notebook's output, not recomputed here.
Run from the repo root:  python analysis/d_customers_arr/d8_deckstyle_segments.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parents[2] / "results" / "d_customers_arr"

# Palette and type: identical to slides/deck_charts.py
PAPER, INK, INK2, NEUTRAL, RULE = "#F4F1E8", "#1B2A22", "#4F564E", "#8F8A7A", "#D9D4C5"
GREEN = "#3D7A1E"
plt.rcParams.update({
    "figure.facecolor": PAPER, "axes.facecolor": PAPER, "savefig.facecolor": PAPER,
    "font.family": ["Segoe UI", "DejaVu Sans"], "font.size": 16,
    "text.color": INK, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK,
    "axes.edgecolor": RULE, "axes.grid": True, "axes.grid.axis": "x", "grid.color": RULE,
    "grid.linewidth": 0.8, "axes.axisbelow": True,
    "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False,
    "xtick.major.size": 0, "ytick.major.size": 0, "text.parse_math": False,
})

segments = [  # name, short description, % of customers, % of ARR, % using free repairs
    ("Gold regulars", "about 18 trips a year", 31.8, 79.7, 89),
    ("Occasional big-basket\nshoppers", "about 3–4 trips, biggest baskets", 31.49, 14.5, 10),
    ("Fading light shoppers", "youngest group, last visit ~5 months ago", 26.4, 3.2, 6),
    ("Frequent returners", "a third of their trips are returns", 10.3, 2.6, 14),
]

fig, ax = plt.subplots(figsize=(13, 7.4))
y = np.arange(len(segments))
h = 0.36
cust = [s[2] for s in segments]
arr = [s[3] for s in segments]
ax.barh(y - h / 2, cust, h, color=NEUTRAL)
ax.barh(y + h / 2, arr, h, color=[GREEN] + [INK] * 3)

for i, s in enumerate(segments):
    ax.text(cust[i] + 1, i - h / 2, f"{cust[i]:.0f}% of customers", va="center", fontsize=14, color=INK2)
    ax.text(arr[i] + 1, i + h / 2, f"{arr[i]:.0f}% of sales", va="center", fontsize=15, fontweight="bold",
            color=GREEN if i == 0 else INK)
    # repair-use column on the right
    ax.text(106, i, f"{s[4]}%", va="center", ha="center", fontsize=22 if i == 0 else 18, fontweight="bold",
            color=GREEN if i == 0 else INK2)

ax.text(106, -0.55, "use free\nrepairs", ha="center", va="bottom", fontsize=13, color=INK2)
ax.set_yticks(y, [f"{s[0]}\n{s[1]}" for s in segments], fontsize=14)
for lab, s in zip(ax.get_yticklabels(), segments):
    lab.set_color(INK)
ax.set_ylim(3.55, -0.95)
ax.set_xlim(0, 113)
ax.set_xticks([0, 20, 40, 60, 80])
ax.set_xticklabels(["0%", "20%", "40%", "60%", "80%"])
ax.set_xlabel("Share of customers (grey) and of yearly sales from returning customers (dark)")
ax.axvline(99.5, color=RULE, lw=1)

fig.text(0.012, 0.975, "Who brings in our returning-customer sales?", ha="left", va="top", fontsize=19,
         fontweight="bold", color=INK)
fig.text(0.012, 0.915, "We grouped every customer who bought in the last year by how they shop (k-means clustering).\n"
         "A third of customers bring in 80% of the sales, and 9 in 10 of them use free repairs.",
         ha="left", va="top", fontsize=14, color=INK2)
fig.tight_layout(rect=(0, 0, 1, 0.86))
fig.savefig(OUT / "d8_segments_deckstyle.png", dpi=200)
print("saved")
