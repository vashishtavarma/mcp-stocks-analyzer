# MCP Stocks Analyzer

A Model Context Protocol (MCP) server that provides news fetching functionality for stock market analysis using Google News.

## Description

This project implements an MCP server called "NewsFetcher" that provides tools for fetching recent news articles related to stock tickers from Google News. It's designed to be used with MCP-compatible AI assistants and applications to provide real-time news context for stock analysis.

## Features

- **MCP Server**: Implements the Model Context Protocol for seamless integration with AI assistants
- **News Fetching**: Retrieves news articles for any stock ticker from Google News
- **Configurable**: Supports different regions, languages, and time periods
- **Structured Output**: Returns formatted article data including title, date, description, and links

## Installation

```bash
# Clone the repository
git clone https://github.com/vashishtavarma/mcp-stocks-analyzer.git
cd mcp-stocks-analyzer

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Running the MCP Server

```bash
python main.py
```

The server will start and listen for MCP connections. It provides the following tool:

- **`get_news_from_google(ticker: str)`**: Fetches news articles for the specified stock ticker from the last 7 days

### Testing with the Simple Script

For quick testing, you can also run the basic news fetcher:

```bash
python googlenews.py
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

## Project Structure

```
mcp-stocks-analyzer/
├── main.py              # MCP server implementation
├── googlenews.py        # Simple test script
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── LICENSE             # MIT License
└── .gitignore          # Git ignore rules
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
- **MCP Connection Issues**: Ensure your MCP client is configured correctly to connect to this server