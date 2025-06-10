import os

from dotenv import load_dotenv

load_dotenv()

COINGECKO_API_BASE = os.getenv("COINGECKO_API_BASE")
