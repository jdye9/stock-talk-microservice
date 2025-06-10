import pandas as pd
import yfinance as yf
from typing import Any, Dict, List


def get_stock_price(tickers: list[str]) -> dict[str, float]:
    prices = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            prices[ticker] = stock.fast_info['lastPrice']
        except Exception as e:
            prices[ticker] = f"Error: {str(e)}"
    return {
        "tickers": tickers,
        "prices": prices
    }


def get_stock_history(tickers: List[str], period: str = "5d", interval: str = "1d") -> Dict[str, Any]:
    result = {}

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(
                period=period, interval=interval, auto_adjust=False)

            if data.empty:
                result[ticker] = {"error": "No data found"}
                continue

            data = data.reset_index()
            # Pick column dynamically based on what exists
            if "Date" in data.columns:
                date_col = "Date"
            elif "Datetime" in data.columns:
                date_col = "Datetime"
            else:
                raise ValueError("No valid date/time column found")

            result[ticker] = data[[date_col, "Open", "Close", "Adj Close",
                                   "Low", "High", "Volume"]].to_dict(orient="records")
        except Exception as e:
            result[ticker] = {"error": str(e)}

    return result
