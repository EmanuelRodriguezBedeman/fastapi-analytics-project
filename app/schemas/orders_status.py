"""
Order Status schema for request/response validation
"""

from pydantic import BaseModel, ConfigDict


class OrderStatusBase(BaseModel):
    """Base order status schema"""

    status: str
    count: int

    model_config = ConfigDict(from_attributes=True)
