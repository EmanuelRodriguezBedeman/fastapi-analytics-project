"""
Order schemas for request/response validation
"""

# from pydantic import BaseModel
# from datetime import datetime
# from typing import Optional
# from app.models.order import OrderStatus


# class OrderBase(BaseModel):
#     """Base order schema"""
#     shipping_address: str


# class OrderCreate(OrderBase):
#     """Schema for creating an order"""
#     pass


# class OrderUpdate(BaseModel):
#     """Schema for updating an order"""
#     status: Optional[OrderStatus] = None
#     shipping_address: Optional[str] = None


# class OrderResponse(OrderBase):
#     """Schema for order response"""
#     id: int
#     user_id: int
#     total_amount: float
#     status: OrderStatus
#     created_at: datetime
#     updated_at: Optional[datetime] = None

#     class Config:
#         from_attributes = True
