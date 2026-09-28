# Intelligent FMCG Inventory Forecasting and Decision Support System

## Phase 1 — runnable project foundation

This student MVP will help inventory managers decide which products need
replenishment using short-term demand forecasts and transparent inventory rules.
Phase 1 provides the project structure, configuration, sample-data generator,
and Streamlit starter. It is not yet a complete or production-ready system.

## Installation and running (Windows)

Install Python 3.11 or 3.12. Extract the ZIP and open its `inventory_intelligence`
folder in VS Code. Run these commands in the VS Code terminal:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m scripts.generate_sample_data
.venv\Scripts\python.exe -m unittest discover -s tests -v
.venv\Scripts\python.exe -m streamlit run app.py
```

Open the local URL printed by Streamlit (normally http://localhost:8501).
Stop the app with Ctrl+C. Explicitly using the virtual environment's Python
avoids PowerShell activation restrictions.

For macOS/Linux, create the environment with `python3 -m venv .venv` and replace
`.venv\Scripts\python.exe` with `.venv/bin/python` in the remaining commands.

## Where files go and why

Keep the extracted folder structure intact; all paths below are relative to it.

| File or directory | Purpose |
|---|---|
| `app.py` | Runnable Streamlit starter and synthetic data preview |
| `src/config.py` | Central paths, required columns, and configurable defaults |
| `scripts/generate_sample_data.py` | Reproducible daily sales and inventory simulation |
| `data/sample_inventory.csv` | Generated example, also bundled for convenience |
| `data/sample_inventory.metadata.json` | Synthetic-data label and generation assumptions |
| `src/data_loader.py`, `src/preprocessing.py`, `src/feature_engineering.py` | Reserved for Phase 2 |
| `src/forecasting.py`, `src/evaluation.py` | Reserved for Phase 3 |
| `src/inventory_risk.py` | Reserved for Phase 4 |
| `src/replenishment.py`, `src/explanations.py` | Reserved for Phase 5 |
| `pages/` | Reserved for the five dashboard views in Phase 6 |
| `models/saved_models/` | Reserved for later saved models |
| `tests/test_setup.py` | Executable sample-data and starter-app checks |
| `requirements.txt` | Compatible dependency ranges |
| `requirements-tested.txt` | Exact direct-package versions in the verification environment |

The reserved modules contain only descriptive docstrings. They do not return
pretend forecasts or decisions. Complete runnable Phase 1 code is included in
the other Python files.

## Architecture and next phases

Planned flow: CSV → validation → feature engineering → demand forecast →
inventory risk → replenishment recommendation → dashboard.

1. **Setup (implemented):** create folders, settings, sample data and starter UI.
2. **Data pipeline:** validate uploads, report cleaning decisions, create lagged features.
3. **Forecasting:** compare a seven-day moving average with Random Forest using
   chronological, seven-day forecast windows. Fit on past data only; use shifted
   rolling features and recursive forecasts without held-out actuals. Report MAE
   and WAPE, define zero-demand behavior, and retain the baseline if it wins.
4. **Inventory risk:** estimate lead-time demand and a configurable safety buffer.
5. **Decisions:** calculate actions, nonnegative quantities and clear explanations.
6. **Dashboard:** Overview, Demand Forecast, Inventory Risk, Replenishment, SKU Detail.
7. **Business tests:** verify hand-calculated examples and edge cases.
8. **Full documentation:** update assumptions and measured model results.

No forecast metrics have been calculated in Phase 1. No claim of ML improvement
is made. Model selection and business-rule definitions will be implemented and
verified in their respective phases.

## Dataset contract and explicit assumptions

One location; one row per SKU per calendar day. Unit prices are illustrative PKR
selling prices. A price-based stock value later will therefore be a **retail-value
estimate**, not an accounting valuation at purchase cost.

| Column | Meaning |
|---|---|
| `date` | Business date, YYYY-MM-DD |
| `sku_id` | Stable product identifier |
| `product_name` | Readable product name |
| `category` | Product group |
| `sales_quantity` | Fulfilled units sold during that day |
| `current_stock` | Closing on-hand units after receipts and sales |
| `unit_price` | Selling price per unit, in PKR |
| `supplier_lead_time` | Positive whole calendar days to supplier delivery |

Historical stock snapshots must not be summed. Future inventory overview will
use the latest valid snapshot for each SKU and identify stale dates. Missing days
in real data cannot automatically be assumed to mean zero demand.

Defaults in `src/config.py`: forecast horizon 7 days, review period 7 days,
safety buffer 2 days, random seed 42. Business defaults are provisional settings;
they do not run an inventory decision engine yet. Open orders and backorders are
not available in the proposed CSV, so future recommendations must disclose this.

## How the generator works

The fixed seed reproduces the same sample for the same arguments. Eight products
have different baseline demand levels. Weekends and a mild 30-day cycle affect
demand; biscuits also have a rising trend. Poisson draws add daily count variation.
Sales reduce stock; simulated orders arrive after supplier lead time. Cooking oil
stops receiving new orders near the end to demonstrate inventory depletion.

These are illustrative patterns, not evidence about Multan businesses. Stockouts
can censor observed sales: zero sales may mean zero stock, not zero demand.
The export excludes simulated receipts and pending orders; this limits subsequent
replenishment analysis and must be explained in later phases.

Regenerate a different period from the project root:

```powershell
.venv\Scripts\python.exe -m scripts.generate_sample_data --days 365 --end-date 2026-09-27 --seed 42
```

The default output is deliberately overwritten when regenerating. Default tests
expect the bundled 180-day example; regenerate with no options before running them.

## Expected Phase 1 output and verification

The default generator prints `SYNTHETIC: 1,440 rows | 8 SKUs | 180 days per SKU`.
The date range is 2026-04-01 through 2026-09-27. The app displays the synthetic
warning, three sample-data metrics, a preview table and CSV download.

Four tests check schema, complete daily coverage, nonnegative data, reproducibility,
short-history generation, invalid days, and Streamlit execution with expected metrics.
See `VERIFICATION.md` for actual execution results. These checks verify setup,
not forecasting accuracy or production readiness.

## Common errors

| Problem | Fix |
|---|---|
| `python` not recognized | Install Python, enable PATH, reopen terminal; Windows `py` may also work |
| `No module named streamlit` | Install requirements using the same environment's Python |
| `No module named src` | Run module commands from the extracted `inventory_intelligence` folder |
| Missing or corrupted sample | Run `python -m scripts.generate_sample_data` with the environment's Python |
| Port 8501 in use | Add `--server.port 8502` to the Streamlit command |
| Dependency download fails | Check network access and retry the install command |

This phase deliberately stops before uploading/cleaning real CSVs. Later additions
such as expiry prediction, supplier-delay prediction, clustering, and a chatbot
remain outside the five-module MVP.
