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
df = load()   # one joined table; build visits / customers / ARR with the SPRINT_CONTEXT.md cheat sheet

# %% [markdown]
# ## 3. ARR over time (Stream D, slide 3)

# %%

# %% [markdown]
# ## 4. Competitor impact & seasonality (Stream A, slide 4)

# %%

# %% [markdown]
# ## 5. Loyalty program: revenue vs profit, points-funded returns (Stream B, slides 5-6)

# %%

# %% [markdown]
# ## 6. Repairs: churn and cost vs ARR at risk, with scenarios (Stream C, slides 7-8)

# %%

# %% [markdown]
# ## 7. Pilates campaign (Stream D, slide 9)

# %%

# %% [markdown]
# ## 8. Recommendation, KPIs & risks (Stream D, slide 10)
