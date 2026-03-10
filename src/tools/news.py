from gnews import GNews
from toon import encode
from ..resources.errors import not_found, fetch_failed


def get_news_from_google(ticker: str, region: str = 'IN', period: str = '7d'):
    """
    Fetch news articles for a stock ticker from Google News.

    Args:
        ticker: Stock ticker symbol or company name to search for (e.g., 'AAPL', 'Reliance').
        region: ISO 3166-1 alpha-2 country code for the Google News edition.
            - Common values: 'US' (United States), 'IN' (India), 'GB' (United Kingdom).
            - Defaults to 'IN'.
        period: Lookback window for articles. Format is a number followed by 'd' (days) or 'm' (months), e.g. '1d', '7d', '1m'. Defaults to '7d'.

    Returns:
        list[dict]: News articles, each containing:
            - title (str): Headline of the article.
            - date (str): Human-readable publication date.
            - datetime (None): Reserved for parsed datetime.
            - description (str): Short snippet or summary.
            - link (str): URL to the full article.
            - publisher (str): Source/publisher name.
    """
    try:
        google_news = GNews(language="en", country=region, period=period)
        results = google_news.get_news(ticker) or []
        if not results:
            return {
                "error": "no_results",
                "ticker": ticker,
                "message": f"No news found for '{ticker}' in region='{region}' over the past {period}.",
                "suggestion": "Try a broader period (e.g. '30d'), a different region, or the full company name.",
            }
        articles = [
            {
                "title": r.get("title"),
                "date": r.get("published date"),
                "datetime": None,
                "description": r.get("description"),
                "link": r.get("url"),
                "publisher": r.get("publisher"),
            }
            for r in results
        ]
        return encode(articles)
    except Exception as e:
        return {
            "error": "fetch_failed",
            "ticker": ticker,
            "message": str(e),
            "suggestion": "Check that the ticker or company name is spelled correctly.",
        }
