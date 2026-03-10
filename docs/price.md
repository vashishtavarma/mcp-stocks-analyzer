## `src/price.py`

### 1. Context & Overview
`price.py` implements the MCP tool for retrieving historical stock price data (OHLCV plus dividends and splits) from Yahoo Finance. It uses `yfinance` to fetch the data, returns it as an encoded list of records, and surfaces structured error responses when a symbol is invalid or no data is available.

### 2. Structure Analysis
- **Imports**
  - `yfinance as yf` – Yahoo Finance data client.
  - `encode` from `toon` – serialization helper for MCP.
  - `not_found`, `fetch_failed` from `src.errors` – shared structured error builders.
- **Functions**
  - `get_stock_price(symbol: str, period: str, interval: str)`
    - Primary tool function that retrieves and formats price history.

### 3. Key Logic & Responsibilities
- Wraps the entire fetch in a `try/except` block:
  - On exception: returns `fetch_failed(symbol, e)` with error code `"fetch_failed"`.
- Builds a `yf.Ticker` object from the `symbol`.
- Calls `ticker.history(period=period, interval=interval)` to get a pandas DataFrame of historical data.
- If the DataFrame is empty, returns `not_found(symbol, ...)` with error code `"symbol_not_found"` and a suffix suggestion (e.g. `SUZLON` → try `SUZLON.NS` or `SUZLON.BO`).
- Resets the index so that the date/time becomes a regular column, making conversion to dicts straightforward.
- Converts the DataFrame to a list of dictionaries (`orient="records"`), where each record includes:
  - `Date`, `Open`, `High`, `Low`, `Close`, `Volume`, `Dividends`, `Stock Splits`, and related fields.
- Uses `encode(records)` to serialize the list for MCP.

### 4. Dependencies and Relationships
- **External dependencies**
  - `yfinance` for market data.
  - `toon.encode` for encoding.
- **Internal relationships**
  - `src.errors` – shared error response helpers.
  - Registered as an MCP tool in `main.py` under `get_stock_price`.
  - Conceptually complements `indicators.py`, which derives technical indicators from price history, though they do not call each other directly.

### 5. Usage & Summary
- **Usage example (conceptual)**:
  - As an MCP tool: `get_stock_price("AAPL", period="6mo", interval="1d")` to retrieve six months of daily candles for Apple.
- **Error response shape**:
  ```json
  {
    "error": "symbol_not_found",
    "symbol": "SUZLON",
    "message": "No data returned for 'SUZLON'. No price data for period='6mo', interval='1d'.",
    "suggestion": "For Indian stocks try 'SUZLON.NS' (NSE) or 'SUZLON.BO' (BSE)."
  }
  ```
- **Summary**:
  - `price.py` is the low-level price history fetcher for the MCP server, turning Yahoo Finance OHLCV data into an encoded list of uniform records suitable for downstream analysis or display, with structured errors to aid recovery when a symbol is not found.

