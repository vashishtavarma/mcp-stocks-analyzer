import yfinance as yf

def get_last_7_days(symbol):
    ticker = yf.Ticker(symbol)
    print(ticker)
    hist = ticker.history(period="10d", interval="1d")
    last_7 = hist.tail(7)
    return last_7

data = get_last_7_days("SWIGGY.NS")
print(data)
