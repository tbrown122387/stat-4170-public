"""
Run this script once to download all data shared across the module slides.
The slides load from lectures/data/*.csv rather than hitting Yahoo/FRED on
every render.

Usage:
    conda activate quant-ts
    python fetch_data.py
"""
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# --- Equity / sector SPDR prices (modules 1, 2, 6) ---------------------

PRICE_TICKERS = [
    "AAPL", "TSLA",
    "XLC", "XLY", "XLP", "XLE", "XLF",
    "XLV", "XLI", "XLB", "XLRE", "XLK", "XLU",
    "SPY",
]

print("Downloading equity/sector price data from Yahoo Finance...")
prices = yf.download(
    PRICE_TICKERS,
    start="2020-01-01",
    end="2024-12-31",
    auto_adjust=True,
    progress=False,
)["Close"]
prices.to_csv(DATA_DIR / "prices.csv")
print(f"Saved {len(prices)} rows to data/prices.csv")

# --- FX spot rates (modules 3-6) ----------------------------------------

fx_tickers = {
    "AUDUSD": "AUDUSD=X",
    "USDJPY": "USDJPY=X",
    "AUDJPY": "AUDJPY=X",
    "EURUSD": "EURUSD=X",
    "GBPUSD": "GBPUSD=X",
    "NZDUSD": "NZDUSD=X",
}

print("Downloading FX data from Yahoo Finance...")
fx = yf.download(
    list(fx_tickers.values()),
    start="2010-01-01",
    auto_adjust=True,
    progress=False,
)["Close"]
fx.columns = list(fx_tickers.keys())
fx.to_csv(DATA_DIR / "fx_rates.csv")
print(f"Saved {len(fx)} rows to data/fx_rates.csv")

# --- Short-term interest rates from FRED (annualized %, monthly) --------
# IRSTCI01AUM156N: Australia overnight call money/interbank rate
# IRSTCI01JPM156N: Japan overnight call money/interbank rate

print("Downloading interest rate data from FRED...")
fred_series = {
    "AUD_rate": "IRSTCI01AUM156N",
    "JPY_rate": "IRSTCI01JPM156N",
}
frames = []
for col, series_id in fred_series.items():
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    s = pd.read_csv(url, index_col=0, parse_dates=True, na_values=".")
    s.columns = [col]
    frames.append(s)

rates = pd.concat(frames, axis=1, sort=True)
rates.to_csv(DATA_DIR / "rates.csv")
print(f"Saved {len(rates)} rows to data/rates.csv")

# --- Carry P&L for the AUD/JPY carry trade (modules 3-6) -----------------
# Spot return + accrued rate differential, compounded over the actual
# number of calendar days between observations (so weekend/holiday accrual
# is included, unlike a flat /252 approximation).

print("Computing AUD/JPY carry P&L...")
audjpy = fx["AUDJPY"].dropna()
log_ret = np.log(audjpy).diff().dropna() * 100  # spot return, %

aud_rate = rates["AUD_rate"].reindex(log_ret.index, method="ffill")
jpy_rate = rates["JPY_rate"].reindex(log_ret.index, method="ffill")

calendar_days = log_ret.index.to_series().diff().dt.days


def accrued_pct(annual_rate_pct, n_days, day_count=365):
    return ((1 + annual_rate_pct / 100) ** (n_days / day_count) - 1) * 100


aud_accrued = accrued_pct(aud_rate, calendar_days)
jpy_accrued = accrued_pct(jpy_rate, calendar_days)

carry_pnl = (log_ret + aud_accrued - jpy_accrued).dropna().rename("carry_pnl")
carry_pnl.to_csv(DATA_DIR / "carry_pnl.csv")
print(f"Saved {len(carry_pnl)} rows to data/carry_pnl.csv")
