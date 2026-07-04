"""
data_loader.py
Fetches and caches historical price data for TSLA, BND, SPY from yfinance.
"""
import os
import pandas as pd
import yfinance as yf

TICKERS = ["TSLA", "BND", "SPY"]
START_DATE = "2015-01-01"
END_DATE = "2026-06-30"
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")


def fetch_asset_data(tickers=TICKERS, start=START_DATE, end=END_DATE):
    """
    Downloads daily OHLCV data for each ticker individually.
    Returns a dict of {ticker: DataFrame}.
    """
    data = {}
    for ticker in tickers:
        print(f"Fetching {ticker}...")
        df = yf.download(ticker, start=start, end=end, auto_adjust=False)
        # yfinance sometimes returns MultiIndex columns even for a single ticker
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df["Ticker"] = ticker
        data[ticker] = df
    return data


def save_processed(data: dict, out_dir: str = PROCESSED_DIR):
    """Saves each ticker's DataFrame as a CSV in data/processed/."""
    os.makedirs(out_dir, exist_ok=True)
    for ticker, df in data.items():
        path = os.path.join(out_dir, f"{ticker}.csv")
        df.to_csv(path)
        print(f"Saved {ticker} -> {path} ({len(df)} rows)")


def load_combined(tickers=TICKERS, out_dir: str = PROCESSED_DIR):
    """
    Loads previously saved CSVs and combines them into one long-format DataFrame
    with columns: Date, Open, High, Low, Close, Adj Close, Volume, Ticker.
    """
    frames = []
    for ticker in tickers:
        path = os.path.join(out_dir, f"{ticker}.csv")
        df = pd.read_csv(path, index_col=0, parse_dates=True)
        frames.append(df)
    combined = pd.concat(frames)
    combined.index.name = "Date"
    return combined


if __name__ == "__main__":
    raw = fetch_asset_data()
    save_processed(raw)