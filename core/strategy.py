"""Transparent, conservative baseline strategies for research only."""

from datetime import datetime
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd


PAKISTAN_TZ = ZoneInfo("Asia/Karachi")


def _indicators(candles: pd.DataFrame) -> pd.DataFrame:
    df = candles.copy()
    close = df["Close"].astype(float)
    df["fast_ma"] = close.ewm(span=9, adjust=False).mean()
    df["slow_ma"] = close.ewm(span=21, adjust=False).mean()
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = -delta.clip(upper=0).rolling(14).mean()
    rs = gain / loss.replace(0, np.nan)
    df["rsi"] = (100 - (100 / (1 + rs))).fillna(50)
    df["atr"] = (df["High"] - df["Low"]).rolling(14).mean()
    return df.dropna().copy()


def _base_analysis(candles: pd.DataFrame):
    df = _indicators(candles)
    if len(df) < 5:
        raise ValueError("Not enough valid candles after calculating indicators.")
    last = df.iloc[-1]
    previous = df.iloc[-2]
    bullish = last.fast_ma > last.slow_ma and last.rsi >= 50 and last.Close >= previous.Close
    bearish = last.fast_ma < last.slow_ma and last.rsi <= 50 and last.Close <= previous.Close
    if bullish:
        trend, direction = "Bullish", "up"
    elif bearish:
        trend, direction = "Bearish", "down"
    else:
        trend, direction = "Mixed", "unclear"
    strength = 50
    if direction in {"up", "down"}:
        strength += min(20, abs(float(last.rsi) - 50) * 0.6)
        strength += min(15, abs(float(last.fast_ma - last.slow_ma)) / max(float(last.Close), 1e-9) * 10000)
    volatility = "High" if float(last.atr / last.Close) > 0.004 else "Normal"
    return df, last, trend, direction, round(min(strength, 85)), volatility


def _result(signal, timeframe, reasons, strength, trend, volatility, last):
    return {
        "signal": signal,
        "strength": strength,
        "close": f"{float(last.Close):.6f}",
        "trend": trend,
        "rsi": f"{float(last.rsi):.2f}",
        "fast_ma": f"{float(last.fast_ma):.6f}",
        "slow_ma": f"{float(last.slow_ma):.6f}",
        "volatility": volatility,
        "reasons": reasons + [f"Selected timeframe: {timeframe}"],
        "timestamp": datetime.now(PAKISTAN_TZ).strftime("%Y-%m-%d %H:%M:%S PKT"),
    }


def analyze_binary(candles: pd.DataFrame, timeframe: str):
    _, last, trend, direction, strength, volatility = _base_analysis(candles)
    reasons = ["CALL/PUT is based on moving-average direction, RSI, and the latest candle."]
    if direction == "up" and volatility == "Normal":
        signal = "CALL"
        reasons.append("Momentum is upward and volatility is within the baseline range.")
    elif direction == "down" and volatility == "Normal":
        signal = "PUT"
        reasons.append("Momentum is downward and volatility is within the baseline range.")
    else:
        signal = "NO TRADE"
        reasons.append("Trend is mixed or volatility is high; waiting is safer.")
    return _result(signal, timeframe, reasons, strength, trend, volatility, last)


def analyze_forex(candles: pd.DataFrame, timeframe: str):
    _, last, trend, direction, strength, volatility = _base_analysis(candles)
    reasons = ["BUY/SELL is based on moving-average direction, RSI, and the latest candle."]
    if direction == "up":
        signal = "BUY"
        reasons.append("Fast moving average is above slow moving average with positive momentum.")
    elif direction == "down":
        signal = "SELL"
        reasons.append("Fast moving average is below slow moving average with negative momentum.")
    else:
        signal = "NO TRADE"
        reasons.append("Trend confirmation is insufficient.")
    return _result(signal, timeframe, reasons, strength, trend, volatility, last)
