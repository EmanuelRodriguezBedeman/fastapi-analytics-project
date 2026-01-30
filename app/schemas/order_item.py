"""
Order Item schemas for request/response validation
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OrderItemBase(BaseModel):
    """Base order item schema"""

    product_id: int
    quantity: int
    price: float


class OrderItemCreate(OrderItemBase):
    """Schema for creating an order item"""

    pass


class OrderItemResponse(OrderItemBase):
    """Schema for order item response"""

    id: int
    order_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
