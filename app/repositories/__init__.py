"""
Repository modules for database access
"""

from app.repositories import (
    customer_repository,
    order_item_repository,
    order_repository,
    product_repository,
    review_repository,
)

__all__ = [
    "customer_repository",
    "product_repository",
    "order_repository",
    "review_repository",
    "order_item_repository",
]
