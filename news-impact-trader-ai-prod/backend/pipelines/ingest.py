import feedparser, requests, time, logging
from datetime import datetime
from typing import List, Dict
from functools import lru_cache

logger = logging.getLogger(__name__)

GLOBAL_FEEDS = [
    ('Reuters', 'https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best'),
    # Add more global feeds
]

INDIA_FEEDS = [
    ('Economic Times', 'https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms'),
    ('Moneycontrol', 'https://www.moneycontrol.com/rss/MCtopnews.xml'),
    ('Mint', 'https://www.livemint.com/rss/markets'),
    ('Business Standard', 'https://www.business-standard.com/rss/markets-106.rss'),
]

def _parse_feed(url):
    try:
        feed = feedparser.parse(url)
        items = []
        for e in feed.entries:
            items.append({
                'title': getattr(e,'title',''),
                'url': getattr(e,'link',''),
                'source': getattr(e,'source',''),
                'published_at': getattr(e,'published', getattr(e,'updated', datetime.utcnow().isoformat())),
                'raw': dict(e)
            })
        return items
    except Exception as e:
        logger.exception('Failed parse feed %s', url)
        return []

@lru_cache(maxsize=32)
def fetch_rss_global(limit=100):
    out = []
    for src,url in GLOBAL_FEEDS:
        out += _parse_feed(url)[:limit]
    return out

@lru_cache(maxsize=32)
def fetch_rss_india(limit=200):
    out = []
    for src,url in INDIA_FEEDS:
        out += _parse_feed(url)[:limit]
    return out
