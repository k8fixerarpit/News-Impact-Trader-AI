from typing import List, Dict
from datetime import datetime, timedelta

def sample_news() -> List[Dict]:
    # Minimal synthetic sample (replace with real RSS/scrapers)
    now = datetime.utcnow()
    items = [
        {"title": "Apple unveils new AI features for iPhone", "source":"Reuters", "url":"https://example.com/aapl-ai", "time": now.isoformat()},
        {"title": "Regulators probe Tesla over autopilot incidents", "source":"CNBC", "url":"https://example.com/tsla-probe", "time": (now - timedelta(minutes=5)).isoformat()},
        {"title": "NVIDIA announces next-gen GPU for data centers", "source":"Bloomberg", "url":"https://example.com/nvda-gpu", "time": (now - timedelta(minutes=7)).isoformat()},
        {"title": "Oil prices surge on supply cut worries", "source":"Reuters", "url":"https://example.com/oil-surge", "time": (now - timedelta(minutes=10)).isoformat()},
    ]
    return items
