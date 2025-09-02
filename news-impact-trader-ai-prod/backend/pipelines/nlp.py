import os, logging, time
from typing import List, Dict
from pathlib import Path
import numpy as np
import pandas as pd
from functools import lru_cache

from sentence_transformers import SentenceTransformer
import hdbscan
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

logger = logging.getLogger(__name__)
MODEL_DIR = os.getenv('MODEL_CACHE_DIR','./models_cache')

# Load FinBERT once
@lru_cache(maxsize=1)
def load_finbert():
    tokenizer = AutoTokenizer.from_pretrained('ProsusAI/finbert')
    model = AutoModelForSequenceClassification.from_pretrained('ProsusAI/finbert')
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model.to(device)
    return tokenizer, model, device

# Load embedding model
@lru_cache(maxsize=1)
def load_embedder():
    return SentenceTransformer('all-MiniLM-L6-v2', cache_folder=MODEL_DIR)

def get_sentiment(text: str) -> Dict:
    tokenizer, model, device = load_finbert()
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1).cpu().numpy()[0]
    labels = ['negative','neutral','positive']
    return dict(zip(labels, [float(p) for p in probs]))

def cluster_headlines(news: List[Dict], min_cluster_size:int=2) -> List[Dict]:
    # news: list of dicts with 'title'
    titles = [n.get('title','') for n in news]
    embedder = load_embedder()
    embeddings = embedder.encode(titles, convert_to_numpy=True, show_progress_bar=False)
    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, metric='euclidean', cluster_selection_method='eom')
    labels = clusterer.fit_predict(embeddings)
    clusters = {}
    for i,label in enumerate(labels):
        clusters.setdefault(int(label), []).append(news[i])
    out = []
    for label, items in clusters.items():
        out.append({'cluster_id': int(label), 'headlines': items})
    return out

# Simple entity->ticker link using KB
KB_PATH = Path(__file__).resolve().parents[1] / 'data' / 'tickers_nifty50.csv'
import pandas as pd
if KB_PATH.exists():
    KB = pd.read_csv(KB_PATH)
else:
    KB = pd.DataFrame(columns=['company','nse','bse','sector'])

from rapidfuzz import process, fuzz

def _fuzzy_map_company_to_ticker(text: str):
    if KB.empty:
        return None
    choices = KB['company'].astype(str).tolist()
    match = process.extractOne(text, choices, scorer=fuzz.token_set_ratio)
    if match and match[1] >= 75:
        comp = match[0]
        sym = KB[KB['company']==comp]['nse'].iloc[0]
        return str(sym)
    return None

def link_entities_to_tickers(clusters: List[Dict]) -> List[Dict]:
    rows = []
    for c in clusters:
        for h in c.get('headlines', []):
            title = h.get('title','')
            sentiment = get_sentiment(title)
            pos = sentiment.get('positive',0)
            neg = sentiment.get('negative',0)
            score = pos - neg
            ticker = _fuzzy_map_company_to_ticker(title)
            rows.append({
                'cluster_id': c.get('cluster_id'),
                'title': title,
                'source': h.get('source',''),
                'url': h.get('url',''),
                'ticker': ticker,
                'sentiment': float(score),
                'sentiment_probs': sentiment
            })
    return rows
