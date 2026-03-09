## `src/company.py`

### 1. Context & Overview
`company.py` provides an MCP tool to fetch detailed company profile and fundamental data for a given ticker from Yahoo Finance. It returns a rich dictionary with descriptive and financial fields, encoded for MCP clients.

### 2. Structure Analysis
- **Imports**
  - `yfinance as yf` – data source for company fundamentals.
  - `encode` from `toon` – serializer for MCP responses.
- **Functions**
  - `get_company_info(symbol: str) -> dict`
    - Single public function that fetches and encodes the `ticker.info` object.

### 3. Key Logic & Responsibilities
- Wraps the `yf.Ticker(symbol).info` property:
  - `info` is a flat dict of company attributes and ratios.
- Immediately encodes the `info` dict with `encode()` to conform to MCP output conventions.
- Uses a `try/except` block to:
  - On success: return the encoded info.
  - On any exception: return a small error dict `{"error": str(e), "symbol": symbol}` instead of raising, improving resilience for MCP clients.

### 4. Dependencies and Relationships
- **External dependencies**
  - `yfinance` for fundamentals and profile data.
  - `toon.encode` for encoding the output.
- **Internal relationships**
  - Exposed via `main.py` as an MCP tool named `get_company_info`.
  - Often used alongside `get_stock_price` and `get_technical_indicators` to present a holistic view of a stock.

### 5. Usage & Summary
- **Usage example (conceptual)**:
  - `get_company_info("RELIANCE.NS")` to retrieve Reliance Industries’ description, sector, market cap, valuation ratios, and other fundamentals.
- **Summary**:
  - `company.py` centralizes company-level fundamentals retrieval, converting the verbose `yfinance` `info` dict into a directly consumable, encoded payload, with graceful error handling.

