from mcp.server.fastmcp import FastMCP
from GoogleNews import GoogleNews
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
def get_stock_price(ticker: str):
    """
    Fetch intraday stock price data for the given ticker using Alpha Vantage API.
    """
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    if not api_key:
        return {"error": "Alpha Vantage API key not found in environment variables"}
    
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=60min&apikey={api_key}'

    r = requests.get(url)
    data = r.json()
    
    return data



if __name__ == "__main__":
    mcp.run()
