import pandas as pd

from src.analysis import compute_risk_metrics, enrich_time_series


def test_enrich_time_series_adds_expected_columns():
    frame = pd.DataFrame({"Close": [10.0, 11.0, 12.0]}, index=pd.date_range("2024-01-01", periods=3))

    enriched = enrich_time_series(frame)

    assert {"daily_return", "rolling_mean_20", "rolling_volatility_20"}.issubset(enriched.columns)
    assert abs(enriched["daily_return"].iloc[1] - 0.1) < 1e-9


def test_compute_risk_metrics_returns_expected_keys():
    returns = pd.Series([0.01, -0.02, 0.03, 0.01])

    metrics = compute_risk_metrics(returns)

    assert set(metrics) == {"mean_return", "volatility", "sharpe_ratio", "var_95"}
    assert metrics["var_95"] < metrics["mean_return"]
