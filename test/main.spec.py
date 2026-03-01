import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import get_news_from_google


def test_get_news_from_google():
    news = get_news_from_google("AAPL", "US", "7d")
    return news

if __name__ == "__main__":
    print(test_get_news_from_google())
