# MCP Stocks Analyzer

A comprehensive Model Context Protocol (MCP) server that provides financial data analysis tools including news fetching, stock data retrieval, and market analysis capabilities.

## Description

This project implements an MCP server called "NewsFetcher" that provides multiple tools for comprehensive stock market analysis. It integrates various financial data sources including Google News, Yahoo Finance, and Alpha Vantage to provide real-time financial insights and news context for stock analysis.

## Features

- **MCP Server**: Implements the Model Context Protocol for seamless integration with AI assistants
- **News Fetching**: Retrieves news articles for any stock ticker from Google News
- **Stock Data**: Access to real-time and historical stock data via Yahoo Finance
- **Alpha Vantage Integration**: Professional-grade financial data and market analysis
- **Multiple Data Sources**: Combines news, price data, and financial metrics
- **Configurable**: Supports different regions, languages, and time periods
- **Structured Output**: Returns formatted data including title, date, description, and links

## Installation

```bash
# Clone the repository
git clone https://github.com/vashishtavarma/mcp-stocks-analyzer.git
cd mcp-stocks-analyzer

# Create a virtual environment (recommended)
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Optional: Set up Alpha Vantage API key
# Create a .env file and add your API key:
# ALPHA_VANTAGE_API_KEY=your_api_key_here
```

## Usage

### Running the MCP Server

```bash
python main.py
```

The server will start and listen for MCP connections. It provides the following tool:

- **`get_news_from_google(ticker: str)`**: Fetches news articles for the specified stock ticker from the last 7 days

### Testing with Individual Modules

For quick testing of specific functionalities:

```bash
# Test Google News fetching
python finance/googlenews.py

# Test Yahoo Finance integration
python finance/yahoofinance.py

# Test Alpha Vantage API (requires API key in .env)
python finance/alphavantage.py
```

### Integration with MCP Clients

To use this server with an MCP-compatible client, configure your client to connect to this server. The server provides:

- **Server Name**: NewsFetcher
- **Available Tools**: 
  - `get_news_from_google`: Fetch news articles for stock tickers

### Example Tool Usage

When integrated with an MCP client, you can use the tool like this:

```python
# The tool will return a list of articles with the following structure:
{
    "title": "Article Title",
    "date": "Publication Date",
    "datetime": "ISO DateTime",
    "description": "Article Description",
    "link": "Article URL"
}
```

## Configuration

The news fetcher is configured for:
- **Language**: English (`en`)
- **Region**: India (`IN`)
- **Period**: Last 7 days (`7d`)
- **Encoding**: UTF-8

You can modify these settings in the `main.py` file as needed.

## Dependencies

- `fastmcp` - FastMCP framework for building MCP servers
- `GoogleNews` - Google News scraping library
- `mcp` - Model Context Protocol implementation
- `requests` - HTTP library for API calls
- `yfinance` - Yahoo Finance data retrieval
- `python-dotenv` - Environment variable management (for Alpha Vantage API key)

## Project Structure

```
mcp-stocks-analyzer/
├── main.py                  # MCP server implementation
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── LICENSE                 # MIT License
├── .gitignore             # Git ignore rules
└── finance/               # Financial data modules
    ├── alphavantage.py    # Alpha Vantage API integration
    ├── googlenews.py      # Google News scraping
    └── yahoofinance.py    # Yahoo Finance data retrieval
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Troubleshooting

- **Import Errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`
- **News Not Loading**: Check your internet connection and verify the ticker symbol is valid
- **Alpha Vantage Errors**: Ensure your API key is correctly set in the `.env` file
- **MCP Connection Issues**: Ensure your MCP client is configured correctly to connect to this server
- **Virtual Environment Issues**: Make sure your virtual environment is activated before running the scripts

## API Keys

To use Alpha Vantage functionality, you'll need to:
1. Get a free API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
2. Create a `.env` file in the project root
3. Add your API key: `ALPHA_VANTAGE_API_KEY=your_api_key_here`