from typing import List
from pydantic import BaseModel, Field


class CryptoPriceRequest(BaseModel):
    coin_ids: List[str] = Field(..., min_length=1)
    vs_currencies: List[str] = Field(["usd"], min_length=1)


class CryptoHistoryRequest(BaseModel):
    coin_ids: List[str] = Field(..., min_length=1)
    vs_currency: str = Field("usd", min_length=1)
    days: str = Field("1")  # Accepts "max" or positive int as string
    # "5m", "hourly", "daily". Leave empty for automatic granularity
    interval: str = Field("")
