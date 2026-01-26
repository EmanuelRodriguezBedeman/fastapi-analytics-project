"""
Customer schemas for request/response validation
"""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class CustomerBase(BaseModel):
    """Base customer schema"""
    email: EmailStr
    name: str
    country: Optional[str] = None
    city: Optional[str] = None
    signup_date: Optional[date] = None


class CustomerCreate(CustomerBase):
    """Schema for creating a customer"""
    pass


class CustomerUpdate(BaseModel):
    """Schema for updating a customer"""
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    signup_date: Optional[date] = None


class CustomerResponse(CustomerBase):
    """Schema for customer response"""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
