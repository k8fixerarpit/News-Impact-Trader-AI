
from typing import List, Dict
from datetime import datetime
import feedparser

INDIA_RSS = [
    ("Economic Times", "https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms"),
    ("Moneycontrol Markets", "https://www.moneycontrol.com/rss/MCtopnews.xml"),
    ("Mint Markets", "https://www.livemint.com/rss/markets"),
    ("Business Standard Markets", "https://www.business-standard.com/rss/markets-106.rss"),
]

def fetch_rss() -> List[Dict]:
    out = []
    for source, url in INDIA_RSS:
        try:
            feed = feedparser.parse(url)
            for e in feed.entries[:30]:
                out.append({
                    "title": getattr(e, "title", ""),
                    "source": source,
                    "url": getattr(e, "link", ""),
                    "time": getattr(e, "published", getattr(e, "updated", datetime.utcnow().isoformat()))
                })
        except Exception:
            continue
    return out
