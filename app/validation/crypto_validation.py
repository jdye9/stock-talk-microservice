# validation.py
from fastapi import HTTPException
from typing import List, Tuple, Set
import requests

from app.constants.crypto_constants import COINGECKO_API_BASE

_valid_coin_ids_cache: Set[str] = set()
_valid_vs_currencies_cache: Set[str] = set()


def get_valid_coin_ids() -> Set[str]:
    global _valid_coin_ids_cache
    if not _valid_coin_ids_cache:
        url = f"{COINGECKO_API_BASE}/coins/list"
        resp = requests.get(url)
        resp.raise_for_status()
        _valid_coin_ids_cache = {coin["id"] for coin in resp.json()}
    return _valid_coin_ids_cache


def get_valid_vs_currencies() -> Set[str]:
    global _valid_vs_currencies_cache
    if not _valid_vs_currencies_cache:
        url = f"{COINGECKO_API_BASE}/simple/supported_vs_currencies"
        resp = requests.get(url)
        resp.raise_for_status()
        _valid_vs_currencies_cache = set(resp.json())
    return _valid_vs_currencies_cache


def validate_crypto_inputs(
    coin_ids: List[str],
    vs_currencies: List[str]
) -> Tuple[List[str], List[str], List[str], List[str]]:
    valid_coin_ids = get_valid_coin_ids()
    valid_vs_currencies = get_valid_vs_currencies()

    valid_ids = [cid for cid in coin_ids if cid in valid_coin_ids]
    invalid_ids = [cid for cid in coin_ids if cid not in valid_coin_ids]

    valid_vs = [cur.lower()
                for cur in vs_currencies if cur.lower() in valid_vs_currencies]
    invalid_vs = [cur for cur in vs_currencies if cur.lower()
                  not in valid_vs_currencies]

    return valid_ids, valid_vs, invalid_ids, invalid_vs


def validate_and_raise(coin_ids: List[str], vs_currencies: List[str]):
    valid_ids, valid_vs, invalid_ids, invalid_vs = validate_crypto_inputs(
        coin_ids, vs_currencies)

    if not valid_ids and not valid_vs:
        raise HTTPException(status_code=400, detail={
            "error": "No valid coin_id(s) or vs_currenc(y/ies) provided.",
            "invalid_coin_ids": invalid_ids,
            "invalid_vs_currencies": invalid_vs
        })
    if not valid_ids:
        raise HTTPException(status_code=400, detail={
            "error": "No valid coin_id(s) provided.",
            "invalid_coin_ids": invalid_ids
        })
    if not valid_vs:
        raise HTTPException(status_code=400, detail={
            "error": "No valid vs_currenc(y/ies) provided.",
            "invalid_vs_currencies": invalid_vs
        })

    return valid_ids, valid_vs, invalid_ids, invalid_vs
