## `src/news.py`

### 1. Context & Overview
`news.py` defines the MCP tool that fetches stock-related news from Google News. It wraps the `gnews` library, normalizes results into a simple list of article dictionaries, and returns structured error responses when no articles are found or the fetch fails.

### 2. Structure Analysis
- **Imports**
  - `GNews` from `gnews` – client for Google News.
  - `encode` from `toon` – helper to serialize Python objects for MCP responses.
  - `not_found`, `fetch_failed` from `src.errors` – shared structured error builders.
- **Functions**
  - `get_news_from_google(ticker: str, region: str = 'IN', period: str = '7d')`
    - Main (and only) exported function; registered as an MCP tool in `main.py`.

### 3. Key Logic & Responsibilities
- Wraps the entire operation in a `try/except` block:
  - On exception: returns a structured `"fetch_failed"` error dict with the exception message and a spelling suggestion.
- Creates a `GNews` client configured with:
  - English language (`"en"`).
  - Country/region from the `region` parameter.
  - Time range from the `period` parameter (e.g. `'7d'`).
- Calls `get_news(ticker)` to fetch related news articles.
- If results are empty, returns a structured `"no_results"` error with a suggestion to broaden the period or try the full company name.
- For each result, builds a normalized dictionary with:
  - `title`, `date`, `datetime` (currently `None` placeholder), `description`, `link`, `publisher`.
- Encodes the list of article dicts using `encode()` before returning.

### 4. Dependencies and Relationships
- **External dependencies**
  - `gnews` for the Google News scraping/search API.
  - `toon.encode` for MCP-friendly serialization.
- **Internal relationships**
  - `src.errors` – shared error response helpers.
  - This function is imported and registered as an MCP tool in `main.py`.
  - Other modules do not directly depend on it; it is a standalone news-fetching tool.

### 5. Usage & Summary
- **Usage example (conceptual)**:
  - As an MCP tool: call `get_news_from_google(ticker="AAPL", region="US", period="1d")` from your AI client to get fresh Apple news articles.
- **Error response shapes**:
  ```json
  {
    "error": "no_results",
    "ticker": "AAPL",
    "message": "No news found for 'AAPL' in region='US' over the past 1d.",
    "suggestion": "Try a broader period (e.g. '30d'), a different region, or the full company name."
  }
  ```
  ```json
  {
    "error": "fetch_failed",
    "ticker": "AAPL",
    "message": "<exception message>",
    "suggestion": "Check that the ticker or company name is spelled correctly."
  }
  ```
- **Summary**:
  - `news.py` is responsible exclusively for fetching and shaping stock news data from Google News, providing a predictable, encoded list of article dictionaries for the MCP server, with structured errors to help callers recover gracefully.

