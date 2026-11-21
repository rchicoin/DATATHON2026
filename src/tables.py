"""Build the 5 shared tables and write them to data/processed/*.parquet.

    python -m src.tables

Tables (grain):
  lines           one row per sales line (item sold / returned / repair), joined
  visits          one row per transaction_id
  customers       one row per customer
  customer_month  one row per customer per month (first visit month .. DATA_END)
  links           one row per Return / Repair Pickup line, linked to its original
"""
import numpy as np
import pandas as pd

from src import config as C
from src.clean import clean_customers, clean_items, clean_sales, join, read_raw


# --- lines ---------------------------------------------------------------------
def build_lines(sales, items, customers) -> pd.DataFrame:
    df = join(sales, items, customers)
    rt = df["row_type"]
    is_merch = rt.isin([C.PURCHASE, C.RETURN])

    df["revenue"] = df["quantity"] * df["unit_price_paid"]          # Returns are negative

    prod = df["quantity"] * df["production_cost"]
    if not C.RETURN_COST_REVERSES:
        prod = prod.where(rt != C.RETURN, 0.0)
    df["production_cost_amt"] = prod.where(is_merch, 0.0)

    # Repair cost is incurred at drop-off only; Pickup rows carry no cost.
    df["repair_cost_amt"] = (df["quantity"] * df["production_cost"]).where(rt == C.DROPOFF, 0.0)

    df["redeemed_dollars"] = df["points_redeemed"] / C.POINTS_PER_DOLLAR_REDEEMED
    df["profit"] = (df["revenue"] - df["production_cost_amt"]
                    - df["repair_cost_amt"] - df["redeemed_dollars"])
    df["is_repeat_visit"] = df["date"] > df["signup_date"]
    df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()
    return df


# --- visits --------------------------------------------------------------------
def build_visits(lines: pd.DataFrame) -> pd.DataFrame:
    g = lines.groupby("transaction_id", sort=False)
    v = g.agg(
        customer_id=("customer_id", "first"),
        datetime=("datetime", "first"),
        date=("date", "first"),
        month=("month", "first"),
        signup_date=("signup_date", "first"),
        tier=("tier_at_purchase", "first"),
        n_lines=("item_id", "size"),
        units=("quantity", "sum"),
        revenue=("revenue", "sum"),
        production_cost=("production_cost_amt", "sum"),
        repair_cost=("repair_cost_amt", "sum"),
        points_earned=("points_earned", "sum"),
        points_redeemed=("points_redeemed", "sum"),           # summed per transaction
        points_balance_after=("points_balance_after", "first"),  # never summed
        redeemed_dollars=("redeemed_dollars", "sum"),
        profit=("profit", "sum"),
    ).reset_index()
    for rt, col in [(C.PURCHASE, "has_purchase"), (C.RETURN, "has_return"),
                    (C.DROPOFF, "has_dropoff"), (C.PICKUP, "has_pickup")]:
        v[col] = v["transaction_id"].isin(lines.loc[lines["row_type"] == rt, "transaction_id"])
    v["is_repeat_visit"] = v["date"] > v["signup_date"]
    return v.sort_values("datetime").reset_index(drop=True)


# --- customers -----------------------------------------------------------------
def build_customers(customers: pd.DataFrame, visits: pd.DataFrame) -> pd.DataFrame:
    since_12m = C.AS_OF_DATE - pd.DateOffset(months=C.ARR_WINDOW_MONTHS)
    v = visits.assign(
        rev_12m=visits["revenue"].where(visits["date"] > since_12m, 0.0),
        arr_12m=visits["revenue"].where((visits["date"] > since_12m) & visits["is_repeat_visit"], 0.0),
        tier_rank=visits["tier"].map(C.TIER_RANK),
    )
    agg = v.groupby("customer_id").agg(
        first_visit=("date", "min"),
        last_visit=("date", "max"),
        n_visits=("transaction_id", "size"),
        n_repeat_visits=("is_repeat_visit", "sum"),
        revenue_total=("revenue", "sum"),
        profit_total=("profit", "sum"),
        revenue_12m=("rev_12m", "sum"),
        arr_12m=("arr_12m", "sum"),
        redeemed_dollars_total=("redeemed_dollars", "sum"),
        n_repair_dropoffs=("has_dropoff", "sum"),
        n_returns=("has_return", "sum"),
        max_tier_rank=("tier_rank", "max"),
    )
    first_repair = v[v["has_dropoff"]].groupby("customer_id")["date"].min().rename("first_repair_date")
    agg = agg.join(first_repair)
    agg["used_repair"] = agg["n_repair_dropoffs"] > 0
    agg["max_tier"] = agg["max_tier_rank"].map(dict(enumerate(C.TIER_ORDER)))
    agg = agg.drop(columns="max_tier_rank")
    agg["days_since_last_visit"] = (C.AS_OF_DATE - agg["last_visit"]).dt.days
    agg["churned"] = agg["days_since_last_visit"] > C.CHURN_DAYS

    out = customers.merge(agg, left_on="customer_id", right_index=True, how="left",
                          validate="one_to_one")
    out["has_sales"] = out["n_visits"].notna()
    return out


