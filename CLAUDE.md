# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Model Context Protocol (MCP) server** that exposes financial data tools to AI assistants (e.g., Claude Desktop). It provides real-time stock prices via Yahoo Finance and news via Google News.

## Setup & Running

```bash
# Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows (Git Bash)
# source venv/bin/activate     # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the MCP server
python main.py
```

## Architecture

All server logic lives in a single file: **`main.py`**. It uses the `FastMCP` framework to register Python functions as MCP tools via the `@mcp.tool()` decorator. When `main.py` is run, `mcp.run()` starts the server.

### Exposed MCP Tools

- **`get_news_from_google(ticker, region='IN', period='7d')`** — Fetches news via `GNews` (from the `gnews` package). Returns a list of article dicts (`title`, `date`, `datetime`, `description`, `link`, `publisher`). Output is encoded via `toon.encode`.
- **`get_stock_price(symbol, period, interval)`** — Fetches OHLCV data via `yfinance`. Returns all records for the requested period as a list of dicts. Output is encoded via `toon.encode`.
- **`get_company_info(symbol)`** — Fetches company profile and financial fundamentals via `yfinance`. Returns a dict of key fields (e.g. `shortName`, `sector`, `marketCap`, `trailingPE`). Returns `{"error": ..., "symbol": ...}` on failure instead of raising.

### `finance/` directory

Contains standalone scripts (`alphavantage.py`, `googlenews.py`, `yahoofinance.py`) for testing individual data sources directly. These are **not imported** by `main.py` and are not part of the server.

## Claude Desktop Integration

Add to `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "stock-analyzer": {
      "command": "<absolute-path>/mcp-stocks-analyzer/venv/Scripts/python.exe",
      "args": ["<absolute-path>/mcp-stocks-analyzer/main.py"]
    }
  }
}
```

## Key Conventions

- New data source tools go in `main.py` as `@mcp.tool()`-decorated functions.
- Indian stocks use `.NS` (NSE) or `.BO` (BSE) suffixes for `yfinance` symbols.
- The `finance/` scripts use `python-dotenv` with a `.env` file for API keys (e.g., `ALPHA_VANTAGE_API_KEY`).
