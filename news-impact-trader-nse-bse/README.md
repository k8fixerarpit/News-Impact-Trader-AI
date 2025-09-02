# News Impact Trader AI (Open-Source)

An open-source MVP that connects **trending news → impacted tickers → candle/TA analysis → alerts**.

## Features (MVP)
- Ingest RSS/Twitter/Reddit (stubs provided)
- NLP: dedup + clustering + FinBERT sentiment (plug-in)
- Map entities → tickers (spaCy + rules + KB)
- TA layer: RSI, MACD, EMA, Bollinger, ATR + candlestick patterns
- Impact score + alert rules
- FastAPI backend (endpoints: /ingest, /clusters, /impacts, /alerts)
- Simple frontend placeholder

## Quick Start
```bash
# 1) Python env
python -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt

# 2) Run API
uvicorn backend.app:app --reload --port 8000

# 3) Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/alerts
```

## Structure
```
backend/
  app.py                # FastAPI app + endpoints
  requirements.txt      # OSS deps
  pipelines/
    nlp.py              # FinBERT sentiment, clustering stubs
    impact.py           # impact scoring
    ta_signals.py       # indicators + candlestick detection
    ingest.py           # RSS/Reddit/Twitter stubs
  data/
    tickers.csv         # sample KB (issuer → ticker → sector)
frontend/
  index.html            # simple placeholder (fetches alerts)
infra/
  docker-compose.yml
  Dockerfile.api
notebooks/
  backtest_template.py  # outline for event study/backtest
```

## Notes
- FinBERT + sentence-transformers models download on first run (internet required).
- Replace stubs in `ingest.py` with your chosen sources (RSS, GDELT, snscrape, praw).
- This is **not financial advice**; for research/education.


## India (NSE/BSE) Setup
- Ticker KB: `backend/data/tickers_nifty50.csv` (edit/expand as needed)
- News: `pipelines/ingest_india.py` fetches Economic Times, Moneycontrol, Mint, Business Standard via RSS.
- NLP: fuzzy company→ticker mapping via `rapidfuzz` in `pipelines/nlp.py`
- Try alerts: `curl http://localhost:8000/alerts?tickers=RELIANCE.NS,HDFCBANK.NS,INFY.NS`
