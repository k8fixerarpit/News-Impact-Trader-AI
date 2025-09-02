import logging, time, json
logger = logging.getLogger(__name__)

def safe_parse_time(s):
    try:
        from dateutil import parser
        return parser.parse(s)
    except Exception:
        return None
