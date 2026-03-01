from mcp.server.fastmcp import FastMCP
from GoogleNews import GoogleNews
import yfinance as yf
from toon import encode

DISCLAIMER = """
            DISCLAIMER:
                - All stock data, news, and analysis provided by this server are system-generated and sourced from third-party services (Yahoo Finance, Google News).
                - This information is for informational purposes only.
                - It does not constitute financial or investment advice.
                - Invest at your own risk. We do not claim any responsibility for decisions made based on this data.
"""

mcp = FastMCP("Stock Analyzer", instructions=DISCLAIMER)

@mcp.tool()
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
            - datetime (datetime | None): Parsed publication datetime, if available.
            - description (str): Short snippet or summary.
            - link (str): URL to the full article.
    """
    googlenews = GoogleNews(lang='en', region=region, period=period, encode='utf-8')
    googlenews.get_news(ticker)
    results = googlenews.results()
    articles = []
    for result in results:
        article = {
            "title": result.get("title"),
            "date": result.get("date"),
            "datetime": result.get("datetime"),
            "description": result.get("desc"),
            "link": result.get("link")
        }
        articles.append(article)
        
    googlenews.clear()
    
    return encode(articles)
    

@mcp.tool()
def get_stock_price(symbol: str, period: str, interval: str):
    """
    Fetch historical OHLCV price data for a stock using Yahoo Finance.

    Args:
        symbol: Yahoo Finance ticker symbol.
            - US stocks: plain ticker, e.g. 'AAPL', 'MSFT', 'GOOGL'.
            - Indian stocks: append '.NS' (NSE) or '.BO' (BSE), e.g. 'RELIANCE.NS', 'TCS.BO'.
            - Other exchanges: use the Yahoo Finance suffix, e.g. '7203.T' (Toyota/Tokyo),
              'RY.TO' (Royal Bank of Canada/Toronto).
        period: Total span of data to retrieve.
            - Valid values: '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'.
        interval: Granularity of each data point.
            - Valid values: '1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'.
            - Note: Intraday intervals (< '1d') are only available for the trailing 60 days.

    Returns:
        list[dict]: OHLCV records, each containing:
            - Date (datetime): Timestamp of the record.
            - Open, High, Low, Close (float): Price data.
            - Volume (int): Trading volume.
            - Dividends (float): Dividends paid.
            - Stock Splits (float): Stock splits occurred.
    """
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period, interval=interval)
    hist = hist.reset_index()
    records = hist.to_dict(orient="records")

    return encode(records)

@mcp.tool()
def get_company_info(symbol: str) -> dict:
    """
    Fetch detailed company information and fundamentals for a stock using Yahoo Finance.

    Args:
        symbol: Yahoo Finance ticker symbol.
            - US stocks: plain ticker, e.g. 'AAPL', 'MSFT', 'GOOGL'.
            - Indian stocks: append '.NS' (NSE) or '.BO' (BSE), e.g. 'RELIANCE.NS', 'TCS.BO'.

    Returns:
        dict: Company profile and fundamentals, including fields such as:
            - shortName (str): Company display name.
            - sector, industry (str): Business classification.
            - country, city (str): Headquarters location.
            - marketCap (int): Market capitalisation in base currency.
            - currentPrice, fiftyTwoWeekHigh, fiftyTwoWeekLow (float): Price data.
            - trailingPE, forwardPE (float): Price-to-earnings ratios.
            - dividendYield (float): Annual dividend yield.
            - returnOnEquity, returnOnAssets (float): Profitability ratios.
            - totalRevenue, netIncomeToCommon (int): Income statement highlights.
            - debtToEquity (float): Leverage ratio.
            - longBusinessSummary (str): Full business description.
    """
    try:
        ticker = yf.Ticker(symbol)
        return encode(ticker.info)
    except Exception as e:
        return {"error": str(e), "symbol": symbol}


if __name__ == "__main__":
    mcp.run()
    
