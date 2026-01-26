"""
Database models
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.product import Product
    from app.models.order import Order

# Import models for Alembic
from app.models.user import User
from app.models.product import Product
from app.models.order import Order

# Import OrderStatus enum (doesn't require database)
from app.models.order import OrderStatus

__all__ = ["User", "Product", "Order", "OrderStatus"]
