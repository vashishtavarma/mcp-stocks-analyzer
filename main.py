from mcp.server.fastmcp import FastMCP
from src.news import get_news_from_google
from src.price import get_stock_price
from src.company import get_company_info
from src.indicators import get_technical_indicators

DISCLAIMER = """
            DISCLAIMER:
                - All stock data, news, and analysis provided by this server are system-generated and sourced from third-party services (Yahoo Finance, Google News).
                - This information is for informational purposes only.
                - It does not constitute financial or investment advice.
                - Invest at your own risk. We do not claim any responsibility for decisions made based on this data.
"""

mcp = FastMCP("Stock Analyzer", instructions=DISCLAIMER)

mcp.tool()(get_news_from_google)
mcp.tool()(get_stock_price)
mcp.tool()(get_company_info)
mcp.tool()(get_technical_indicators)

if __name__ == "__main__":
    mcp.run()
