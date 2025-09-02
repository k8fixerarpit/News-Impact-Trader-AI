import pandas as pd
import numpy as np

def ema(series, span):
    return series.ewm(span=span, adjust=False).mean()

def rsi(close, period=14):
    delta = close.diff()
    gain = np.where(delta>0, delta, 0.0)
    loss = np.where(delta<0, -delta, 0.0)
    roll_up = pd.Series(gain, index=close.index).rolling(period).mean()
    roll_down = pd.Series(loss, index=close.index).rolling(period).mean()
    rs = roll_up / (roll_down + 1e-9)
    return 100 - (100 / (1 + rs))

def macd(close, fast=12, slow=26, signal=9):
    ema_fast, ema_slow = ema(close, fast), ema(close, slow)
    macd_line = ema_fast - ema_slow
    signal_line = ema(macd_line, signal)
    hist = macd_line - signal_line
    return macd_line, signal_line, hist

def bollinger(close, window=20, num_std=2):
    ma = close.rolling(window).mean()
    std = close.rolling(window).std()
    upper = ma + num_std*std
    lower = ma - num_std*std
    return upper, ma, lower

def atr(df, period=14):
    hl = (df['High'] - df['Low']).abs()
    hc = (df['High'] - df['Close'].shift()).abs()
    lc = (df['Low'] - df['Close'].shift()).abs()
    tr = pd.concat([hl, hc, lc], axis=1).max(axis=1)
    return tr.rolling(period).mean()

def bullish_engulfing(df):
    prev_red = (df['Close'].shift(1) < df['Open'].shift(1))
    curr_green = (df['Close'] > df['Open'])
    body_engulf = (df['Open'] < df['Close'].shift(1)) & (df['Close'] > df['Open'].shift(1))
    return (prev_red & curr_green & body_engulf).astype(int)

def signals_from_ohlcv(df):
    out = df.copy()
    out['EMA20'] = ema(out['Close'], 20)
    out['EMA50'] = ema(out['Close'], 50)
    out['RSI14'] = rsi(out['Close'], 14)
    macd_line, signal_line, hist = macd(out['Close'])
    out['MACD'], out['MACDsig'], out['MACDhist'] = macd_line, signal_line, hist
    out['BB_up'], out['BB_mid'], out['BB_low'] = bollinger(out['Close'])
    out['ATR14'] = atr(out)
    out['BullishEngulfing'] = bullish_engulfing(out)
    return out
