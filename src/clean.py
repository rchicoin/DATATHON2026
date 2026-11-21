"""Load and clean the three raw CSVs, then join them into one line-level frame.

All cleaning rules live here (see docs/data_notes.md). Notebooks must never
re-clean — import from src.metrics.load() instead.
"""
import pandas as pd

from src import config as C

ID_COLS = {"transaction_id": str, "customer_id": str, "item_id": str,
           "original_transaction_id": str}


def read_raw():
    """Read the raw CSVs with IDs as strings. No cleaning."""
    sales = pd.read_csv(C.SALES_CSV, dtype={**ID_COLS, "tier_at_purchase": str, "notes": str})
    items = pd.read_csv(C.ITEMS_CSV, dtype={"item_id": str})
    customers = pd.read_csv(C.CUSTOMERS_CSV, dtype={"customer_id": str})
    return sales, items, customers


def _norm_text(s: pd.Series) -> pd.Series:
    """lowercase, trim, collapse internal whitespace; empty -> NA."""
    out = s.str.strip().str.lower().str.replace(r"\s+", " ", regex=True)
    return out.mask(out == "")


def clean_sales(sales: pd.DataFrame) -> pd.DataFrame:
    s = sales.drop_duplicates(keep="first").copy()   # 1,016 double entries

    s["date"] = pd.to_datetime(s["date"])
    s["datetime"] = pd.to_datetime(s["date"].dt.strftime("%Y-%m-%d") + " " + s["time"])

    # Tier: blank before loyalty launch is "Pre-loyalty", not "Non-member".
    pre = s["date"] < C.LOYALTY_LAUNCH
    s.loc[pre & s["tier_at_purchase"].isna(), "tier_at_purchase"] = C.PRE_LOYALTY
    assert s["tier_at_purchase"].notna().all(), "blank tier after loyalty launch"

    # Points: blank pre-launch and for Non-members -> 0.
    for col in ["points_earned", "points_redeemed", "points_balance_after"]:
        s[col] = s[col].fillna(0)

    s["notes"] = _norm_text(s["notes"])
    return s


def clean_items(items: pd.DataFrame) -> pd.DataFrame:
    return items.copy()


def clean_customers(customers: pd.DataFrame) -> pd.DataFrame:
    c = customers.copy()
    c["signup_date"] = pd.to_datetime(c["signup_date"])
    c["loyalty_join_date"] = pd.to_datetime(c["loyalty_join_date"])
    c["age_band"] = c["age_band"].fillna("Unknown")
    c["home_area"] = c["home_area"].fillna("Unknown")
    split = c["interests"].fillna("").str.split(";")
    for name in C.INTERESTS:
        c[f"interest_{name.lower()}"] = split.apply(lambda xs, n=name: int(n in xs))
    c["is_member"] = c["loyalty_join_date"].notna()
    return c


def join(sales: pd.DataFrame, items: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    """sales LEFT JOIN items LEFT JOIN customers, many_to_one on both."""
    df = sales.merge(items, on="item_id", how="left", validate="many_to_one")
    df = df.merge(customers, on="customer_id", how="left", validate="many_to_one")
    return df


def load_clean():
    """Return (sales, items, customers) cleaned but not joined."""
    sales, items, customers = read_raw()
    return clean_sales(sales), clean_items(items), clean_customers(customers)
