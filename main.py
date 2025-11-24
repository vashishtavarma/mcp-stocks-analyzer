from mcp.server.fastmcp import FastMCP
from GoogleNews import GoogleNews
import yfinance as yf

mcp = FastMCP("Stock Analyzer")

@mcp.tool()
def get_news_from_google(ticker: str, region: str, period: str):
    """ 
        Fetch news articles related to the given ticker from Google News.
        Args:
            ticker (str): Stock ticker symbol to search news for.   
            region (str): Region code for Google News (e.g., 'US', 'IN').
            period (str): Time period for news articles (e.g., '7d' for last 7 days).
        Defaults:
            region: 'IN'
            period: '7d'
        Returns:
            list[dict]: List of news articles with title, date, description, and link.
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
def get_stock_price(symbol: str, period: str, interval: str):
    """
    Fetch the last 7 days of stock price data for the given ticker using yfinance.

    Args:
        symbol (str): Stock ticker symbol.
            - For Indian stocks: append ".NS" for NSE or ".BO" for BSE. 
              Example: "RELIANCE.NS", "TCS.BO"
            - For US stocks: use the ticker as is. 
              Example: "AAPL", "GOOGL", "MSFT"
            - For other foreign exchanges: use the appropriate suffix 
              as per Yahoo Finance conventions. 
              Example: "7203.T" (Toyota on Tokyo Exchange), "RY.TO" (Royal Bank of Canada on Toronto Exchange)
    Defaults:
        period (str): Data retrieval period. Default is '7d' (last 7 days).
        interval (str): Data interval. Default is '1d' (daily data).
    Returns:
        list[dict]: List of stock price records with date and OHLCV data.
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
        • get_news_from_google(ticker) - Retrieve latest news for any stock
        • get_stock_price(symbol) - Fetch 7-day price history

        Stock Symbol Examples:
        • US Stocks: AAPL, GOOGL, MSFT, TSLA
        • Indian Stocks: RELIANCE.NS, TCS.BO, INFY.NS
        • International: 7203.T (Toyota), RY.TO (Royal Bank)

        Ready to begin your financial analysis.
    """
    
    return welcome_msg.strip()



if __name__ == "__main__":
    mcp.run()
