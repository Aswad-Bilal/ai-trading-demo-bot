# Demo Trading Signal Assistant

A local, signal-only desktop application with two separate systems:

- **Binary/Digital mode:** produces CALL, PUT, or NO TRADE suggestions for a manually selected expiry/timeframe. It does not place trades.
- **Forex mode:** produces BUY, SELL, or NO TRADE suggestions for a manually selected candle timeframe.

This project is for research and demo use only. It does not connect to IQ Option or any broker, does not read passwords, and does not click trade buttons.

## Requirements

- Windows, macOS, or Linux
- Python 3.10+
- Internet connection for Yahoo Finance market data

## Install

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

If PowerShell blocks activation, run the app with `.venv\Scripts\python.exe app.py` after installing dependencies.

## Use

1. Select **Binary/Digital** or **Forex**.
2. Enter a Yahoo Finance symbol, such as `EURUSD=X` or `BTC-USD`.
3. Select a timeframe manually.
4. Click **Refresh signal**.
5. Treat the result as a research signal and verify the price/time on your broker platform.
6. Record any manual demo trade outside the app until the journal is added.

Yahoo Finance data can be delayed, incomplete, or different from a broker's quote. This is especially important for short binary/digital expiries. Do not use this as a live-money trading system.

## Limitations

- This first version uses transparent indicator rules rather than a trained machine-learning model.
- Binary/digital results depend on the platform payout, expiry timing, and exact quote feed; the app does not know those values.
- No automatic execution, browser automation, screen reading, martingale, or investment advice is included.
