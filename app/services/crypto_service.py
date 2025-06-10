from typing import Any, Dict, List, Tuple, Set
import requests

from app.constants.crypto_constants import COINGECKO_API_BASE
from app.validation.crypto_validation import validate_and_raise


def get_crypto_price(coin_ids: List[str], vs_currencies: List[str] = ["usd"]):
    valid_ids, valid_vs, invalid_ids, invalid_vs = validate_and_raise(
        coin_ids, vs_currencies)

    url = f"{COINGECKO_API_BASE}/simple/price"
    params = {
        "ids": ",".join(valid_ids),
        "vs_currencies": ",".join(valid_vs)
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()

    data = resp.json()
    missing_ids = [cid for cid in valid_ids if cid not in data]

    return {
        "prices": data,
        "invalid_coin_ids": invalid_ids + missing_ids,
        "invalid_vs_currencies": invalid_vs
    }


def get_crypto_history(coin_ids: List[str], vs_currency: str, days: str, interval: str) -> Dict[str, Any]:
    valid_ids, valid_vs, invalid_ids, invalid_vs = validate_and_raise(coin_ids, [
                                                                      vs_currency])

    history_data = {}
    for coin_id in valid_ids:
        try:
            url = f"{COINGECKO_API_BASE}/coins/{coin_id}/market_chart"
            params = {"vs_currency": valid_vs[0],
                      "days": days}
            if interval:
                params["interval"] = interval
            resp = requests.get(url, params=params)
            resp.raise_for_status()

            data = resp.json()
            history_data[coin_id] = {
                "coin_id": coin_id,
                "vs_currency": vs_currency,
                "days": days,
                "prices": data.get("prices", []),
                "market_caps": data.get("market_caps", []),
                "total_volumes": data.get("total_volumes", [])
            }
        except Exception as e:
            history_data[coin_id] = {"error": str(e)}

    return {
        "data": history_data,
        "invalid_coin_ids": invalid_ids,
        "invalid_vs_currencies": invalid_vs
    }


def get_crypto_history_ohlc(coin_ids: List[str], vs_currency: str, days: str, interval: str) -> Dict[str, Any]:
    valid_ids, valid_vs, invalid_ids, invalid_vs = validate_and_raise(coin_ids, [
                                                                      vs_currency])

    history_data = {}
    for coin_id in valid_ids:
        try:
            url = f"{COINGECKO_API_BASE}/coins/{coin_id}/ohlc"
            params = {"vs_currency": valid_vs[0],
                      "days": days}
            if interval:
                params["interval"] = interval
            resp = requests.get(url, params=params)
            resp.raise_for_status()

            ohlc_data = resp.json()
            history_data[coin_id] = {
                "coin_id": coin_id,
                "vs_currency": vs_currency,
                "days": days,
                "ohlc": ohlc_data
            }
        except Exception as e:
            history_data[coin_id] = {"error": str(e)}

    return {
        "data": history_data,
        "invalid_coin_ids": invalid_ids,
        "invalid_vs_currencies": invalid_vs
    }
