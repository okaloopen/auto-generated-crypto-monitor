"""Main entry point for the asynchronous cryptocurrency monitor API.

This module configures and runs a FastAPI application that exposes
REST endpoints for retrieving cryptocurrency price data. The data is
fetched asynchronously from a third‑party API using aiohttp. A
background task periodically updates the cached prices.
"""

import asyncio
import logging
from typing import Dict, List

from fastapi import FastAPI, HTTPException

from .models import PriceData
from .services import CryptoMonitor


# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title="Asynchronous Crypto Monitor", version="0.1.0")
    monitor = CryptoMonitor(
        coins=["bitcoin", "ethereum"], vs_currency="usd", interval=30.0
    )

    @app.on_event("startup")
    async def startup_event() -> None:
        """Start the background price fetching task on startup."""
        logger.info("Starting crypto monitor background task")
        asyncio.create_task(monitor.run())

    @app.get("/prices", response_model=List[PriceData])
    async def get_prices() -> List[PriceData]:
        """Return the latest cached price data for the monitored coins."""
        prices = monitor.get_prices()
        if not prices:
            raise HTTPException(status_code=503, detail="Price data not available yet")
        return prices

    @app.get("/prices/{coin_id}", response_model=PriceData)
    async def get_price(coin_id: str) -> PriceData:
        """Return the latest price for a specific coin."""
        price = monitor.get_price(coin_id)
        if price is None:
            raise HTTPException(status_code=404, detail="Coin not found")
        return price

    return app


app = create_app()
