"""
Order schemas for request/response validation
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.order import OrderStatus


class OrderBase(BaseModel):
    """Base order schema"""

    shipping_address: str


class OrderResponse(OrderBase):
    """Schema for order response"""

    id: int
    customer_id: int
    total_amount: float
    status: OrderStatus
    created_at: datetime
    updated_at: Optional[datetime] = None


class OrderStatusBase(BaseModel):
    """Base order status schema"""

    status: str
    count: int

    model_config = ConfigDict(from_attributes=True)


class SalesSummaryResponse(BaseModel):
    """Schema for sales summary response"""

    country: str
    year: int
    aggregation: str
    value: float

    model_config = ConfigDict(from_attributes=True)
