# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
# ---

# %% [markdown]
# # Lululime — Should leadership scrap repairs and expand loyalty?
# Dataverse 2026 · Final notebook. Edit `summary.py`, then generate the notebook with:
# `jupytext --to notebook summary.py -o summary.ipynb`

# %% [markdown]
# ## 1. Problem framing

# %%
from src import config as C
from src.metrics import load, company_arr, churn_rate, period

# %% [markdown]
# ## 2. Data & methodology
# Cleaning and joins live in `src/` (see `docs/data_notes.md`). Rebuilding the tables reruns the integrity checks.

# %%
# from src.tables import build_all; build_all()   # uncomment to rebuild and show the checks
lines, visits, customers = load("lines"), load("visits"), load("customers")
customer_month, links = load("customer_month"), load("links")

# %% [markdown]
# ## 3. Competitor impact & seasonality (Stream A)

# %%

# %% [markdown]
# ## 4. Loyalty program (Stream B)

# %%

# %% [markdown]
# ## 5. Free repair program (Stream C)

# %%

# %% [markdown]
# ## 6. Customers & ARR (Stream D)

# %%

# %% [markdown]
# ## 7. Recommendation, risks & KPIs
