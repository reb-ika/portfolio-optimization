"""
data_loader.py
Fetches and caches historical price data for TSLA, BND, SPY from yfinance.
Includes error handling for network failures, empty responses, and missing files.
"""
import os
import logging
import pandas as pd
import yfinance as yf

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

TICKERS = ["TSLA", "BND", "SPY"]
START_DATE = "2015-01-01"
END_DATE = "2026-06-30"
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")


def fetch_asset_data(tickers=TICKERS, start=START_DATE, end=END_DATE):
    """
    Downloads daily OHLCV data for each ticker individually.
    Returns a dict of {ticker: DataFrame}. Tickers that fail to download
    are skipped with a logged warning rather than crashing the whole run.
    """
    data = {}
    for ticker in tickers:
        logger.info(f"Fetching {ticker}...")
        try:
            df = yf.download(ticker, start=start, end=end, auto_adjust=False)
        except Exception as e:
            logger.error(f"Failed to download {ticker}: {e}")
            continue

        if df is None or df.empty:
            logger.warning(f"No data returned for {ticker} — skipping.")
            continue

        # yfinance sometimes returns MultiIndex columns even for a single ticker
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df["Ticker"] = ticker
        data[ticker] = df
        logger.info(f"Fetched {len(df)} rows for {ticker}")

    if not data:
        raise RuntimeError("No data was successfully fetched for any ticker.")

    return data


def save_processed(data: dict, out_dir: str = PROCESSED_DIR):
    """Saves each ticker's DataFrame as a CSV in data/processed/."""
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as e:
        raise RuntimeError(f"Could not create output directory {out_dir}: {e}")

    for ticker, df in data.items():
        path = os.path.join(out_dir, f"{ticker}.csv")
        try:
            df.to_csv(path)
            logger.info(f"Saved {ticker} -> {path} ({len(df)} rows)")
        except OSError as e:
            logger.error(f"Failed to save {ticker} to {path}: {e}")


def load_combined(tickers=TICKERS, out_dir: str = PROCESSED_DIR):
    """
    Loads previously saved CSVs and combines them into one long-format DataFrame
    with columns: Date, Open, High, Low, Close, Adj Close, Volume, Ticker.
    Raises a clear error if a required file is missing rather than a raw
    FileNotFoundError from pandas.
    """
    frames = []
    for ticker in tickers:
        path = os.path.join(out_dir, f"{ticker}.csv")
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Expected processed data for {ticker} at {path}, but it doesn't exist. "
                f"Run 'python src/data_loader.py' first to fetch and save the data."
            )
        try:
            df = pd.read_csv(path, index_col=0, parse_dates=True)
        except pd.errors.EmptyDataError:
            raise ValueError(f"{path} exists but is empty or corrupted.")
        frames.append(df)

    if not frames:
        raise RuntimeError("No ticker data could be loaded.")

    combined = pd.concat(frames)
    combined.index.name = "Date"
    return combined


if __name__ == "__main__":
    try:
        raw = fetch_asset_data()
        save_processed(raw)
    except RuntimeError as e:
        logger.error(f"Data pipeline failed: {e}")
        raise