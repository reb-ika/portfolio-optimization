"""Reusable helpers for basic time-series analysis and risk metrics."""
from __future__ import annotations

import numpy as np
import pandas as pd


def enrich_time_series(frame: pd.DataFrame, price_column: str = "Close") -> pd.DataFrame:
    """Add simple return and rolling statistics to a price series DataFrame."""
    if price_column not in frame.columns:
        raise KeyError(f"Expected price column '{price_column}' in the input frame.")

    enriched = frame.copy().sort_index()
    enriched["daily_return"] = enriched[price_column].pct_change()
    enriched["rolling_mean_20"] = enriched[price_column].rolling(window=20).mean()
    enriched["rolling_volatility_20"] = enriched["daily_return"].rolling(window=20).std()
    return enriched


def compute_risk_metrics(series: pd.Series, risk_free_rate: float = 0.0) -> dict[str, float]:
    """Compute basic risk metrics for a return series."""
    clean_series = series.dropna()
    if clean_series.empty:
        return {
            "mean_return": float("nan"),
            "volatility": float("nan"),
            "sharpe_ratio": float("nan"),
            "var_95": float("nan"),
        }

    mean_return = float(clean_series.mean())
    volatility = float(clean_series.std(ddof=0))
    sharpe_ratio = float((mean_return - risk_free_rate) / volatility) if volatility else float("nan")
    var_95 = float(np.percentile(clean_series, 5))

    return {
        "mean_return": mean_return,
        "volatility": volatility,
        "sharpe_ratio": sharpe_ratio,
        "var_95": var_95,
    }
