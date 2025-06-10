from fastapi import APIRouter, HTTPException
from app.models.stock_models import StockPriceRequest, StockHistoryRequest
from app.services.stock_service import get_stock_history, get_stock_price

router = APIRouter()


@router.post("/price")
def stock_price(payload: StockPriceRequest):
    try:
        return get_stock_price(payload.tickers)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/history")
def stock_history(payload: StockHistoryRequest):
    try:
        return get_stock_history(payload.tickers, payload.period, payload.interval)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
