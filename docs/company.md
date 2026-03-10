## `src/company.py`

### 1. Context & Overview
`company.py` provides an MCP tool to fetch detailed company profile and fundamental data for a given ticker from Yahoo Finance. It returns a rich dictionary with descriptive and financial fields, encoded for MCP clients, and surfaces structured error responses when the symbol is invalid or the profile is empty.

### 2. Structure Analysis
- **Imports**
  - `yfinance as yf` – data source for company fundamentals.
  - `encode` from `toon` – serializer for MCP responses.
  - `not_found`, `fetch_failed` from `src.errors` – shared structured error builders.
- **Functions**
  - `get_company_info(symbol: str) -> dict`
    - Single public function that fetches and encodes the `ticker.info` object.

### 3. Key Logic & Responsibilities
- Wraps the fetch in a `try/except` block:
  - On exception: returns `fetch_failed(symbol, e)` with error code `"fetch_failed"`.
- Calls `yf.Ticker(symbol).info` to retrieve a flat dict of company attributes and ratios.
- Validates the returned `info` dict:
  - If it is empty, has `quoteType == "NONE"`, or is missing `shortName`, returns `not_found(symbol, ...)` with error code `"symbol_not_found"` and a suffix suggestion.
- On success: encodes the `info` dict with `encode()` to conform to MCP output conventions.

### 4. Dependencies and Relationships
- **External dependencies**
  - `yfinance` for fundamentals and profile data.
  - `toon.encode` for encoding the output.
- **Internal relationships**
  - `src.errors` – shared error response helpers.
  - Exposed via `main.py` as an MCP tool named `get_company_info`.
  - Often used alongside `get_stock_price` and `get_technical_indicators` to present a holistic view of a stock.

### 5. Usage & Summary
- **Usage example (conceptual)**:
  - `get_company_info("RELIANCE.NS")` to retrieve Reliance Industries' description, sector, market cap, valuation ratios, and other fundamentals.
- **Error response shape**:
  ```json
  {
    "error": "symbol_not_found",
    "symbol": "RELIANCE",
    "message": "No data returned for 'RELIANCE'. Yahoo Finance returned no company profile.",
    "suggestion": "For Indian stocks try 'RELIANCE.NS' (NSE) or 'RELIANCE.BO' (BSE)."
  }
  ```
- **Summary**:
  - `company.py` centralizes company-level fundamentals retrieval, converting the verbose `yfinance` `info` dict into a directly consumable, encoded payload, with structured error handling to help callers identify and recover from invalid symbols.

