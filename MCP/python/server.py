from mcp.server.fastmcp import FastMCP
from typing import Optional, Dict, Any
import yfinance as yf
import pandas as pd
from datetime import datetime

mcp = FastMCP("Finance")


@mcp.tool(
    description="Get historical stock data with flexible date ranges and intervals"
)
def get_financial_data(
    ticker: str,
    start_date: str = "2025-01-01",
    end_date: Optional[str] = None,
    period: Optional[str] = None,
    interval: str = "1d",
) -> Dict[str, Any]:
    """
    Get comprehensive historical stock data.

    Args:
        ticker: Stock symbol (e.g., 'AAPL', 'TSLA')
        start_date: Start date in YYYY-MM-DD format (default: 2024-01-01)
        end_date: End date in YYYY-MM-DD format (optional, defaults to today)
        period: Alternative to start/end dates ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
        interval: Data interval ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo')
    """
    ticker = ticker.upper().strip()

    if period:
        yf_data = yf.download(ticker, period=period, interval=interval, progress=False)
    else:
        yf_data = yf.download(
            ticker, start=start_date, end=end_date, interval=interval, progress=False
        )

    if yf_data.empty:
        return {"error": f"No data found for ticker {ticker}"}

    yf_data["Daily_Return"] = yf_data["Close"].pct_change()
    yf_data["MA_20"] = yf_data["Close"].rolling(window=20).mean()
    yf_data["MA_50"] = yf_data["Close"].rolling(window=50).mean()
    yf_data["Volatility"] = yf_data["Daily_Return"].rolling(window=20).std()

    latest_data = yf_data.iloc[-1]
    first_data = yf_data.iloc[0]

    total_return = (
        (latest_data["Close"] - first_data["Close"]) / first_data["Close"]
    ) * 100
    avg_volume = yf_data["Volume"].mean()
    max_price = yf_data["High"].max()
    min_price = yf_data["Low"].min()

    return {
        "ticker": ticker,
        "period": f"{yf_data.index[0].date()} to {yf_data.index[-1].date()}",
        "data_points": len(yf_data),
        "summary": {
            "latest_price": round(latest_data["Close"], 2),
            "total_return_percent": round(total_return, 2),
            "period_high": round(max_price, 2),
            "period_low": round(min_price, 2),
            "average_volume": int(avg_volume),
            "current_ma_20": round(latest_data["MA_20"], 2)
            if pd.notna(latest_data["MA_20"])
            else None,
            "current_ma_50": round(latest_data["MA_50"], 2)
            if pd.notna(latest_data["MA_50"])
            else None,
            "current_volatility": round(latest_data["Volatility"] * 100, 2)
            if pd.notna(latest_data["Volatility"])
            else None,
        },
        "recent_data": yf_data.tail(5).round(2).to_dict("records"),
        "technical_indicators": {
            "price_above_ma20": latest_data["Close"] > latest_data["MA_20"]
            if pd.notna(latest_data["MA_20"])
            else None,
            "price_above_ma50": latest_data["Close"] > latest_data["MA_50"]
            if pd.notna(latest_data["MA_50"])
            else None,
            "ma20_above_ma50": latest_data["MA_20"] > latest_data["MA_50"]
            if pd.notna(latest_data["MA_20"]) and pd.notna(latest_data["MA_50"])
            else None,
        },
    }


@mcp.tool(
    description="Get the current live stock price with additional real-time metrics"
)
def get_current_price(ticker: str) -> Dict[str, Any]:
    """Get current stock price with extended metrics"""
    ticker = ticker.upper().strip()
    stock = yf.Ticker(ticker)

    hist_data = stock.history(period="5d", interval="1d")
    if hist_data.empty:
        return {"error": f"No data found for ticker {ticker}"}

    current_price = hist_data["Close"].iloc[-1]
    prev_close = hist_data["Close"].iloc[-2] if len(hist_data) > 1 else current_price

    daily_change = current_price - prev_close
    daily_change_percent = (daily_change / prev_close) * 100 if prev_close != 0 else 0

    intraday = stock.history(period="1d", interval="1m")
    day_high = intraday["High"].max() if not intraday.empty else current_price
    day_low = intraday["Low"].min() if not intraday.empty else current_price
    day_volume = hist_data["Volume"].iloc[-1] if "Volume" in hist_data.columns else 0

    return {
        "ticker": ticker,
        "current_price": round(current_price, 2),
        "daily_change": round(daily_change, 2),
        "daily_change_percent": round(daily_change_percent, 2),
        "day_high": round(day_high, 2),
        "day_low": round(day_low, 2),
        "day_volume": int(day_volume),
        "previous_close": round(prev_close, 2),
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


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


@mcp.tool(description="Get financial news and analyst recommendations")
def get_stock_news_and_recommendations(ticker: str) -> Dict[str, Any]:
    """Get latest news and analyst recommendations for a stock"""
    ticker = ticker.upper().strip()
    stock = yf.Ticker(ticker)

    # Get recommendations
    try:
        recommendations = stock.recommendations
        if recommendations is not None and not recommendations.empty:
            latest_rec = recommendations.tail(1).iloc[0]
            rec_summary = {
                "period": str(latest_rec.name),
                "firm": latest_rec.get("Firm", "Unknown"),
                "to_grade": latest_rec.get("To Grade", "N/A"),
                "from_grade": latest_rec.get("From Grade", "N/A"),
                "action": latest_rec.get("Action", "N/A"),
            }
        else:
            rec_summary = {"message": "No recent recommendations available"}
    except:
        rec_summary = {"error": "Could not fetch recommendations"}

    # Get analyst price targets
    try:
        info = stock.info
        analyst_info = {
            "target_high_price": info.get("targetHighPrice"),
            "target_low_price": info.get("targetLowPrice"),
            "target_mean_price": info.get("targetMeanPrice"),
            "target_median_price": info.get("targetMedianPrice"),
            "recommendation_mean": info.get("recommendationMean"),
            "recommendation_key": info.get("recommendationKey"),
            "number_of_analyst_opinions": info.get("numberOfAnalystOpinions"),
        }
    except:
        analyst_info = {"error": "Could not fetch analyst targets"}

    return {
        "ticker": ticker,
        "latest_recommendation": rec_summary,
        "analyst_targets": analyst_info,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
