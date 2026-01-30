"""
Review schemas for request/response validation
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ReviewBase(BaseModel):
    """Base review schema"""

    product_id: int
    customer_id: int
    rating: int  # 1-5
    comment: Optional[str] = None


class ReviewResponse(ReviewBase):
    """Schema for review response"""

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
