from GoogleNews import GoogleNews

googlenews = GoogleNews(lang='en', region='US', period='7d', encode='utf-8')
googlenews.get_news('Tata motors')
print(googlenews.results())