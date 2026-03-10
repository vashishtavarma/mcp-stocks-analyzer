from mcp.server.fastmcp import FastMCP
from src.resources.disclaimer import DISCLAIMER
from src.tools import get_news_from_google, get_stock_price, get_company_info, get_technical_indicators
from src.prompts import analyze_stock

mcp = FastMCP("Stock Analyzer", instructions=DISCLAIMER)

mcp.tool()(get_news_from_google)
mcp.tool()(get_stock_price)
mcp.tool()(get_company_info)
mcp.tool()(get_technical_indicators)

mcp.prompt()(analyze_stock)

if __name__ == "__main__":
    mcp.run()
