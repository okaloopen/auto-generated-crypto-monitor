"""Service layer for cryptocurrency monitoring.

This module defines the CryptoMonitor class, which is responsible for
periodically fetching cryptocurrency price data from a third‑party API
and caching the results. The class uses aiohttp for asynchronous
HTTP requests and exposes synchronous methods for retrieving the
cached data.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import aiohttp

from .models import PriceData


logger = logging.getLogger(__name__)


@dataclass
class CryptoMonitor:
    """Monitor cryptocurrency prices using asynchronous HTTP requests."""

    coins: List[str]
    vs_currency: str = "usd"
    interval: float = 60.0
    _prices: Dict[str, PriceData] = field(default_factory=dict, init=False)

    async def run(self) -> None:
        """Continuously fetch price data at a fixed interval."""
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    await self._update_prices(session)
                except Exception as exc:
                    logger.exception("Error updating prices: %s", exc)
                await asyncio.sleep(self.interval)

    async def _update_prices(self, session: aiohttp.ClientSession) -> None:
        """Fetch latest prices from the external API and update the cache."""
        url = (
            "https://api.coingecko.com/api/v3/simple/price?"
            f"ids={','.join(self.coins)}&vs_currencies={self.vs_currency}"
        )
        logger.debug("Fetching price data from %s", url)
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()
            for coin_id, values in data.items():
                price = values.get(self.vs_currency)
                if price is not None:
                    self._prices[coin_id] = PriceData(
                        coin_id=coin_id, currency=self.vs_currency, price=price
                    )
                    logger.info("Updated %s price to %s %s", coin_id, price, self.vs_currency)

    def get_prices(self) -> List[PriceData]:
        """Return a list of the latest cached price data."""
        return list(self._prices.values())

    def get_price(self, coin_id: str) -> Optional[PriceData]:
        """Return the latest price for a specific coin, if available."""
        return self._prices.get(coin_id)
