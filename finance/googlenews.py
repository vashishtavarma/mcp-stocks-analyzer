"""
This is an example script for testing the GoogleNews library.
It is not part of the main MCP Stocks Analyzer application logic.
"""

from GoogleNews import GoogleNews

googlenews = GoogleNews(lang='en', region='US', period='7d', encode='utf-8')
googlenews.get_news('Tata motors')
print(googlenews.results())