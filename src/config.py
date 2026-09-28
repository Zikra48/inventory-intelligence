"""Shared settings; paths are independent of the terminal's working directory."""
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
SAMPLE_DATA_PATH = DATA_DIR / "sample_inventory.csv"
MODEL_DIR = PROJECT_ROOT / "models" / "saved_models"
REQUIRED_COLUMNS = (
    "date", "sku_id", "product_name", "category", "sales_quantity",
    "current_stock", "unit_price", "supplier_lead_time",
)

@dataclass(frozen=True)
class Settings:
    app_title: str = "Intelligent FMCG Inventory"
    currency: str = "PKR"
    forecast_horizon_days: int = 7
    review_period_days: int = 7
    safety_buffer_days: int = 2
    random_seed: int = 42
    sample_days: int = 180
    sample_end_date: str = "2026-09-27"

SETTINGS = Settings()
