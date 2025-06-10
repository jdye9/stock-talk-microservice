from fastapi import FastAPI
from app.routes import crypto_routes, stock_routes

app = FastAPI(title="Stock & Crypto Data API")

# Include routers
app.include_router(stock_routes.router, prefix="/stock", tags=["stock"])
app.include_router(crypto_routes.router, prefix="/crypto", tags=["crypto"])
