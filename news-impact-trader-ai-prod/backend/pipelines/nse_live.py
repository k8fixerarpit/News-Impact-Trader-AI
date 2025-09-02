import yfinance as yf
import pandas as pd

def fetch_ohlcv(ticker, period='3mo', interval='1d'):
    # ticker e.g., RELIANCE.NS
    df = yf.download(ticker, period=period, interval=interval, progress=False)
    if df is None or df.empty:
        return pd.DataFrame()
    df = df.rename(columns=str.title)
    return df
