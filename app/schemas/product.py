"""
Product schemas for request/response validation
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    """Base product schema"""

    name: str
    description: Optional[str] = None
    price: float
    stock: int = 0
    category: Optional[str] = None


class ProductResponse(ProductBase):
    """Schema for product response"""

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class TopRevenueResultItem(BaseModel):
    """Schema for top revenue result item"""

    product_id: int
    product_name: str
    category: Optional[str] = None
    revenue: float


class TopRevenueFilters(BaseModel):
    """Schema for top revenue filters metadata"""

    limit: int
    country: Optional[str] = None
    year: Optional[int] = None
    category: Optional[str] = None
