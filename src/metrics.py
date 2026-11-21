"""Shared loaders and metric helpers. Import these in every notebook:

    from src.metrics import load
    df = load()      # the joined table: one row per sales line

Helpers implement the agreed definitions in docs/definitions.md — use them
instead of re-deriving a metric so every stream gets the same number.
"""
import pandas as pd

from src import config as C

DATE_COLS = ["date", "datetime", "signup_date", "loyalty_join_date", "month"]
ID_COLS = {"transaction_id": str, "customer_id": str, "item_id": str,
           "original_transaction_id": str, "tier_at_purchase": str}


def load(name: str = "lines") -> pd.DataFrame:
    """Load the cleaned, joined table (data/processed/lululime_clean.csv.gz). Builds it if missing.

    load() / load("lines") -> the joined table, one row per sales line.
    load("visits" | "customers" | "customer_month" | "links") -> built from that
    same CSV with the shared definitions in src/tables.py (nothing extra on disk).
    """
    if not C.CLEAN_CSV.exists():
        from src.tables import build_all
        build_all()
    lines = pd.read_csv(C.CLEAN_CSV, dtype=ID_COLS, parse_dates=DATE_COLS)
    if name == "lines":
        return lines

    from src import tables as T
    if name == "links":
        return T.build_links(lines)
    visits = T.build_visits(lines)
    if name == "visits":
        return visits
    if name == "customer_month":
        return T.build_customer_month(visits)
    if name == "customers":
        from src.clean import clean_customers, read_raw
        return T.build_customers(clean_customers(read_raw()[2]), visits)
    raise ValueError(f"unknown table {name!r}; choose lines, visits, customers, customer_month, links")


def profit(revenue, production_cost, repair_cost, points_redeemed):
    """Profit = Revenue − Production Costs − Repair Costs − Redeemed Points ($)."""
    return revenue - production_cost - repair_cost - points_redeemed / C.POINTS_PER_DOLLAR_REDEEMED


def company_arr(customer_month: pd.DataFrame) -> pd.Series:
    """ARR by month: sum of each customer's trailing-12-month repeat revenue."""
    return customer_month.groupby("month")["arr_12m"].sum().rename("arr")


def churn_rate(customers: pd.DataFrame) -> float:
    """Share of customers with sales in the data who had no visit in CHURN_DAYS as of AS_OF_DATE."""
    c = customers[customers["has_sales"]]
    return float(c["churned"].mean())


def period(dates: pd.Series) -> pd.Series:
    """Label each date with the most recent event that preceded it (for before/after cuts)."""
    labels = ["baseline"] + list(C.EVENTS)
    edges = [pd.Timestamp.min] + list(C.EVENTS.values())
    order = sorted(zip(edges, labels))
    edges, labels = [e for e, _ in order], [l for _, l in order]
    return pd.cut(pd.to_datetime(dates), bins=edges + [pd.Timestamp.max],
                  labels=labels, right=False)


def in_window(dates: pd.Series, start, end) -> pd.Series:
    """True where start <= date <= end (inclusive)."""
    d = pd.to_datetime(dates)
    return (d >= pd.Timestamp(start)) & (d <= pd.Timestamp(end))
