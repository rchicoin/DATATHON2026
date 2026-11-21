"""Single source of truth for paths, dates and agreed definitions.

Change a value here (via a reviewed PR) — never hard-code it in a notebook.
Every change must also be recorded in docs/decisions_log.md.
"""
from pathlib import Path

import pandas as pd

# --- Paths -------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
RESULTS_DIR = ROOT / "results"

SALES_CSV = RAW_DIR / "sales.csv"
ITEMS_CSV = RAW_DIR / "items.csv"
CUSTOMERS_CSV = RAW_DIR / "customers.csv"

# --- Data window ---------------------------------------------------------------
DATA_START = pd.Timestamp("2022-11-01")   # first sales row
DATA_END = pd.Timestamp("2026-10-31")     # last sales row
AS_OF_DATE = DATA_END                     # "today" for churn / trailing-12m metrics

# --- Key dates (see docs/definitions.md) ---------------------------------------
COMPETITOR_OPEN = pd.Timestamp("2024-03-01")   # WORKING ESTIMATE — Person A to confirm
LOYALTY_LAUNCH = pd.Timestamp("2024-06-01")
PILATES_START = pd.Timestamp("2025-01-06")
PILATES_END = pd.Timestamp("2025-03-31")
REPAIRS_LAUNCH = pd.Timestamp("2025-04-01")
WEBSITE_LAUNCH = pd.Timestamp("2025-11-17")
NEW_MANAGER = pd.Timestamp("2026-02-02")

EVENTS = {
    "competitor_open": COMPETITOR_OPEN,
    "loyalty_launch": LOYALTY_LAUNCH,
    "pilates_start": PILATES_START,
    "pilates_end": PILATES_END,
    "repairs_launch": REPAIRS_LAUNCH,
    "website_launch": WEBSITE_LAUNCH,
    "new_manager": NEW_MANAGER,
}

# --- Loyalty -------------------------------------------------------------------
POINTS_PER_DOLLAR_REDEEMED = 20          # 20 points = $1 off
SILVER_THRESHOLD = 600                   # trailing-365-day points
GOLD_THRESHOLD = 2000
TIER_WINDOW_DAYS = 365
PRE_LOYALTY = "Pre-loyalty"              # label for blank tier before LOYALTY_LAUNCH
TIER_ORDER = [PRE_LOYALTY, "Non-member", "Member", "Silver", "Gold"]
TIER_RANK = {t: i for i, t in enumerate(TIER_ORDER)}

# --- Profit / cost rules -------------------------------------------------------
# Profit = Revenue − Production Costs − Repair Costs − Redeemed Points ($)
RETURN_COST_REVERSES = True   # PLACEHOLDER — team decision pending (decisions_log.md)
REPAIR_ITEMS = {"R01": "outerwear", "R02": "activewear"}   # cost $45 / $18, price $0

# --- Customer definitions ------------------------------------------------------
CHURN_DAYS = 180              # churned = no visit in the last 180 days
ARR_WINDOW_MONTHS = 12        # ARR = repeat-customer revenue over trailing 12 months
# Repeat visit = a visit dated after the customer's signup_date.

# --- Row types -----------------------------------------------------------------
PURCHASE, RETURN = "Purchase", "Return"
DROPOFF, PICKUP = "Repair Drop-off", "Repair Pickup"
ROW_TYPES = [PURCHASE, RETURN, DROPOFF, PICKUP]

# --- Customer interests (split into 0/1 columns interest_<name>) ---------------
INTERESTS = ["Run", "Yoga", "Pilates", "Outdoor", "Lifestyle"]

# --- Shared output ---------------------------------------------------------------
# The ONE cleaned, joined dataset everyone starts from (one row per sales line).
CLEAN_CSV = PROCESSED_DIR / "lululime_clean.csv.gz"