# --- customer_month ------------------------------------------------------------
def build_customer_month(visits: pd.DataFrame) -> pd.DataFrame:
    v = visits.assign(repeat_revenue=visits["revenue"].where(visits["is_repeat_visit"], 0.0))
    m = v.groupby(["customer_id", "month"]).agg(
        n_visits=("transaction_id", "size"),
        revenue=("revenue", "sum"),
        repeat_revenue=("repeat_revenue", "sum"),
        profit=("profit", "sum"),
        last_visit_in_month=("date", "max"),
    )
    # tier at the customer's last visit of the month
    last_tier = (v.sort_values("datetime").groupby(["customer_id", "month"])["tier"].last())
    m = m.join(last_tier.rename("tier_last_seen"))

    # dense panel: each customer from first-visit month to DATA_END month
    end = C.DATA_END.to_period("M").to_timestamp()
    first = v.groupby("customer_id")["month"].min()
    panel = pd.DataFrame({
        "customer_id": first.index,
        "month": [pd.date_range(f, end, freq="MS") for f in first.values],
    }).explode("month")
    panel["month"] = pd.to_datetime(panel["month"])
    cm = panel.merge(m.reset_index(), on=["customer_id", "month"], how="left")
    cm = cm.sort_values(["customer_id", "month"]).reset_index(drop=True)

    for col in ["n_visits", "revenue", "repeat_revenue", "profit"]:
        cm[col] = cm[col].fillna(0)
    cm["n_visits"] = cm["n_visits"].astype(int)
    cm["active"] = cm["n_visits"] > 0

    grp = cm.groupby("customer_id", sort=False)
    # tier only recorded at visits -> carry forward last seen (a lapsed member never shows a lower tier)
    cm["tier_last_seen"] = grp["tier_last_seen"].ffill()
    cm["arr_12m"] = (grp["repeat_revenue"]
                     .rolling(C.ARR_WINDOW_MONTHS, min_periods=1).sum()
                     .reset_index(level=0, drop=True))
    last_visit = grp["last_visit_in_month"].ffill()
    month_end = cm["month"] + pd.offsets.MonthEnd(0)
    cm["days_since_last_visit"] = (month_end - last_visit).dt.days
    cm["churned"] = cm["days_since_last_visit"] > C.CHURN_DAYS
    return cm.drop(columns="last_visit_in_month")


# --- links ---------------------------------------------------------------------
def build_links(lines: pd.DataFrame) -> pd.DataFrame:
    cols = ["transaction_id", "item_id", "customer_id", "date", "row_type",
            "original_transaction_id", "unit_price_paid", "notes"]
    pairs = [(C.RETURN, C.PURCHASE, "return"), (C.PICKUP, C.DROPOFF, "repair")]
    out = []
    for child, parent, kind in pairs:
        ch = lines.loc[lines["row_type"] == child, cols].copy()
        par = (lines.loc[lines["row_type"] == parent, ["transaction_id", "item_id", "date"]]
               .drop_duplicates(["transaction_id", "item_id"])
               .rename(columns={"transaction_id": "original_transaction_id",
                                "date": "original_date"}))
        # link on BOTH transaction_id and item_id
        ch = ch.merge(par, on=["original_transaction_id", "item_id"], how="left",
                      validate="many_to_one")
        ch["link_type"] = kind
        out.append(ch)
    links = pd.concat(out, ignore_index=True)
    links["resolved"] = links["original_date"].notna()
    links["unresolved_reason"] = np.where(
        links["resolved"], None,
        np.where(links["original_transaction_id"].isna(),
                 "no original_transaction_id (purchase predates data start)",
                 "original not found"))
    links["days_between"] = (links["date"] - links["original_date"]).dt.days
    return links


