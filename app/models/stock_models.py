from pydantic import BaseModel, Field
from typing import List


class StockPriceRequest(BaseModel):
    tickers: List[str] = Field(..., min_length=1)


class StockHistoryRequest(BaseModel):
    tickers: List[str] = Field(..., min_length=1)
    # e.g., "1d", "5d", "1mo", "6mo", "1y"
    period: str = Field(default="1mo")
    interval: str = Field(default="1d")    # e.g., "1m", "5m", "1d"
