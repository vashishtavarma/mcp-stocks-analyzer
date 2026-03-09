## `src/price.py`

### 1. Context & Overview
`price.py` implements the MCP tool for retrieving historical stock price data (OHLCV plus dividends and splits) from Yahoo Finance. It uses `yfinance` to fetch the data and returns it as an encoded list of records.

### 2. Structure Analysis
- **Imports**
  - `yfinance as yf` – Yahoo Finance data client.
  - `encode` from `toon` – serialization helper for MCP.
- **Functions**
  - `get_stock_price(symbol: str, period: str, interval: str)`
    - Primary tool function that retrieves and formats price history.

### 3. Key Logic & Responsibilities
- Builds a `yf.Ticker` object from the `symbol`.
- Calls `ticker.history(period=period, interval=interval)` to get a pandas DataFrame of historical data.
- Resets the index so that the date/time becomes a regular column, making conversion to dicts straightforward.
- Converts the DataFrame to a list of dictionaries (`orient="records"`), where each record includes:
  - `Date`, `Open`, `High`, `Low`, `Close`, `Volume`, `Dividends`, `Stock Splits`, and related fields.
- Uses `encode(records)` to serialize the list for MCP.

### 4. Dependencies and Relationships
- **External dependencies**
  - `yfinance` for market data.
  - `toon.encode` for encoding.
- **Internal relationships**
  - Registered as an MCP tool in `main.py` under `get_stock_price`.
  - Conceptually complements `indicators.py`, which derives technical indicators from price history, though they do not call each other directly.

### 5. Usage & Summary
- **Usage example (conceptual)**:
  - As an MCP tool: `get_stock_price("AAPL", period="6mo", interval="1d")` to retrieve six months of daily candles for Apple.
- **Summary**:
  - `price.py` is the low-level price history fetcher for the MCP server, turning Yahoo Finance OHLCV data into an encoded list of uniform records suitable for downstream analysis or display.

