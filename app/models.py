"""Pydantic models for the cryptocurrency monitor API."""

from pydantic import BaseModel


class PriceData(BaseModel):
    """Represents the price information for a single cryptocurrency."""

    coin_id: str
    currency: str
    price: float
