"""Deck-style versions of Stream B's charts (slides 5-6).

Plotting only: every number below is copied from the printed outputs of
results/b_loyalty/loyalty_analysis.ipynb (Aisyah, Stream B). Nothing is recomputed.
Run from the repo root:  python analysis/d_customers_arr/deck_b_charts.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

OUT = Path(__file__).resolve().parents[2] / "results" / "d_customers_arr"
BLUE, ORANGE = "#2a78d6", "#eb6834"
INK, INK2, GRID = "#0b0b0b", "#5f5e5a", "#e4e3df"
plt.rcParams.update({
    "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb", "font.size": 12,
    "axes.edgecolor": GRID, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "axes.axisbelow": True,
    "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False,
})


def label_bars(ax, bars, fmt):
    for b in bars:
        ax.annotate(fmt(b.get_height()), (b.get_x() + b.get_width() / 2, b.get_height()), xytext=(0, 4),
                    textcoords="offset points", ha="center", color=INK, fontsize=11)


# --- B-1: profit per customer, 12 months before vs after loyalty launch (cell 0 output) ---
groups = ["Non-members", "Members"]
before = [341.00, 870.30]
after = [156.59, 714.70]
x = np.arange(2)
fig, ax = plt.subplots(figsize=(10, 4.6))
b1 = ax.bar(x - 0.19, before, 0.36, color=BLUE, label="12 months before launch (Jun 2023 – May 2024)")
b2 = ax.bar(x + 0.19, after, 0.36, color=ORANGE, label="12 months after launch (Jun 2024 – May 2025)")
label_bars(ax, list(b1) + list(b2), lambda v: f"${v:,.0f}")
for i in range(2):
    ch = (after[i] / before[i] - 1) * 100
    ax.annotate(f"{ch:+.0f}%", (x[i] + 0.19, after[i]), xytext=(0, 22), textcoords="offset points",
                ha="center", color=INK2, fontsize=11)
ax.set_xticks(x, groups)
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f"${v:,.0f}"))
ax.set_ylabel("Average profit per customer")
ax.set_ylim(0, 1050)
ax.grid(axis="x", visible=False)
ax.legend(loc="upper left", frameon=False)
fig.suptitle("Members were 2.6× as profitable before loyalty launched; both groups fell in the competitor year",
             x=0.01, ha="left", color=INK, fontsize=13)
fig.tight_layout()
fig.savefig(OUT / "deck_b1_profit_members.png", dpi=200)
plt.close(fig)

# --- B-2: return rate by share paid with points (cell 1 output) + B-3: basket by points to next tier (cell 2) ---
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.6))
buckets = ["0%\n(133K)", "1–25%\n(26K)", "26–50%\n(5.9K)", "Over 50%\n(3.6K)"]
rates = [9.5, 10.5, 9.8, 23.7]
n = [133425, 25580, 5861, 3617]
bars = a1.bar(buckets, rates, color=[BLUE, BLUE, BLUE, ORANGE], width=0.6)
label_bars(a1, bars, lambda v: f"{v:.1f}%")
a1.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
a1.set_ylim(0, 30)
a1.set_xlabel("Share of purchase paid with points (purchases)")
a1.set_ylabel("Purchases later returned")
a1.set_title("Returns more than double past 50% points", loc="left", color=INK, fontsize=12)
a1.grid(axis="x", visible=False)

gaps = ["0–50", "50–100", "100–200", "200–400", "400+"]
basket = [159.70, 164.27, 162.38, 160.01, 155.65]
bars = a2.bar(gaps, basket, color=BLUE, width=0.6)
label_bars(a2, bars, lambda v: f"${v:,.0f}")
a2.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f"${v:,.0f}"))
a2.set_ylim(0, 200)
a2.set_xlabel("Points still needed for the next tier")
a2.set_ylabel("Average basket")
a2.set_title("Being close to a tier doesn’t raise spending", loc="left", color=INK, fontsize=12)
a2.grid(axis="x", visible=False)
fig.tight_layout()
fig.savefig(OUT / "deck_b2_b3_points_tiers.png", dpi=200)
plt.close(fig)
print("saved")
