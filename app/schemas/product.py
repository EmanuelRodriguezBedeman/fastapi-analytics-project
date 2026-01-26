"""
Product schemas for request/response validation
"""

# from pydantic import BaseModel
# from datetime import datetime
# from typing import Optional


# class ProductBase(BaseModel):
#     """Base product schema"""
#     name: str
#     description: Optional[str] = None
#     price: float
#     stock: int = 0
#     category: Optional[str] = None
#     image_url: Optional[str] = None


# class ProductCreate(ProductBase):
#     """Schema for creating a product"""
#     pass


# class ProductUpdate(BaseModel):
#     """Schema for updating a product"""
#     name: Optional[str] = None
#     description: Optional[str] = None
#     price: Optional[float] = None
#     stock: Optional[int] = None
#     category: Optional[str] = None
#     image_url: Optional[str] = None
#     is_active: Optional[bool] = None


# class ProductResponse(ProductBase):
#     """Schema for product response"""
#     id: int
#     is_active: bool
#     created_at: datetime
#     updated_at: Optional[datetime] = None

#     class Config:
#         from_attributes = True
