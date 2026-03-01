# MCP Stocks Analyzer API Documentation

This document describes the tools available in the MCP Stocks Analyzer server.

## Tools

### `get_news_from_google`

Fetches news articles related to the given ticker from Google News.

**Signature:**

```python
get_news_from_google(ticker: str, region: str = 'IN', period: str = '7d') -> list[dict]
```

**Parameters:**

*   `ticker` (str): **Required**. The stock ticker symbol to search news for.
*   `region` (str, optional): The region code for Google News. Defaults to `'IN'`.
    *   Examples: `'US'` (United States), `'IN'` (India), `'GB'` (United Kingdom).
*   `period` (str, optional): The time period for news articles. Defaults to `'7d'`.
    *   Format: Number followed by unit (e.g., `'1d'`, `'7d'`, `'1m'`).

**Returns:**

A list of dictionaries, where each dictionary represents a news article with the following keys:

*   `title` (str): The title of the article.
*   `date` (str): The publication date string.
*   `datetime` (datetime, optional): The publication datetime object (if available).
*   `description` (str): A short description or snippet of the article.
*   `link` (str): The URL to the full article.

**Example Usage:**

```python
# Get news for Apple in the US for the last 7 days
news = get_news_from_google(ticker="AAPL", region="US", period="7d")
```

---

### `get_stock_price`

Fetches stock price data for the given ticker using Yahoo Finance.

**Signature:**

```python
get_stock_price(symbol: str, period: str, interval: str) -> list[dict]
```

**Parameters:**

*   `symbol` (str): **Required**. The stock ticker symbol.
    *   **US Stocks**: Use the ticker as is (e.g., `"AAPL"`, `"MSFT"`).
    *   **Indian Stocks**: Append `".NS"` for NSE or `".BO"` for BSE (e.g., `"RELIANCE.NS"`, `"TCS.BO"`).
    *   **Other Exchanges**: Use appropriate suffix (e.g., `"7203.T"` for Toyota).
*   `period` (str): **Required**. The data retrieval period.
    *   Valid values: `'1d'`, `'5d'`, `'1mo'`, `'3mo'`, `'6mo'`, `'1y'`, `'2y'`, `'5y'`, `'10y'`, `'ytd'`, `'max'`.
*   `interval` (str): **Required**. The data interval.
    *   Valid values: `'1m'`, `'2m'`, `'5m'`, `'15m'`, `'30m'`, `'60m'`, `'90m'`, `'1h'`, `'1d'`, `'5d'`, `'1wk'`, `'1mo'`, `'3mo'`.
    *   Note: Intraday intervals (< `'1d'`) are only available for the trailing 60 days.

**Returns:**

A list of dictionaries, where each dictionary represents a historical price record. The keys typically include:

*   `Date` (datetime): The date of the record.
*   `Open` (float): Opening price.
*   `High` (float): Highest price.
*   `Low` (float): Lowest price.
*   `Close` (float): Closing price.
*   `Volume` (int): Trading volume.
*   `Dividends` (float): Dividends paid.
*   `Stock Splits` (float): Stock splits occurred.

**Example Usage:**

```python
# Get daily stock price for Reliance (NSE) for the last 7 days
prices = get_stock_price(symbol="RELIANCE.NS", period="7d", interval="1d")
```

---

### `get_company_info`

Fetches detailed company profile and financial fundamentals using Yahoo Finance.

**Signature:**

```python
get_company_info(symbol: str) -> dict
```

**Parameters:**

*   `symbol` (str): **Required**. The stock ticker symbol.
    *   **US Stocks**: Use the ticker as is (e.g., `"AAPL"`, `"MSFT"`).
    *   **Indian Stocks**: Append `".NS"` for NSE or `".BO"` for BSE (e.g., `"RELIANCE.NS"`, `"TCS.BO"`).

**Returns:**

A dictionary with company profile and fundamentals. Key fields include:

*   `shortName` (str): Company display name.
*   `sector`, `industry` (str): Business classification.
*   `country`, `city` (str): Headquarters location.
*   `marketCap` (int): Market capitalisation in base currency.
*   `currentPrice`, `fiftyTwoWeekHigh`, `fiftyTwoWeekLow` (float): Price data.
*   `trailingPE`, `forwardPE` (float): Price-to-earnings ratios.
*   `dividendYield` (float): Annual dividend yield.
*   `returnOnEquity`, `returnOnAssets` (float): Profitability ratios.
*   `totalRevenue`, `netIncomeToCommon` (int): Income statement highlights.
*   `debtToEquity` (float): Leverage ratio.
*   `longBusinessSummary` (str): Full business description.

On failure, returns `{"error": "<message>", "symbol": "<symbol>"}` instead of raising an exception.

**Example Usage:**

```python
# Get company info for TCS (NSE)
info = get_company_info(symbol="TCS.NS")
```
