"""
Example script for testing the GNews library.
It is not part of the main MCP Stocks Analyzer application logic.
"""

from gnews import GNews

google_news = GNews(language="en", country="US", period="7d")
results = google_news.get_news("Tata motors")
print(results[0] if results else "No results")