from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.pipelines import ingest, nlp, impact, ta_signals, nse_live
from backend.db import SessionLocal, engine, Base
from backend import models, schemas
import logging
import os

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="News Impact Trader AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

logger = logging.getLogger('uvicorn.error')

@app.get('/health')
async def health():
    return {'status':'ok'}

@app.get('/alerts')
async def alerts(tickers: str = None, india: bool = True):
    # Simple synchronous pipeline for demonstration. For production use async workers and caching.
    try:
        if india:
            news = ingest.fetch_rss_india()
        else:
            news = ingest.fetch_rss_global()
        clusters = nlp.cluster_headlines(news)
        links = nlp.link_entities_to_tickers(clusters)
        impacts = impact.score_impacts(links)
        tickers_set = set([r['ticker'] for r in impacts if r.get('ticker')])
        if tickers:
            tickers_set = set([t.strip().upper() for t in tickers.split(',') if t.strip()])
        results = []
        for t in tickers_set:
            try:
                df = nse_live.fetch_ohlcv(t, period='3mo', interval='1d')
                if df is None or df.empty:
                    continue
                sig = ta_signals.signals_from_ohlcv(df)
                last = sig.iloc[-1]
                rel = [r for r in impacts if r.get('ticker')==t]
                sent = sum([r.get('sentiment',0) for r in rel])/max(1,len(rel)) if rel else 0.0
                imp_score = impact.aggregate_ticker_impact(rel)
                alert = impact.make_alert(last, imp_score, sent)
                if alert:
                    results.append({
                        'ticker': t,
                        'impact': imp_score,
                        'sentiment': sent,
                        'bias': alert['bias'],
                        'reason': alert['reason'],
                    })
            except Exception as e:
                logger.exception('Ticker processing failed for %s', t)
                continue
        return results
    except Exception as e:
        logger.exception('Pipeline failed')
        raise HTTPException(status_code=500, detail='Pipeline failure')
