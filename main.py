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
def get_domestic_stock_price(symbol: str):
    """
    Fetch 7 days stock price data for the given ticker using yfinance.
    """
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="10d", interval="1d")
    last_7 = hist.tail(7)
    
    return last_7
    

if __name__ == "__main__":
    mcp.run()
