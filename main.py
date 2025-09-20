from mcp.server.fastmcp import FastMCP
from GoogleNews import GoogleNews

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


if __name__ == "__main__":
    mcp.run()
