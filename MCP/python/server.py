from mcp.server.fastmcp import FastMCP
import yfinance as yf

mcp = FastMCP("Finance")

@mcp.tool()
def get_financial_data(ticker: str) -> str:
    yf_data = yf.download(ticker, start="2024-08-13")
    return str(yf_data)

@mcp.tool(description="Get the current live stock price")
def get_current_price(ticker: str) -> dict:
    stock = yf.Ticker(ticker)
    price = stock.history(period="1d")["Close"].iloc[-1]
    return {"ticker": ticker, "price": round(price, 2)}

@mcp.tool(description="Get company info for a stock ticker")
def get_company_info(ticker: str) -> dict:
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "ticker": ticker,
        "longName": info.get("longName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "marketCap": info.get("marketCap"),
        "currency": info.get("currency"),
    }