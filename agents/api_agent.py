
from fastapi import FastAPI, Query
import yfinance as yf

app = FastAPI()

@app.get("/stock-info")
def get_stock_info(ticker: str = Query(..., example="TSM")):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "symbol": info.get("symbol"),
            "name": info.get("shortName"),
            "price": info.get("currentPrice"),
            "currency": info.get("currency"),
            "sector": info.get("sector"),
            "marketCap": info.get("marketCap"),
            "trailingPE": info.get("trailingPE"),
        }
    except Exception as e:
        return {"error": str(e)}
