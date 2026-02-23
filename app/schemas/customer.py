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


class CustomerResponse(CustomerBase):
    """Schema for customer response"""

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MostFrequentCustomerResponse(BaseModel):
    """Schema for most frequent customer analytics response"""

    name: str
    email: str
    country: Optional[str] = None
    city: Optional[str] = None
    signup_date: Optional[date] = None
    purchases_count: int

    model_config = ConfigDict(from_attributes=True)


class HighValueCustomerResponse(BaseModel):
    """Schema for high value customer analytics response"""

    name: str
    email: str
    country: Optional[str] = None
    city: Optional[str] = None
    value: float

    model_config = ConfigDict(from_attributes=True)


class CustomerCountPerCountry(BaseModel):
    """Schema for customer count per country"""

    country: Optional[str] = None
    customer_count: int

    model_config = ConfigDict(from_attributes=True)
