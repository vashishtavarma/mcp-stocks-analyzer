from mcp.server.fastmcp import FastMCP
from GoogleNews import GoogleNews
import yfinance as yf

mcp = FastMCP("Stock Analyzer")

@mcp.tool()
def get_news_from_google(ticker: str, region: str = 'IN', period: str = '7d'):
    """ 
    Fetch news articles related to the given ticker from Google News.

    Args:
        ticker (str): Stock ticker symbol to search news for.
        region (str, optional): Region code for Google News (e.g., 'US', 'IN'). Defaults to 'IN'.
        period (str, optional): Time period for news articles (e.g., '7d' for last 7 days). Defaults to '7d'.

    Returns:
        list[dict]: List of news articles with the following keys:
            - title (str): Article title.
            - date (str): Publication date.
            - datetime (datetime, optional): Publication datetime object.
            - description (str): Article description/snippet.
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
    
    return articles
    

@mcp.tool()
def get_stock_price(symbol: str, period: str = '7d', interval: str = '1d'):
    """
    Fetch stock price data for the given ticker using yfinance.

    Note: This tool specifically returns the *last 7 records* of the fetched data,
    regardless of the requested period, to keep the context concise.

    Args:
        symbol (str): Stock ticker symbol.
            - For Indian stocks: append ".NS" for NSE or ".BO" for BSE. 
              Example: "RELIANCE.NS", "TCS.BO"
            - For US stocks: use the ticker as is. 
              Example: "AAPL", "GOOGL", "MSFT"
            - For other foreign exchanges: use the appropriate suffix 
              as per Yahoo Finance conventions. 
              Example: "7203.T" (Toyota on Tokyo Exchange), "RY.TO" (Royal Bank of Canada on Toronto Exchange)
        period (str, optional): Data retrieval period. Defaults to '7d' (last 7 days).
            Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        interval (str, optional): Data interval. Defaults to '1d' (daily data).
            Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo

    Returns:
        list[dict]: List of stock price records. Each record is a dictionary containing
        OHLCV (Open, High, Low, Close, Volume) data and the date/time.
    """
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period, interval=interval).tail(7)
    hist = hist.reset_index()
    records = hist.to_dict(orient="records")

    return records


@mcp.resource("welcome://")
def get_welcome() -> str:
    """Get a general welcome message for the MCP Stocks Analyzer"""
    
    welcome_msg = """
        Welcome to MCP Stocks Analyzer

        A professional financial analysis tool providing:
        • Real-time news from Google News
        • Stock data from Yahoo Finance
        • Market analysis capabilities

        Available Tools:
        • get_news_from_google(ticker, region='IN', period='7d') - Retrieve latest news for any stock
        • get_stock_price(symbol, period='7d', interval='1d') - Fetch price history (returns last 7 records)

        Stock Symbol Examples:
        • US Stocks: AAPL, GOOGL, MSFT, TSLA
        • Indian Stocks: RELIANCE.NS, TCS.BO, INFY.NS
        • International: 7203.T (Toyota), RY.TO (Royal Bank)

        Ready to begin your financial analysis.
    """
    
    return welcome_msg.strip()



if __name__ == "__main__":
    mcp.run()
