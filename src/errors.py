def _suggest(symbol: str) -> str:
    s = symbol.upper()
    if s.endswith(".NS"):
        return f"Try '{s.replace('.NS', '.BO')}' (BSE) or verify the ticker spelling."
    if s.endswith(".BO"):
        return f"Try '{s.replace('.BO', '.NS')}' (NSE) or verify the ticker spelling."
    return f"For Indian stocks try '{s}.NS' (NSE) or '{s}.BO' (BSE). For US stocks use plain ticker e.g. 'AAPL'."


def not_found(symbol: str, context: str = "") -> dict:
    return {
        "error": "symbol_not_found",
        "symbol": symbol,
        "message": f"No data returned for '{symbol}'{'. ' + context if context else '.'}",
        "suggestion": _suggest(symbol),
    }


def fetch_failed(symbol: str, exc: Exception) -> dict:
    return {
        "error": "fetch_failed",
        "symbol": symbol,
        "message": str(exc),
        "suggestion": _suggest(symbol),
    }


def invalid_params(message: str) -> dict:
    return {
        "error": "invalid_params",
        "message": message,
    }
