import yfinance as yf
from toon import encode
from src.errors import not_found, fetch_failed


def get_stock_price(symbol: str, period: str, interval: str):
    """
    Fetch historical OHLCV price data for a stock using Yahoo Finance.

    Args:
        symbol: Yahoo Finance ticker symbol.
            - US stocks: plain ticker, e.g. 'AAPL', 'MSFT', 'GOOGL'.
            - Indian stocks: append '.NS' (NSE) or '.BO' (BSE), e.g. 'RELIANCE.NS', 'TCS.BO'.
            - Other exchanges: use the Yahoo Finance suffix, e.g. '7203.T' (Toyota/Tokyo),
              'RY.TO' (Royal Bank of Canada/Toronto).
        period: Total span of data to retrieve.
            - Valid values: '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'.
            - Default: 7d
        interval: Granularity of each data point.
            - Valid values: '1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'.
            - Default: '1d'
            - Note: Intraday intervals (< '1d') are only available for the trailing 60 days.

    Returns:
        list[dict]: OHLCV records, each containing:
            - Date (datetime): Timestamp of the record.
            - Open, High, Low, Close (float): Price data.
            - Volume (int): Trading volume.
            - Dividends (float): Dividends paid.
            - Stock Splits (float): Stock splits occurred.
    """
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period, interval=interval)
        if hist.empty:
            return not_found(symbol, f"No price data for period='{period}', interval='{interval}'.")
        hist = hist.reset_index()
        records = hist.to_dict(orient="records")
        return encode(records)
    except Exception as e:
        return fetch_failed(symbol, e)
