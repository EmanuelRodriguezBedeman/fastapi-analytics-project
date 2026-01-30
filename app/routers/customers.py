"""
Customer router endpoints
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import CustomerResponse
from app.utils.dependencies import get_db

router = APIRouter()


@router.get("/", response_model=List[CustomerResponse])
async def get_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all customers"""
    customers = db.query(Customer).offset(skip).limit(limit).all()
    return customers


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """Get a specific customer by ID"""
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer
