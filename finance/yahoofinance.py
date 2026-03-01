"""
This is an example script for testing the yfinance library.
It is not part of the main MCP Stocks Analyzer application logic.
"""

import yfinance as yf
from toon import encode

def get_last_7_days(symbol):
    ticker = yf.Ticker(symbol)
    print(ticker)
    hist = ticker.history(period="7d", interval="1h")
    return hist

def check(symbol):
    ticker = yf.Ticker(symbol)
    return encode(ticker.info)

print(check("SWIGGY.NS"))
# data = get_last_7_days("SWIGGY.NS")
# print(data)
