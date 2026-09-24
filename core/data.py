"""Market data access. This module never connects to a broker account."""

import pandas as pd
import yfinance as yf


def fetch_candles(symbol: str, interval: str, period: str) -> pd.DataFrame:
    data = yf.download(symbol, interval=interval, period=period, auto_adjust=False, progress=False)
    if data is None or data.empty:
        raise ValueError(f"No market data returned for {symbol}. Check the symbol and timeframe.")
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    required = {"Open", "High", "Low", "Close"}
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"Market data is missing columns: {', '.join(sorted(missing))}")
    data = data.dropna(subset=["Open", "High", "Low", "Close"]).copy()
    if len(data) < 40:
        raise ValueError("Not enough candles for analysis; choose a larger data period or timeframe.")
    return data
