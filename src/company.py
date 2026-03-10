import yfinance as yf
from toon import encode
from src.errors import not_found, fetch_failed


def get_company_info(symbol: str) -> dict:
    """
    Fetch detailed company information and fundamentals for a stock using Yahoo Finance.

    Args:
        symbol: Yahoo Finance ticker symbol.
            - US stocks: plain ticker, e.g. 'AAPL', 'MSFT', 'GOOGL'.
            - Indian stocks: append '.NS' (NSE) or '.BO' (BSE), e.g. 'RELIANCE.NS', 'TCS.BO'.

    Returns:
        dict: Company profile and fundamentals, including fields such as:
            - shortName (str): Company display name.
            - sector, industry (str): Business classification.
            - country, city (str): Headquarters location.
            - marketCap (int): Market capitalisation in base currency.
            - currentPrice, fiftyTwoWeekHigh, fiftyTwoWeekLow (float): Price data.
            - trailingPE, forwardPE (float): Price-to-earnings ratios.
            - dividendYield (float): Annual dividend yield.
            - returnOnEquity, returnOnAssets (float): Profitability ratios.
            - totalRevenue, netIncomeToCommon (int): Income statement highlights.
            - debtToEquity (float): Leverage ratio.
            - longBusinessSummary (str): Full business description.
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        if not info or info.get("quoteType") == "NONE" or "shortName" not in info:
            return not_found(symbol, "Yahoo Finance returned no company profile.")
        return encode(info)
    except Exception as e:
        return fetch_failed(symbol, e)
