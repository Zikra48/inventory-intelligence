"""Phase 1 checks; use Python's built-in unittest runner."""
import unittest
import pandas as pd
from scripts.generate_sample_data import generate_sample_data
from src.config import REQUIRED_COLUMNS

class SetupTests(unittest.TestCase):
    def test_sample_contract(self):
        frame = generate_sample_data()
        self.assertEqual(frame.shape, (1440, 8))
        self.assertEqual(tuple(frame.columns), REQUIRED_COLUMNS)
        self.assertFalse(frame.isna().any().any())
        self.assertFalse(frame.duplicated(["sku_id", "date"]).any())
        self.assertTrue((frame[["sales_quantity", "current_stock", "unit_price"]] >= 0).all().all())
        self.assertTrue((frame.supplier_lead_time > 0).all())
        for _, sku in frame.groupby("sku_id"):
            self.assertTrue(pd.to_datetime(sku.date).diff().dropna().eq(pd.Timedelta(days=1)).all())

    def test_reproducibility(self):
        pd.testing.assert_frame_equal(generate_sample_data(), generate_sample_data())

    def test_short_history_and_invalid_days(self):
        self.assertEqual(len(generate_sample_data(days=1)), 8)
        with self.assertRaises(ValueError):
            generate_sample_data(days=0)

    def test_streamlit_starter(self):
        from streamlit.testing.v1 import AppTest
        from src.config import PROJECT_ROOT
        app = AppTest.from_file(str(PROJECT_ROOT / "app.py")).run(timeout=20)
        self.assertEqual(len(app.exception), 0)
        self.assertEqual([metric.value for metric in app.metric], ["8", "1,440", "180"])

if __name__ == "__main__":
    unittest.main()
