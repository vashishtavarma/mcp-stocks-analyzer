## `src/indicators.py`

### 1. Context & Overview
`indicators.py` computes higher-level technical analysis indicators and summary signals for a given stock using historical price data from Yahoo Finance and the `ta` library. It distills raw OHLCV data into trend, momentum, volatility, volume metrics, and interpreted trading signals.

### 2. Structure Analysis
- **Imports**
  - `yfinance as yf` – to fetch historical price data.
  - `pandas as pd` – for NaN handling and DataFrame operations.
  - `ta` – technical analysis indicators library.
- **Functions**
  - `get_technical_indicators(symbol: str, period: str = "6mo", interval: str = "1d") -> dict`
    - Single exported function; orchestrates data retrieval, feature computation, and summary generation.
  - Inner helper:
    - `safe(val)` – nested helper to convert values to rounded floats or `None`.

### 3. Key Logic & Responsibilities
- **Data retrieval & preparation**
  - Fetches history via `yf.Ticker(symbol).history(period=period, interval=interval)`.
  - Returns `{"error": f"No data found for {symbol}"}` if no data is found.
  - Normalizes column names (handles multi-index cases).
  - Extracts `close`, `high`, `low`, `volume` series and latest price.
- **Trend indicators**
  - Computes SMAs: 20, 50, 200-period; EMAs: 12, 26.
  - Computes MACD (line, signal, histogram).
  - Computes ADX for trend strength.
- **Momentum indicators**
  - RSI(14).
  - Stochastic oscillator %K and %D.
  - Williams %R(14).
  - CCI(20).
- **Volatility indicators**
  - Bollinger Bands (upper, middle, lower).
  - ATR(14) and ATR as a percentage of price.
- **Volume indicators**
  - OBV (On-Balance Volume).
  - VWAP.
  - 20-period SMA of volume and relative volume vs this average.
- **Signals and derived summaries**
  - Uses `safe()` to standardize numeric values (rounded, NaN-safe).
  - Builds a `signals` list including:
    - RSI overbought/oversold hints.
    - MACD bullish/bearish crossovers.
    - Golden/Death cross based on SMA50 vs SMA200 (current vs previous bar).
    - Bollinger band breakout (price above upper or below lower band) and “squeeze” (narrow band width).
  - Computes price position vs key moving averages:
    - Whether price is above/below each MA and distance in percent.
  - Assesses trend strength from ADX (weak, moderate, strong) and direction (bullish, bearish, neutral) based on MA structure and price.
- **Return structure**
  - Returns a nested dict with top-level keys:
    - `symbol`, `last_price`, `date`.
    - `trend` – direction, strength, ADX, MA values, MACD details, price vs MA.
    - `momentum` – RSI, Stoch, Williams %R, CCI.
    - `volatility` – ATR, ATR %, Bollinger band values and bandwidth.
    - `volume` – current/avg volume, relative volume, OBV, VWAP.
    - `signals` – list of human-readable signal entries.

### 4. Dependencies and Relationships
- **External dependencies**
  - `yfinance` – price history source.
  - `pandas` – NaN detection and numeric conversion.
  - `ta` – indicator computations (trend, momentum, volatility, volume).
- **Internal relationships**
  - Conceptually complements `price.py`:
    - `price.py` exposes raw OHLCV; `indicators.py` adds interpretation and aggregation.
  - Registered as `get_technical_indicators` MCP tool in `main.py`.
  - Can be used by AI clients to provide more insightful commentary and trade sentiment rather than just raw price data.

### 5. Usage & Summary
- **Usage example (conceptual)**:
  - `get_technical_indicators("AAPL", period="6mo", interval="1d")` to get the latest technical state for Apple, including trend classification and notable signals.
- **Summary**:
  - `indicators.py` is the technical analysis engine of the project, turning historical prices into an opinionated, structured set of indicators and signals that are easy for an AI or UI to consume.

