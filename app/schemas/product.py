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
