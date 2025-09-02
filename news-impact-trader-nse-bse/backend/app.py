from fastapi import FastAPI, Query
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
from pipelines import ingest, ingest_india, nlp, impact as impact_mod, ta_signals
import yfinance as yf
import pandas as pd

app = FastAPI(title="News Impact Trader AI (OSS)")

class Alert(BaseModel):
    ticker: str
    impact: float
    sentiment: float
    bias: str
    reason: str
    time: datetime
    indicators: Dict[str, Any]
    headlines: List[Dict[str, Any]]

@app.get("/health")
def health():
    return {"status":"ok","time": datetime.utcnow().isoformat()}

@app.get("/ingest")
def ingest_news(sample: bool = True, india: bool = True):
    items = ingest_india.fetch_rss() if india else (ingest.sample_news() if sample else [])
    return {"count": len(items), "items": items}

@app.get("/clusters")
def clusters():
    news = ingest_india.fetch_rss()
    clusters = nlp.cluster_headlines(news)
    return {"count": len(clusters), "clusters": clusters}

@app.get("/impacts")
def impacts():
    news = ingest_india.fetch_rss()
    clusters = nlp.cluster_headlines(news)
    links = nlp.link_entities_to_tickers(clusters)
    impacts = impact_mod.score_impacts(links)
    return {"count": len(impacts), "impacts": impacts}

@app.get("/alerts", response_model=List[Alert])
def alerts(tickers: Optional[str] = Query(None, description="CSV tickers (e.g., AAPL,MSFT,TSLA)")):
    # pipeline: sample news -> cluster -> link-> score -> TA confirm -> alerts
    news = ingest_india.fetch_rss()
    clusters = nlp.cluster_headlines(news)
    links = nlp.link_entities_to_tickers(clusters)

    # If user passes tickers, filter; else use linked tickers
    passed = set([t.strip().upper() for t in (tickers.split(",") if tickers else []) if t.strip()])
    tickers_set = passed or {r["ticker"] for r in links if r.get("ticker")}

    alerts_out = []
    for t in sorted(tickers_set):
        try:
            df = yf.download(t, period="3mo", interval="1d", progress=False)
            if df.empty: 
                continue
            df = df.rename(columns=str.title)
            sig = ta_signals.signals_from_ohlcv(df)
            last = sig.iloc[-1]
            rel_links = [r for r in links if r.get("ticker")==t]
            sent = 0.0
            if rel_links:
                sent = sum([x.get("sentiment",0) for x in rel_links]) / max(1,len(rel_links))
            imp = impact_mod.aggregate_ticker_impact(rel_links)

            alert = impact_mod.make_alert(last, imp, sent)
            if alert:
                alerts_out.append(Alert(
                    ticker=t,
                    impact=imp,
                    sentiment=sent,
                    bias=alert["bias"],
                    reason=alert["reason"],
                    time=datetime.utcnow(),
                    indicators={
                        "Close": float(last["Close"]),
                        "EMA20": float(last["EMA20"]),
                        "EMA50": float(last["EMA50"]),
                        "RSI14": float(last["RSI14"]),
                        "MACD": float(last["MACD"]),
                        "MACDsig": float(last["MACDsig"]),
                        "BullishEngulfing": int(last["BullishEngulfing"]),
                    },
                    headlines=[{"title": x["title"], "source": x["source"], "url": x["url"], "sentiment": x["sentiment"]} for x in rel_links]
                ))
        except Exception as e:
            # swallow errors per ticker to avoid breaking whole list
            continue
    return alerts_out
