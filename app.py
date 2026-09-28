"""Phase 1 starter. Only the bundled sample is read; upload validation comes next."""
import pandas as pd
import streamlit as st

from src.config import REQUIRED_COLUMNS, SAMPLE_DATA_PATH, SETTINGS

st.set_page_config(page_title=SETTINGS.app_title, page_icon="📦", layout="wide")
st.title(SETTINGS.app_title)
st.caption("Forecasting and decision support • Phase 1: project setup")
st.warning("SYNTHETIC DEMO DATA — illustrative products, sales and prices.")
st.sidebar.title("Project status")
st.sidebar.success("Phase 1 • Setup")
st.sidebar.info("Next: CSV validation and preprocessing")
st.info("This starter verifies the project and sample data. Forecasts, risk levels, recommendations and CSV upload will be added in later phases.")

if not SAMPLE_DATA_PATH.exists():
    st.error("Sample data is missing. Run: python -m scripts.generate_sample_data")
    st.stop()
try:
    data = pd.read_csv(SAMPLE_DATA_PATH)
    if data.empty or not set(REQUIRED_COLUMNS).issubset(data.columns):
        raise ValueError("The bundled sample is empty or has missing columns.")
except (OSError, ValueError, pd.errors.ParserError) as exc:
    st.error(f"Could not read the sample data: {exc}")
    st.code("python -m scripts.generate_sample_data")
    st.stop()

a, b, c = st.columns(3)
a.metric("Sample products", data.sku_id.nunique())
b.metric("Sample records", f"{len(data):,}")
c.metric("Days per product", data.date.nunique())
st.subheader("Sample data preview")
st.caption(f"Dates: {data.date.min()} to {data.date.max()} • Prices in {SETTINGS.currency}")
st.dataframe(data.head(24), use_container_width=True, hide_index=True)
st.download_button("Download synthetic CSV", data.to_csv(index=False),
                   file_name="synthetic_sample_inventory.csv", mime="text/csv")
with st.expander("What does one row mean?"):
    st.write("One product on one day. Sales are fulfilled units that day; current_stock is closing on-hand inventory. Historical stock must never be summed to calculate today's stock.")
