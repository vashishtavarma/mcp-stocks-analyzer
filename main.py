from mcp.server.fastmcp import FastMCP
from GoogleNews import GoogleNews
import yfinance as yf

mcp = FastMCP("NewsFetcher")

@mcp.tool()
def get_news_from_google(ticker: str):
    """ 
        Fetch news articles related to the given ticker from Google News.
    """
    googlenews = GoogleNews(lang='en', region='IN', period='7d', encode='utf-8')
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
def get_stock_price(symbol: str):
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

    Returns:
        list[dict]: List of stock price records with date and OHLCV data.
    """
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="10d", interval="1d").tail(7)
    hist = hist.reset_index()
    records = hist.to_dict(orient="records")

    return records


if __name__ == "__main__":
    mcp.run()
