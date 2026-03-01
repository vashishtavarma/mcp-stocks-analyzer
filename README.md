# MCP Stocks Analyzer

A simple and efficient Model Context Protocol (MCP) server for financial analysis. This tool provides real-time stock data and news aggregation for AI assistants.

---

## Features

- **Real-time News**: Fetch news articles for stock tickers from Google News.
- **Stock Data**: Retrieve historical OHLCV prices using Yahoo Finance.
- **Company Info**: Fetch fundamentals, ratios, and company profile via Yahoo Finance.
- **MCP Integration**: Seamless compatibility with AI assistants.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/vashishtavarma/mcp-stocks-analyzer.git
   cd mcp-stocks-analyzer
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. Start the MCP server:
   ```bash
   python main.py
   ```

2. Use the available tools. See [API Documentation](docs/API.md) for full details.
   - `get_news_from_google(ticker, region='IN', period='7d')`
   - `get_stock_price(symbol, period, interval)`
   - `get_company_info(symbol)`

---

## Project Structure

- `main.py`: The entry point for the MCP server.
- `finance/`: Contains example scripts for testing individual libraries (`alphavantage.py`, `googlenews.py`, `yahoofinance.py`). These are not used by the main application.
- `docs/`: Documentation files.

---

## Claude Desktop Setup

To integrate MCP Stocks Analyzer with Claude Desktop, follow these steps:

1. **Locate the Configuration File**:
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. **Add the Server Configuration**:
   Insert the following JSON snippet into the `mcpServers` object in the configuration file:

   ```json
   {
     "mcpServers": {
       "stock-analyzer": {
         "command": "<path>/mcp-stocks-analyzer/venv/bin/python",
         "args": [
           "<path>/mcp-stocks-analyzer/main.py"
         ]
       }
     }
   }
   ```

   *Note for Windows users: Adjust the python path to `...\\venv\\Scripts\\python.exe` and use backslashes.*

   > **Important**: Replace `<path>` with the absolute path to your project directory.

3. **Restart Claude Desktop**:
   Restart the application to apply the changes. The MCP Stocks Analyzer tools will now be available in Claude Desktop.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
