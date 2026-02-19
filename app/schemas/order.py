"""
Order schemas for request/response validation
"""

from datetime import datetime
from typing import List, Optional

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


class SalesMetrics(BaseModel):
    """Schema for sales metrics"""

    average: Optional[float] = None
    max: Optional[float] = None
    median: Optional[float] = None
    sum: Optional[float] = None
    count: int


class SalesGroup(BaseModel):
    """Schema for a single (country, year) results group"""

    country: str
    year: int
    metrics: SalesMetrics


class SalesFilters(BaseModel):
    """Schema for applied filters metadata"""

    country: Optional[str] = None
    year: Optional[int] = None
    status: Optional[str] = None


class SalesMetadata(BaseModel):
    """Schema for response metadata"""

    requested_at: datetime
    last_data_point: Optional[datetime] = None
    currency: str = "USD"
    total_groups: int
    applied_filters: SalesFilters


class SalesSummaryResponse(BaseModel):
    """Main schema for sales summary response"""

    metadata: SalesMetadata
    results: List[SalesGroup]
