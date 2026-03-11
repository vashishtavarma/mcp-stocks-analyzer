from ..resources.disclaimer import DISCLAIMER


def analyze_stock(company_name: str, symbol: str, target_date: str) -> str:
    """Analyze a stock and predict its direction for a target date."""
    return f"""Analyze {company_name} ({symbol}) and predict its stock direction for {target_date}.
            Use your MCP tools to gather data in this order:
            1. Call get_stock_price(symbol="{symbol}", period="1mo", interval="1d") — use the last 10 trading days of results
            2. Call get_technical_indicators(symbol="{symbol}", period="6mo", interval="1d") — use trend, momentum, volatility, volume, and signals
            3. Call get_news_from_google(ticker="{symbol}", region="IN", period="10d") — fetch recent news

            After collecting all data, synthesize everything and give me ONE verdict.

            Output MUST follow this exact format:

            Verdict: [BULLISH / BEARISH / NEUTRAL]
            Current Price: ₹X
            Target Price: ₹X (by {target_date})
            Profit Potential: X%

            Top Reasons: ...
            Key Risk: ...

            {DISCLAIMER}"""
