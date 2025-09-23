from dotenv import load_dotenv
import requests
import os

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv('ALPHA_VANTAGE_API_KEY')

url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=60min&apikey={api_key}'

response = requests.get(url)
data = response.json()
print(data)