# Time Series Forecasting for Portfolio Management Optimization

**Client:** GMF Investments &nbsp;|&nbsp; **Program:** 10 Academy Kifiya AI Mastery Program — Week 9

## Business Context

GMF Investments is a financial advisory firm specializing in personalized, data-driven portfolio management. This project applies time series forecasting and Modern Portfolio Theory to translate historical market data into an actionable, risk-aware portfolio recommendation — simulating the role of a Financial Analyst at GMF who must justify allocation decisions to an investment committee, not just produce a forecast in isolation.

## Assets

| Ticker | Description | Risk Profile |
|---|---|---|
| **TSLA** | Tesla — high-growth consumer discretionary stock | High risk, high potential return |
| **BND** | Vanguard Total Bond Market ETF | Low risk, stability and income |
| **SPY** | S&P 500 ETF | Moderate risk, broad market exposure |

Data period: **January 1, 2015 – June 30, 2026**, sourced via the [yfinance](https://pypi.org/project/yfinance/) API.

## Project Structure

```text
portfolio-optimization/
├── data/
│   └── processed/
├── notebooks/
├── scripts/
├── src/
│   ├── data_loader.py
│   └── analysis.py
├── tests/
└── .github/workflows/
```

## Development Workflow

1. Create and activate a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Run the test suite with `pytest tests/ -v`.
4. Use the notebooks for exploratory analysis and the reusable modules in `src/` for production-style logic.

## CI

GitHub Actions runs automated tests on every push and pull request to `main` via [.github/workflows/unittests.yml](.github/workflows/unittests.yml).

## Notes

- The data loader centralizes fetching, saving, and loading of processed financial data.
- The analysis module provides reusable helpers for returning metrics and rolling statistics so notebook logic is easier to test.
- The notebooks remain the main place for visualization and experimentation, while core logic is moved into reusable Python modules when possible.
