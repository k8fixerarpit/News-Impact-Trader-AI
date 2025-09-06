from fastapi import FastAPI, Query
import yfinance as yf
import pandas as pd
import pandas_ta as ta

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/alerts")
def get_alerts(tickers: str = Query(..., description="Comma-separated tickers")):
    tickers_list = tickers.split(",")

    results = []

    for ticker in tickers_list:
        try:
            # Fetch last 14 days of daily data
            df = yf.download(ticker, period="14d", interval="1d", progress=False)

            if df.empty:
                results.append({"ticker": ticker, "error": "No data found"})
                continue

            # Calculate RSI (Relative Strength Index)
            df["RSI"] = ta.rsi(df["Close"], length=14)

            latest_price = df["Close"].iloc[-1]
            latest_rsi = df["RSI"].iloc[-1]

            sentiment = "neutral"
            impact = 0.5

            if latest_rsi < 30:
                sentiment = "positive"   # Oversold → buy signal
                impact = 0.8
            elif latest_rsi > 70:
                sentiment = "negative"   # Overbought → sell signal
                impact = 0.9

            results.append({
                "ticker": ticker,
                "price": round(latest_price, 2),
                "RSI": round(latest_rsi, 2),
                "sentiment": sentiment,
                "impact": impact
            })

        except Exception as e:
            results.append({"ticker": ticker, "error": str(e)})

    return {"alerts": results}
