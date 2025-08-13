from mcp.server.fastmcp import FastMCP
import yfinance as yf

mcp = FastMCP("Finance")

@mcp.tool()
def get_financial_data(ticker: str) -> str:
    yf_data = yf.download(ticker, start="2024-08-13")
    return str(yf_data)