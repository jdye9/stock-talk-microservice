from fastapi import APIRouter, HTTPException, Query
from app.services.crypto_service import get_crypto_history_ohlc, get_crypto_price, get_crypto_history

from app.models.crypto_models import CryptoHistoryRequest, CryptoPriceRequest

router = APIRouter()


@router.post("/price")
def crypto_price(payload: CryptoPriceRequest):
    try:
        return get_crypto_price(payload.coin_ids, payload.vs_currencies)
    except HTTPException as e:
        raise e  # re-raise 400 as-is
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/history")
def crypto_history(payload: CryptoHistoryRequest):

    # Validate days input
    if payload.days != "max":
        if not payload.days.isdigit() or int(payload.days) <= 0:
            raise HTTPException(
                status_code=400,
                detail="`days` must be a positive integer or 'max'"
            )

    try:
        return get_crypto_history(payload.coin_ids, payload.vs_currency, payload.days, payload.interval)
    except HTTPException as e:
        raise e  # re-raise 400 as-is
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/history-ohlc")
def crypto_history_ohlc(payload: CryptoHistoryRequest):

    # Validate days input
    if payload.days != "max":
        if not payload.days.isdigit() or int(payload.days) <= 0:
            raise HTTPException(
                status_code=400,
                detail="`days` must be a positive integer or 'max'"
            )

    try:
        return get_crypto_history_ohlc(payload.coin_ids, payload.vs_currency, payload.days, payload.interval)
    except HTTPException as e:
        raise e  # re-raise 400 as-is
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
