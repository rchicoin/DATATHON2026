"""Shared loaders and metric helpers. Import these in every notebook:

    from src.metrics import load
    visits = load("visits")

Helpers implement the agreed definitions in docs/definitions.md — use them
instead of re-deriving a metric so every stream gets the same number.
"""
import pandas as pd

from src import config as C


def load(name: str) -> pd.DataFrame:
    """Load a shared table from data/processed/. Builds all tables if missing."""
    if name not in C.TABLES:
        raise ValueError(f"unknown table {name!r}; choose from {C.TABLES}")
    path = C.PROCESSED_DIR / f"{name}.parquet"
    if not path.exists():
        from src.tables import build_all
        build_all()
    return pd.read_parquet(path)


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
