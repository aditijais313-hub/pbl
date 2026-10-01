import requests
import yfinance as yf

NEWSAPI_URL = "https://newsapi.org/v2/everything"


def _from_newsapi(ticker: str, api_key: str, limit: int):
    params = {
        "q": ticker,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": limit,
        "apiKey": api_key,
    }
    resp = requests.get(NEWSAPI_URL, params=params, timeout=15)
    data = resp.json()
    if data.get("status") != "ok":
        raise RuntimeError(data.get("message", "NewsAPI request failed"))
    return [
        {
            "title": a.get("title"),
            "description": a.get("description"),
            "url": a.get("url"),
            "publishedAt": a.get("publishedAt"),
        }
        for a in data.get("articles", [])[:limit]
        if a.get("title") and a["title"] != "[Removed]"
    ]


def _from_yfinance(ticker: str, limit: int):
    """Fallback that needs no API key. Handles old and new yfinance news formats."""
    articles = []
    for item in (yf.Ticker(ticker).news or [])[:limit]:
        content = item.get("content") or item
        title = content.get("title")
        if not title:
            continue
        url = (
            (content.get("canonicalUrl") or {}).get("url")
            or (content.get("clickThroughUrl") or {}).get("url")
            or content.get("link")
            or ""
        )
        articles.append(
            {
                "title": title,
                "description": content.get("summary", ""),
                "url": url,
                "publishedAt": content.get("pubDate") or content.get("providerPublishTime"),
            }
        )
    return articles


def fetch_financial_news(ticker: str, api_key: str = "", limit: int = 15):
    """Returns (articles, source_name). Uses NewsAPI if a key is given, else yfinance."""
    if api_key:
        try:
            return _from_newsapi(ticker, api_key, limit), "NewsAPI"
        except Exception as e:
            fallback = _from_yfinance(ticker, limit)
            if fallback:
                return fallback, f"yfinance (NewsAPI failed: {e})"
            raise
    return _from_yfinance(ticker, limit), "yfinance"
