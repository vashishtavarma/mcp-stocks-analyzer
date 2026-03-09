## `src/news.py`

### 1. Context & Overview
`news.py` defines the MCP tool that fetches stock-related news from Google News. It wraps the `gnews` library and normalizes the results into a simple list of article dictionaries, then encodes them for MCP transport.

### 2. Structure Analysis
- **Imports**
  - `GNews` from `gnews` – client for Google News.
  - `encode` from `toon` – helper to serialize Python objects for MCP responses.
- **Functions**
  - `get_news_from_google(ticker: str, region: str = 'IN', period: str = '7d')`
    - Main (and only) exported function; registered as an MCP tool in `main.py`.

### 3. Key Logic & Responsibilities
- Creates a `GNews` client configured with:
  - English language (`"en"`).
  - Country/region from the `region` parameter.
  - Time range from the `period` parameter (e.g. `'7d'`).
- Calls `get_news(ticker)` to fetch related news articles.
- Safely handles `None` by using `or []` to ensure iteration is always over a list.
- For each result, builds a normalized dictionary with:
  - `title`, `date`, `datetime` (currently `None` placeholder), `description`, `link`, `publisher`.
- Encodes the list of article dicts using `encode()` before returning.

### 4. Dependencies and Relationships
- **External dependencies**
  - `gnews` for the Google News scraping/search API.
  - `toon.encode` for MCP-friendly serialization.
- **Internal relationships**
  - This function is imported and registered as an MCP tool in `main.py`.
  - Other modules do not directly depend on it; it is a standalone news-fetching tool.

### 5. Usage & Summary
- **Usage example (conceptual)**:
  - As an MCP tool: call `get_news_from_google(ticker="AAPL", region="US", period="1d")` from your AI client to get fresh Apple news articles.
- **Summary**:
  - `news.py` is responsible exclusively for fetching and shaping stock news data from Google News, providing a predictable, encoded list of article dictionaries for the MCP server.

