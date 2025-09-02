from typing import List, Dict

def impact_score(sentiment: float, z_velocity: float = 1.0, source_weight: float = 0.8, novelty: float = 0.6) -> float:
    # Simple bounded score
    w = dict(sent=0.35, vel=0.35, src=0.15, nov=0.15)
    s = (w['sent']*abs(sentiment) + w['vel']*max(z_velocity,0) + w['src']*source_weight + w['nov']*novelty)
    return round(100*max(0,min(1,s)), 1)

def score_impacts(links: List[Dict]) -> List[Dict]:
    out = []
    for r in links:
        out.append({**r, "impact": impact_score(r.get("sentiment",0))})
    return out

def aggregate_ticker_impact(rows: List[Dict]) -> float:
    if not rows: return 0.0
    # average of headline-level impact scores
    scores = [impact_score(r.get("sentiment",0)) for r in rows]
    return round(sum(scores)/len(scores), 1)

def make_alert(row, impact: float, sent: float):
    tech_ok = ((row['Close'] > row['EMA20'] and row['MACD'] > row['MACDsig']) or
               (row['RSI14'] < 30 and int(row['BullishEngulfing']) == 1))
    if impact > 65 and tech_ok:
        bias = "Long" if sent >= 0 else "Watch for fade/Short"
        return dict(bias=bias, reason=f"Impact {impact}, Sent {sent:.2f}, EMA/MACD/RSI confirm")
    return None
