"""Cross-stream review checks (2026-11-21). Reproduces every number in docs/review/analysis_review.md
that isn't already in a stream's findings.

    python docs/review/review_checks.py

Read-only: loads the shared table via src.metrics.load(), writes nothing.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd

from src import config as C
from src import tables as T
from src.metrics import load

pd.set_option("display.width", 200)
df = load()
v = T.build_visits(df)
cust = load("customers").set_index("customer_id")
yr = pd.DateOffset(years=1)
last12 = v[v.date > C.AS_OF_DATE - pd.DateOffset(months=12)]


def h(title):
    print(f"\n=== {title} ===")


# ---------------------------------------------------------------------------------- 0. sanity
h("0. Headline ARR")
arr = v[v.is_repeat_visit].groupby("month").revenue.sum().rolling(12, min_periods=1).sum()
print(f"ARR Feb 2024 ${arr['2024-02-01']:,.0f} | low {arr['2024-03-01':].idxmin():%b %Y} ${arr['2024-03-01':].min():,.0f}"
      f" | Oct 2026 ${arr['2026-10-01']:,.0f} ({arr['2026-10-01'] / arr['2024-02-01'] - 1:+.1%})")
print(f"Revenue last 12 months ${last12.revenue.sum():,.0f}; margin incl. points & repairs "
      f"{last12.profit.sum() / last12.revenue.sum():.1%}")

# ---------------------------------------------------------------------------------- 1. win-back value (A F12)
h("1. Young-shopper value (A F12)")
age = cust.age_band
vv = v.assign(age=v.customer_id.map(age))


def year_value(s, e):
    w = vv[(vv.date >= s) & (vv.date < e) & (vv.age == "18-24")]
    buyers = w.loc[w.has_purchase, "customer_id"].nunique()
    return dict(revenue=w.revenue.sum(), profit=w.profit.sum(), buyers=buyers,
                margin=w.profit.sum() / w.revenue.sum(), points=w.redeemed_dollars.sum())


a = year_value("2023-03-01", "2024-03-01")
b = year_value("2025-11-01", "2026-11-01")
for k, d in [("Mar 2023-Feb 2024", a), ("Nov 2025-Oct 2026", b)]:
    print(f"{k}: revenue ${d['revenue']:,.0f}, profit ${d['profit']:,.0f}, margin {d['margin']:.1%}, "
          f"buyers {d['buyers']:,}, points ${d['points']:,.0f}")
lost_buyers = a["buyers"] - b["buyers"]
ppb = b["profit"] / b["buyers"]
lost_rev = a["revenue"] - b["revenue"]
print(f"Published: lost profit ${a['profit'] - b['profit']:,.0f}; 50% win-back $"
      f"{(a['profit'] - b['profit']) / 2:,.0f}")
print(f"Lost buyers {lost_buyers:,}; profit per buyer today ${ppb:,.0f}")
print(f"  50% win-back at today's profit per buyer: ${0.5 * lost_buyers * ppb:,.0f}")
print(f"  Lost revenue at today's margin: ${lost_rev * b['margin']:,.0f} (50%: ${0.5 * lost_rev * b['margin']:,.0f})")
arr_age = (T.build_customer_month(v).assign(age=lambda d: d.customer_id.map(age))
           .groupby(["month", "age"]).arr_12m.sum().unstack())
lost_arr = arr_age.loc["2024-02-01", "18-24"] - arr_age.loc["2026-10-01", "18-24"]
print(f"  18-24 ARR lost ${lost_arr:,.0f}; 50% x today's margin: ${0.5 * lost_arr * b['margin']:,.0f}")
print(f"  Implied margin of published pair ($212K profit / $275K ARR): {212 / 275:.0%}")

# ---------------------------------------------------------------------------------- 2. points cost (B F1)
h("2. Points cost: earn rate, redemption, tier mix, liability (B F1)")
post = df[df.date >= C.LOYALTY_LAUNCH].assign(q=lambda d: d.date.dt.to_period("Q"))
memb = post[post.tier_at_purchase.isin(["Member", "Silver", "Gold"]) & (post.row_type == C.PURCHASE)]
g = pd.DataFrame({
    "earned_%_member_rev": memb.groupby("q").points_earned.sum() / 20 / memb.groupby("q").revenue.sum() * 100,
    "redeemed_%_all_rev": post.groupby("q").redeemed_dollars.sum() / post.groupby("q").revenue.sum() * 100,
    "gold_%_member_rev": memb[memb.tier_at_purchase == "Gold"].groupby("q").revenue.sum()
                         / memb.groupby("q").revenue.sum() * 100,
}).round(1)
print(g.T.to_string())
print("(2024Q2 = June only; 2026Q4 = October only)")
bal = v.sort_values("datetime").groupby("customer_id").points_balance_after.last()
print(f"Points earned since launch ${df.points_earned.sum() / 20:,.0f} (net of return claw-backs); "
      f"redeemed ${df.points_redeemed.sum() / 20:,.0f}; outstanding balance ${bal.sum() / 20:,.0f}")
m12 = last12.merge(df[["transaction_id", "tier_at_purchase"]].drop_duplicates("transaction_id"), on="transaction_id")
mem_rev12 = m12[m12.tier_at_purchase.isin(["Member", "Silver", "Gold"])].revenue.sum()
print(f"Member revenue last 12 months ${mem_rev12:,.0f} ({mem_rev12 / last12.revenue.sum():.0%} of revenue); "
      f"+0.25 pts per $ costs ~${mem_rev12 * 0.25 / 20:,.0f}/yr")
print(f"Points cut to 5% of revenue (slide 8 bar): ${last12.redeemed_dollars.sum() - 0.05 * last12.revenue.sum():,.0f}")

# ---------------------------------------------------------------------------------- 3. B-1 robustness
h("3. Loyalty matched DiD (B-1) and a timing-robust variant")
cinfo = df[["customer_id", "age_band", "loyalty_join_date"]].drop_duplicates("customer_id").set_index("customer_id")
L = C.LOYALTY_LAUNCH


def did(pre_s, pre_e, post_s, post_e, is_member, exclude=None):
    pre = v[(v.date >= pre_s) & (v.date < pre_e)]
    pst = v[(v.date >= post_s) & (v.date < post_e)]
    t = (pre.groupby("customer_id")[["revenue", "profit"]].sum().add_suffix("_pre")
         .join(pst.groupby("customer_id")[["revenue", "profit"]].sum().add_suffix("_post"), how="inner")
         .join(cinfo))
    t["member"] = is_member(t)
    if exclude is not None:
        t = t[~exclude(t)]
    t["q"] = pd.qcut(t.revenue_pre, 4, labels=False)
    t["dr"], t["dp"] = t.revenue_post - t.revenue_pre, t.profit_post - t.profit_pre
    cell = t.groupby(["age_band", "q", "member"])[["dr", "dp"]].mean().unstack("member")
    d = pd.DataFrame({k: cell[k][True] - cell[k][False] for k in ["dr", "dp"]}).dropna()
    w = t[t.member].groupby(["age_band", "q"]).size().reindex(d.index)
    out = d.mul(w, axis=0).sum() / w.sum()
    return len(t), int(t.member.sum()), out.dr, out.dp


n, nm, dr, dp = did(L - yr, L, L, L + yr, lambda t: t.loyalty_join_date.notna() & (t.loyalty_join_date < L + yr))
print(f"Published design: {n:,} customers, {nm:,} members: +${dr:,.0f} revenue, +${dp:,.0f} profit "
      f"({dp / dr:.0%}); x members = ${dp * nm:,.0f}")
j1 = cinfo.loyalty_join_date[(cinfo.loyalty_join_date >= L) & (cinfo.loyalty_join_date < L + yr)]
print("Year-1 joiners by quarter:", j1.dt.to_period("Q").value_counts().sort_index().to_dict())
E = pd.Timestamp("2024-09-01")
n, nm, dr, dp = did(E - yr, L, E, L + yr, lambda t: t.loyalty_join_date.notna() & (t.loyalty_join_date < E),
                    lambda t: t.loyalty_join_date.notna() & (t.loyalty_join_date >= E) & (t.loyalty_join_date < L + yr))
print(f"Early joiners (Jun-Aug 2024) vs not joined by May 2025, Sep-May windows: {n:,} customers, {nm:,} members: "
      f"+${dr:,.0f} revenue, +${dp:,.0f} profit")

# ---------------------------------------------------------------------------------- 4. B-2 robustness + refunds
h("4. Returns vs points share (B-2): visit, unit and single-item level")
r = df[df.row_type == C.RETURN]
buy = df[df.row_type == C.PURCHASE].groupby("transaction_id").agg(
    rev=("revenue", "sum"), units=("quantity", "sum"), lines=("item_id", "size"))
buy = buy.join(v.set_index("transaction_id").redeemed_dollars)
buy = buy[buy.rev > 0]
buy["share"] = (buy.redeemed_dollars / buy.rev).clip(upper=1)
buy["bucket"] = pd.cut(buy.share, [-0.001, 0, 0.25, 0.5, 1], labels=["0%", "1-25%", "26-50%", ">50%"])
buy["ret_units"] = (-r.groupby("original_transaction_id").quantity.sum()).reindex(buy.index).fillna(0)
buy["any_ret"] = buy.ret_units > 0
tbl = buy.groupby("bucket", observed=True).agg(
    visits=("rev", "size"), visit_return_rate=("any_ret", "mean"), returned_units=("ret_units", "sum"),
    units=("units", "sum"), avg_lines=("lines", "mean"), avg_basket=("rev", "mean"))
tbl["unit_return_rate"] = tbl.returned_units / tbl.units
single = buy[buy.lines == 1].groupby("bucket", observed=True).any_ret.mean().rename("single_item_return_rate")
print(tbl.join(single)[["visits", "visit_return_rate", "unit_return_rate", "single_item_return_rate",
                        "avg_lines", "avg_basket"]].round(3).to_string())

vs = v.sort_values("datetime").copy()
vs["delta"] = vs.points_balance_after - vs.groupby("customer_id").points_balance_after.shift()
ro = vs[vs.has_return & ~vs.has_purchase & vs.tier.isin(["Member", "Silver", "Gold"])].dropna(subset=["delta"])
print(f"Return rows: points_redeemed total {r.points_redeemed.sum():.0f} (never restored); "
      f"points_earned total {r.points_earned.sum():,.0f} (clawed back)")
print(f"Return-only member visits where balance change = earned - redeemed: "
      f"{(abs(ro.delta - (ro.points_earned - ro.points_redeemed)) < 1).mean():.1%} of {len(ro):,}")
r = r.assign(orig_share=r.original_transaction_id.map(buy.share))
print(f"Points-funded value inside refunds since launch: ${(-r.revenue * r.orig_share.fillna(0)).sum():,.0f} "
      f"(from >50%-points purchases: ${(-r.revenue * r.orig_share).where(r.orig_share > 0.5).sum():,.0f})")

# ---------------------------------------------------------------------------------- 5. C-1 timing bias
h("5. Repair churn gap (C-1): built-in bias and a landmark re-estimate")
PRE_S, PRE_E = C.REPAIRS_LAUNCH - yr, C.REPAIRS_LAUNCH - pd.Timedelta(days=1)
coh = cust.loc[v[v.date.between(PRE_S, PRE_E)].customer_id.unique()]
users = coh[coh.used_repair]
cutoff = C.AS_OF_DATE - pd.Timedelta(days=C.CHURN_DAYS)
late = users.first_repair_date > cutoff
print(f"Cohort repair users {len(users):,}; first repair after {cutoff:%d %b %Y} (cannot count as churned): "
      f"{late.sum():,} ({late.mean():.0%}). Churn: all users {users.churned.mean():.1%}, "
      f"excluding late starters {users.loc[~late, 'churned'].mean():.1%}")

L1 = pd.Timestamp("2025-09-30")
win = v[(v.date >= C.REPAIRS_LAUNCH) & (v.date <= L1) & v.has_purchase]
c2 = coh.loc[coh.index.intersection(win.customer_id.unique())].copy()
c2["early_user"] = c2.first_repair_date <= L1
c2["pre_spend"] = v[v.date.between(PRE_S, PRE_E)].groupby("customer_id").revenue.sum()
c2["spend_q"] = pd.qcut(c2.pre_spend.rank(method="first"), 4, labels=False)
c2["visit_q"] = pd.qcut(win.groupby("customer_id").size().reindex(c2.index).rank(method="first"), 4, labels=False)
last_purchase = v[v.has_purchase].groupby("customer_id").date.max()
c2["churn_p"] = (C.AS_OF_DATE - c2.index.map(last_purchase)).days > C.CHURN_DAYS


def matched(d, keys):
    gg = d.groupby(keys + ["early_user"]).churn_p.agg(["mean", "size"]).unstack("early_user").dropna()
    w = gg[("size", True)]
    return (gg[("mean", True)] * w).sum() / w.sum(), (gg[("mean", False)] * w).sum() / w.sum(), int(w.sum())


raw = c2.groupby("early_user").churn_p.mean()
print(f"Landmark sample {len(c2):,} ({c2.early_user.sum():,} repaired by {L1:%b %Y}); purchase-visit churn")
print(f"  raw:                          users {raw[True]:.1%} vs non-users {raw[False]:.1%} -> {raw[True] - raw[False]:+.1%}")
for keys, lab in [(["age_band", "spend_q"], "age x spend"), (["age_band", "spend_q", "visit_q"], "age x spend x visits")]:
    u_, n_, k = matched(c2, keys)
    print(f"  matched {lab:<22}users {u_:.1%} vs non-users {n_:.1%} -> {u_ - n_:+.1%} (users matched {k:,})")

# ---------------------------------------------------------------------------------- 6. what a bigger effect would mean
h("6. Profit at risk at different repair effects (C-2 method: users' ARR x effect x margin)")
uarr = cust.loc[cust.used_repair, "arr_12m"].sum()
uv = last12[last12.customer_id.isin(cust.index[cust.used_repair])]
margin = (uv.profit + uv.repair_cost).sum() / uv.revenue.sum()
cost = last12.repair_cost.sum()
print(f"Repair users' ARR ${uarr:,.0f}; margin before repair cost {margin:.1%}; repair cost ${cost:,.0f}; "
      f"break-even effect {cost / (uarr * margin):.1%} pts")
for eff in [0.046, 0.053, 0.086, 0.16]:
    p = uarr * eff * margin
    print(f"  effect {eff:.1%}: profit at risk ${p:,.0f} -> net of closing ${cost - p:+,.0f}")

# ---------------------------------------------------------------------------------- 7. timing of the recovery
h("7. When did repeat revenue recover? (same months vs Mar 2023-Feb 2024)")
rep = v[v.is_repeat_visit].assign(m=lambda d: d.date.dt.month)
base = rep[(rep.date >= "2023-03-01") & (rep.date < "2024-03-01")].groupby("m").revenue.sum()
for s, e, lab in [("2024-03-01", "2025-03-01", "Mar 2024-Feb 2025"), ("2025-03-01", "2026-03-01", "Mar 2025-Feb 2026"),
                  ("2026-03-01", "2026-11-01", "Mar-Oct 2026")]:
    w = rep[(rep.date >= s) & (rep.date < e)]
    months = w.m.unique()
    print(f"  {lab}: {w.revenue.sum() / base.loc[months].sum() - 1:+.1%}")
