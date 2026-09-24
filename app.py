"""Signal-only desktop application for binary/digital and forex research."""

import tkinter as tk
from tkinter import messagebox, ttk

from core.data import fetch_candles
from core.strategy import analyze_binary, analyze_forex


TIMEFRAMES = {
    "1 minute": ("1m", "1d"),
    "5 minutes": ("5m", "5d"),
    "15 minutes": ("15m", "30d"),
    "30 minutes": ("30m", "60d"),
    "1 hour": ("1h", "730d"),
    "1 day": ("1d", "max"),
}


class TradingAssistant(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Demo Trading Signal Assistant")
        self.geometry("760x560")
        self.minsize(680, 500)
        self._build_ui()

    def _build_ui(self):
        heading = ttk.Frame(self, padding=16)
        heading.pack(fill="x")
        ttk.Label(heading, text="Demo Trading Signal Assistant", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(heading, text="Signal-only research tool — automatic trading is disabled", foreground="#a33").pack(anchor="w")

        controls = ttk.LabelFrame(self, text="Analysis settings", padding=12)
        controls.pack(fill="x", padx=16, pady=(0, 12))

        ttk.Label(controls, text="System").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.system = ttk.Combobox(controls, values=["Binary/Digital", "Forex"], state="readonly", width=20)
        self.system.current(0)
        self.system.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(controls, text="Symbol").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.symbol = ttk.Entry(controls, width=18)
        self.symbol.insert(0, "EURUSD=X")
        self.symbol.grid(row=0, column=3, sticky="w", padx=5, pady=5)

        ttk.Label(controls, text="Timeframe").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.timeframe = ttk.Combobox(controls, values=list(TIMEFRAMES), state="readonly", width=20)
        self.timeframe.current(1)
        self.timeframe.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Button(controls, text="Refresh signal", command=self.refresh).grid(row=1, column=3, sticky="e", padx=5, pady=5)

        self.status = ttk.Label(self, text="Ready. No broker account is connected.", padding=(16, 0))
        self.status.pack(fill="x")

        result = ttk.LabelFrame(self, text="Latest analysis", padding=16)
        result.pack(fill="both", expand=True, padx=16, pady=12)
        self.signal = tk.StringVar(value="NO TRADE")
        ttk.Label(result, textvariable=self.signal, font=("Segoe UI", 30, "bold")).pack(pady=(10, 18))
        self.details = tk.Text(result, height=14, wrap="word", state="disabled", font=("Consolas", 10))
        self.details.pack(fill="both", expand=True)

        warning = ttk.Label(self, text="Verify every signal manually. Never use martingale or real money based on this prototype.", foreground="#a33", padding=16)
        warning.pack(fill="x")

    def refresh(self):
        symbol = self.symbol.get().strip().upper()
        label = self.timeframe.get()
        if not symbol or label not in TIMEFRAMES:
            messagebox.showerror("Missing settings", "Enter a symbol and choose a timeframe.")
            return
        self.status.config(text=f"Downloading {symbol} candles…")
        self.update_idletasks()
        try:
            interval, period = TIMEFRAMES[label]
            candles = fetch_candles(symbol, interval, period)
            if self.system.get() == "Binary/Digital":
                analysis = analyze_binary(candles, label)
            else:
                analysis = analyze_forex(candles, label)
            self.signal.set(analysis["signal"])
            self._write_details(analysis, symbol, label)
            self.status.config(text=f"Updated {analysis['timestamp']} — data source: Yahoo Finance; broker: not connected")
        except Exception as exc:  # UI boundary: show a readable error
            self.status.config(text="Could not update data")
            messagebox.showerror("Data error", str(exc))

    def _write_details(self, analysis, symbol, timeframe):
        lines = [
            f"System: {self.system.get()}",
            f"Symbol: {symbol}",
            f"Timeframe: {timeframe}",
            f"Signal strength: {analysis['strength']}% (not a guaranteed probability)",
            f"Last close: {analysis['close']}",
            f"Trend: {analysis['trend']}",
            f"RSI: {analysis['rsi']}",
            f"Fast/slow moving averages: {analysis['fast_ma']} / {analysis['slow_ma']}",
            f"Volatility: {analysis['volatility']}",
            "",
            "Reasoning:",
            *[f"- {item}" for item in analysis["reasons"]],
            "",
            "Manual action required: verify the live quote, payout/expiry, and market conditions before any demo trade.",
        ]
        self.details.config(state="normal")
        self.details.delete("1.0", "end")
        self.details.insert("1.0", "\n".join(lines))
        self.details.config(state="disabled")


if __name__ == "__main__":
    TradingAssistant().mainloop()
