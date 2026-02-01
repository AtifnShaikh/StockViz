from mcp.server.fastmcp import FastMCP
import yfinance as yf
import matplotlib.pyplot as plt
import os

mcp = FastMCP("StockViz-MCP")

PICTURES_DIR = "Pictures"
os.makedirs(PICTURES_DIR, exist_ok=True)

@mcp.tool()
def get_stock_price(symbol: str) -> float:
    """Get latest stock price"""
    data = yf.Ticker(symbol).history(period="1d")
    return round(float(data["Close"].iloc[-1]), 2)

@mcp.tool()
def get_stock_high_low(symbol: str) -> dict:
    """Get today's high and low price"""
    data = yf.Ticker(symbol).history(period="1d")
    return {
        "high": round(float(data["High"].iloc[-1]), 2),
        "low": round(float(data["Low"].iloc[-1]), 2)
    }

@mcp.tool()
def compare_two_stocks(symbol1: str, symbol2: str) -> dict:
    """Compare two stock prices"""
    p1 = yf.Ticker(symbol1).history(period="1d")["Close"].iloc[-1]
    p2 = yf.Ticker(symbol2).history(period="1d")["Close"].iloc[-1]
    return {
        symbol1: round(float(p1), 2),
        symbol2: round(float(p2), 2)
    }

@mcp.tool()
def plot_stock_trend(symbol: str) -> str:
    """Plot 6 month stock price trend"""
    data = yf.Ticker(symbol).history(period="6mo")

    plt.figure(figsize=(8, 4))
    plt.plot(data.index, data["Close"])
    plt.title(f"{symbol} - 6 Month Price Trend")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)

    path = f"{PICTURES_DIR}/{symbol}_trend.png"
    plt.savefig(path)
    plt.close()

    return f"Plot saved at {path}"

@mcp.tool()
def basic_stock_summary(symbol: str) -> str:
    """Basic textual summary of a stock"""
    data = yf.Ticker(symbol).history(period="6mo")
    start = float(data["Close"].iloc[0])
    end = float(data["Close"].iloc[-1])

    change = ((end - start) / start) * 100
    return f"{symbol} changed by {round(change, 2)}% over the last 6 months."

if __name__ == "__main__":
    mcp.run()