# --- build + checks ------------------------------------------------------------
def build_all(write: bool = True) -> dict:
    raw_sales, raw_items, raw_customers = read_raw()
    sales = clean_sales(raw_sales)
    items = clean_items(raw_items)
    customers = clean_customers(raw_customers)

    lines = build_lines(sales, items, customers)
    visits = build_visits(lines)
    cust = build_customers(customers, visits)
    cm = build_customer_month(visits)
    links = build_links(lines)
    tables = {"lines": lines, "visits": visits, "customers": cust,
              "customer_month": cm, "links": links}

    run_checks(raw_sales, sales, tables)

    if write:
        C.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        for name, df in tables.items():
            df.to_parquet(C.PROCESSED_DIR / f"{name}.parquet", index=False)
        print(f"\nWrote {len(tables)} tables to {C.PROCESSED_DIR.relative_to(C.ROOT)}/")
    return tables


def _ok(cond: bool, msg: str):
    print(f"  [{'PASS' if cond else 'FAIL'}] {msg}")
    return cond


def run_checks(raw_sales, sales, t) -> None:
    lines, visits, cust, cm, links = (t[k] for k in C.TABLES)
    rev_pre = (sales["quantity"] * sales["unit_price_paid"]).sum()
    results = []

    print("\n== Row counts ==")
    print(f"  raw sales rows        {len(raw_sales):>10,}")
    print(f"  duplicates dropped    {len(raw_sales) - len(sales):>10,}")
    print(f"  clean sales rows      {len(sales):>10,}")
    print(f"  lines (after joins)   {len(lines):>10,}")
    print(f"  visits                {len(visits):>10,}")
    print(f"  customers             {len(cust):>10,}  ({int(cust['has_sales'].sum()):,} with sales)")
    print(f"  customer_month        {len(cm):>10,}")
    print(f"  links                 {len(links):>10,}")

    print("\n== Join integrity ==")
    results.append(_ok(len(lines) == len(sales), "row count unchanged by joins"))
    results.append(_ok(np.isclose(lines["revenue"].sum(), rev_pre),
                       f"revenue unchanged by joins: before ${rev_pre:,.2f} / after ${lines['revenue'].sum():,.2f}"))
    results.append(_ok(lines["item_name"].notna().all() and lines["signup_date"].notna().all(),
                       "every line matched an item and a customer"))
    results.append(_ok(np.isclose(visits["revenue"].sum(), rev_pre)
                       and np.isclose(cm["revenue"].sum(), rev_pre),
                       "revenue ties out across lines / visits / customer_month"))

    print("\n== Costs ==")
    pk = lines["row_type"] == C.PICKUP
    pickup_cost = lines.loc[pk, ["production_cost_amt", "repair_cost_amt"]].abs().sum().sum()
    results.append(_ok(pickup_cost == 0, f"no cost on Pickup rows ({pk.sum():,} rows, cost ${pickup_cost:,.2f})"))
    rep = lines["row_type"].isin([C.DROPOFF, C.PICKUP])
    results.append(_ok((lines.loc[rep, "production_cost_amt"] == 0).all(),
                       "repairs carry repair cost only, no production cost"))
    print(f"  repair cost total (drop-offs)  ${lines['repair_cost_amt'].sum():,.2f}")
    print(f"  RETURN_COST_REVERSES = {C.RETURN_COST_REVERSES}")

    print("\n== Links ==")
    for kind in ["return", "repair"]:
        l = links[links["link_type"] == kind]
        has_id = l["original_transaction_id"].notna()
        label = "Return -> Purchase" if kind == "return" else "Pickup -> Drop-off"
        results.append(_ok(l.loc[has_id, "resolved"].all(),
                           f"{label}: {int(l.loc[has_id, 'resolved'].sum()):,}/{int(has_id.sum()):,} linked rows resolve"))
        if (~has_id).any():
            d = l.loc[~has_id, "date"]
            print(f"  [INFO] {label}: {int((~has_id).sum())} rows have no original_transaction_id "
                  f"(dates {d.min():%Y-%m-%d}..{d.max():%Y-%m-%d}; purchase predates data start)")
        results.append(_ok((l["days_between"].dropna() >= 0).all(), f"{label}: days_between >= 0"))
    n_drop = (lines["row_type"] == C.DROPOFF).sum()
    n_picked = links[(links["link_type"] == "repair") & links["resolved"]].drop_duplicates(
        ["original_transaction_id", "item_id"]).shape[0]
    print(f"  [INFO] drop-offs never picked up: {n_drop - n_picked:,} of {n_drop:,} (cost still counted)")

    print(f"\n{sum(results)}/{len(results)} checks passed")
    assert all(results), "a check failed — see above"


if __name__ == "__main__":
    build_all()
