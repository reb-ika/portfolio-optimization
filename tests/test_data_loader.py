"""
Unit tests for src/data_loader.py
Run with: pytest tests/ -v
"""
import os
import sys
import pandas as pd
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.data_loader import load_combined, save_processed, PROCESSED_DIR


def test_save_processed_creates_files(tmp_path):
    """save_processed should write one CSV per ticker into the output dir."""
    fake_data = {
        "TEST": pd.DataFrame({
            "Open": [1.0, 2.0],
            "Close": [1.1, 2.1],
            "Ticker": ["TEST", "TEST"],
        }, index=pd.date_range("2024-01-01", periods=2))
    }
    save_processed(fake_data, out_dir=str(tmp_path))
    assert (tmp_path / "TEST.csv").exists()


def test_load_combined_missing_file_raises(tmp_path):
    """load_combined should raise a clear FileNotFoundError if a CSV is missing."""
    with pytest.raises(FileNotFoundError):
        load_combined(tickers=["NONEXISTENT"], out_dir=str(tmp_path))


def test_load_combined_returns_dataframe(tmp_path):
    """load_combined should correctly read back and combine saved CSVs."""
    fake_data = {
        "AAA": pd.DataFrame({
            "Open": [10.0], "Close": [11.0], "Ticker": ["AAA"]
        }, index=pd.date_range("2024-01-01", periods=1)),
        "BBB": pd.DataFrame({
            "Open": [20.0], "Close": [21.0], "Ticker": ["BBB"]
        }, index=pd.date_range("2024-01-01", periods=1)),
    }
    save_processed(fake_data, out_dir=str(tmp_path))
    result = load_combined(tickers=["AAA", "BBB"], out_dir=str(tmp_path))

    assert isinstance(result, pd.DataFrame)
    assert set(result["Ticker"].unique()) == {"AAA", "BBB"}
    assert len(result) == 2


def test_processed_dir_default_path_exists_as_string():
    """Sanity check that the default PROCESSED_DIR constant is a valid path string."""
    assert isinstance(PROCESSED_DIR, str)
    assert "data" in PROCESSED_DIR