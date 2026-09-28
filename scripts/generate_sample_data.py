"""Generate reproducible SYNTHETIC daily FMCG sales and closing stock."""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import REQUIRED_COLUMNS, SAMPLE_DATA_PATH, SETTINGS

# SKU, name, category, base daily demand, price, lead days, demand pattern
PRODUCTS = (
    ("SKU001", "Cooking Oil 1L", "Pantry", 21, 580, 4, "approaching_stockout"),
    ("SKU002", "Milk 1L", "Dairy", 65, 300, 2, "high"),
    ("SKU003", "Tea 190g", "Beverages", 13, 450, 5, "stable"),
    ("SKU004", "Biscuits 100g", "Snacks", 28, 80, 3, "increasing"),
    ("SKU005", "Detergent 1kg", "Household", 9, 520, 6, "stable"),
    ("SKU006", "Specialty Sauce 250ml", "Pantry", 1.2, 350, 7, "low"),
    ("SKU007", "Bottled Water 1.5L", "Beverages", 80, 110, 2, "high"),
    ("SKU008", "Soap 100g", "Personal Care", 17, 140, 4, "stable"),
)

def generate_sample_data(days=SETTINGS.sample_days, seed=SETTINGS.random_seed,
                         end_date=SETTINGS.sample_end_date):
    """One row per SKU/date. Sales are fulfilled demand, not unconstrained demand."""
    if not isinstance(days, int) or days < 1:
        raise ValueError("days must be a positive integer")
    end = pd.Timestamp(end_date)
    if pd.isna(end) or end.tz is not None:
        raise ValueError("end_date must be a valid date without a timezone")
    dates = pd.date_range(end=end.normalize(), periods=days)
    rng = np.random.default_rng(seed)
    rows = []
    for sku, name, category, base, price, lead, pattern in PRODUCTS:
        stock = int(np.ceil(base * (lead + 12)))
        pending = []
        for day_index, date in enumerate(dates):
            stock += sum(qty for arrival, qty in pending if arrival == day_index)
            pending = [(arrival, qty) for arrival, qty in pending if arrival > day_index]
            trend = 1 + (0.8 * day_index / max(days - 1, 1) if pattern == "increasing" else 0)
            weekly = 1.25 if date.dayofweek >= 5 else 0.90
            seasonal = 1 + 0.08 * np.sin(2 * np.pi * day_index / 30)
            mean = base * trend * weekly * seasonal
            demand = int(rng.poisson(mean))
            sales = min(stock, demand)
            stock -= sales
            rows.append((date.strftime("%Y-%m-%d"), sku, name, category,
                         sales, stock, price, lead))
            # Stop ordering this one product near the end to illustrate depletion.
            pause_orders = pattern == "approaching_stockout" and day_index >= days - 18
            inventory_position = stock + sum(qty for _, qty in pending)
            if not pause_orders and inventory_position <= mean * (lead + 3):
                quantity = max(0, int(np.ceil(mean * (lead + 12) - inventory_position)))
                pending.append((day_index + lead, quantity))
    return pd.DataFrame(rows, columns=REQUIRED_COLUMNS).sort_values(
        ["sku_id", "date"], ignore_index=True
    )

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--days", type=int, default=SETTINGS.sample_days)
    parser.add_argument("--seed", type=int, default=SETTINGS.random_seed)
    parser.add_argument("--end-date", default=SETTINGS.sample_end_date)
    parser.add_argument("--output", type=Path, default=SAMPLE_DATA_PATH)
    args = parser.parse_args()
    try:
        frame = generate_sample_data(args.days, args.seed, args.end_date)
    except (ValueError, TypeError) as exc:
        parser.error(str(exc))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(args.output, index=False)
    metadata = {
        "synthetic": True, "seed": args.seed, "days_per_sku": args.days,
        "rows": len(frame), "start_date": frame.date.min(), "end_date": frame.date.max(),
        "currency": SETTINGS.currency,
        "stock_semantics": "Closing on-hand units after receipts and fulfilled sales",
        "limitations": "Illustrative prices and patterns; not observed Multan industry data. Sales may be censored by stockouts. Receipts and pending orders are not exported.",
        "patterns": {p[0]: p[6] for p in PRODUCTS},
    }
    args.output.with_suffix(".metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(f"SYNTHETIC: {len(frame):,} rows | {frame.sku_id.nunique()} SKUs | {args.days} days per SKU")
    print(f"Saved: {args.output.resolve()}")

if __name__ == "__main__":
    main()
