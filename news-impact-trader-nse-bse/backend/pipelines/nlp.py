
from typing import List, Dict
import re
from pathlib import Path
import pandas as pd
try:
    from rapidfuzz import process, fuzz
    HAVE_FUZZ = True
except Exception:
    HAVE_FUZZ = False

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
KB_FILE = DATA_DIR / "tickers_nifty50.csv"

def load_kb():
    if KB_FILE.exists():
        df = pd.read_csv(KB_FILE)
        return df
    return pd.DataFrame(columns=["company","nse","bse","sector"])

KB = load_kb()

def simple_sentiment(headline: str) -> float:
    h = headline.lower()
    pos = any(w in h for w in ["surge", "soar", "rally", "record", "beats", "profit", "expands", "unveils", "launches"])
    neg = any(w in h for w in ["plunge", "fall", "drop", "ban", "probe", "raid", "recall", "loss", "fraud", "resign"])
    return 1.0 if pos and not neg else (-1.0 if neg and not pos else 0.0)

def cluster_headlines(news: List[Dict]) -> List[Dict]:
    # naive: each item is its own cluster (placeholder)
    clusters = []
    for i, n in enumerate(news):
        clusters.append({"cluster_id": i, "headlines": [n]})
    return clusters

def _fuzzy_map_company_to_ticker(text: str) -> str:
    if KB.empty:
        return None
    name = text.upper()
    # Exact quick path
    for _, row in KB.iterrows():
        if row["company"].upper() in name:
            return str(row["nse"])
    # Fuzzy
    if HAVE_FUZZ:
        choices = KB["company"].tolist()
        match = process.extractOne(text, choices, scorer=fuzz.token_set_ratio)
        if match and match[1] >= 85:
            comp = match[0]
            sym = KB[KB["company"]==comp]["nse"].iloc[0]
            return str(sym)
    return None

def link_entities_to_tickers(clusters: List[Dict]) -> List[Dict]:
    rows = []
    for c in clusters:
        for h in c["headlines"]:
            title = h.get("title","")
            ticker = _fuzzy_map_company_to_ticker(title) or None
            rows.append({
                "cluster_id": c["cluster_id"],
                "title": title,
                "source": h.get("source",""),
                "url": h.get("url",""),
                "ticker": ticker,
                "sentiment": simple_sentiment(title)
            })
    return rows
