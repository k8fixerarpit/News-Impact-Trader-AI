"""
Backtest Template: News Impact + TA Confirmation

1) Load historical headlines (CSV with columns: time, title, source, ticker, sentiment)
2) Load OHLCV via yfinance
3) Align events to daily bars (or intraday if available)
4) Compute indicators and evaluate strategy rules
"""

import pandas as pd
import yfinance as yf
from backend.pipelines.ta_signals import signals_from_ohlcv

def event_study(ticker: str, events_csv: str, lookahead_days: int = 3):
    df = yf.download(ticker, period="2y", interval="1d", progress=False).rename(columns=str.title)
    sig = signals_from_ohlcv(df)
    ev = pd.read_csv(events_csv, parse_dates=["time"])
    ev = ev[ev["ticker"]==ticker.upper()].copy()
    ev["date"] = ev["time"].dt.date
    sig["date"] = sig.index.date
    merged = ev.merge(sig.reset_index().rename(columns={"index":"Date"}), on="date", how="left")
    # Example metric: next N-day return
    sig["ret_fwd"] = sig["Close"].pct_change(lookahead_days).shift(-lookahead_days)
    merged = merged.merge(sig[["ret_fwd","date"]], on="date", how="left")
    print(merged[["time","title","sentiment","ret_fwd"]].head())
    return merged

if __name__ == "__main__":
    # Example usage (prepare events.csv yourself)
    pass
