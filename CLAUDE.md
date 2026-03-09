# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Model Context Protocol (MCP) server** that exposes financial data tools to AI assistants (e.g., Claude Desktop). It provides real-time stock prices and company fundamentals via Yahoo Finance, news via Google News, and derived technical indicators via the `ta` library.

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

The MCP server entry point is **`main.py`**. It creates a `FastMCP` instance and registers tool functions imported from the `src/` package:

- `src/news.py` — `get_news_from_google`
- `src/price.py` — `get_stock_price`
- `src/company.py` — `get_company_info`
- `src/indicators.py` — `get_technical_indicators`

When `main.py` is run, `mcp.run()` starts the server and exposes these functions as MCP tools.

### Exposed MCP Tools

- **`get_news_from_google(ticker, region='IN', period='7d')`** — Fetches news via `GNews` (from the `gnews` package). Returns a list of article dicts (`title`, `date`, `datetime`, `description`, `link`, `publisher`). Output is encoded via `toon.encode`.
- **`get_stock_price(symbol, period, interval)`** — Fetches OHLCV data via `yfinance`. Returns all records for the requested period as a list of dicts. Output is encoded via `toon.encode`.
- **`get_company_info(symbol)`** — Fetches company profile and financial fundamentals via `yfinance`. Returns a dict of key fields (e.g. `shortName`, `sector`, `marketCap`, `trailingPE`). Returns `{"error": ..., "symbol": ...}` on failure instead of raising. Output is encoded via `toon.encode`.
- **`get_technical_indicators(symbol, period='6mo', interval='1d')`** — Computes higher-level technical analysis metrics (trend, momentum, volatility, volume, and signals) using historical data from `yfinance` and indicators from the `ta` library. Returns a structured dict summarizing the current technical setup for the symbol.

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

- New tools should generally be implemented in `src/` modules and registered in `main.py` via `mcp.tool()(your_function)`.
- Indian stocks use `.NS` (NSE) or `.BO` (BSE) suffixes for `yfinance` symbols.
