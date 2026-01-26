"""
Pydantic schemas for request/response validation
"""

from app.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from app.schemas.order import OrderCreate, OrderResponse, OrderUpdate
from app.schemas.order_item import OrderItemCreate, OrderItemResponse
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.schemas.review import ReviewCreate, ReviewResponse, ReviewUpdate

__all__ = [
    "CustomerCreate",
    "CustomerUpdate",
    "CustomerResponse",
    "ProductCreate",
    "ProductUpdate",
    "ProductResponse",
    "OrderCreate",
    "OrderUpdate",
    "OrderResponse",
    "ReviewCreate",
    "ReviewUpdate",
    "ReviewResponse",
    "OrderItemCreate",
    "OrderItemResponse",
]
