"""
User schemas for request/response validation
"""

# from pydantic import BaseModel, EmailStr
# from datetime import datetime
# from typing import Optional


# class UserBase(BaseModel):
#     """Base user schema"""
#     email: EmailStr
#     username: str
#     full_name: Optional[str] = None


# class UserCreate(UserBase):
#     """Schema for creating a user"""
#     password: str


# class UserUpdate(BaseModel):
#     """Schema for updating a user"""
#     email: Optional[EmailStr] = None
#     username: Optional[str] = None
#     full_name: Optional[str] = None
#     password: Optional[str] = None


# class UserResponse(UserBase):
#     """Schema for user response"""
#     id: int
#     is_active: bool
#     is_superuser: bool
#     created_at: datetime
#     updated_at: Optional[datetime] = None

#     class Config:
#         from_attributes = True
