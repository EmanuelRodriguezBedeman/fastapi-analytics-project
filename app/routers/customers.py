"""
Customer router endpoints
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.repositories import customer_repository
from app.schemas.customer import (
    CustomerResponse,
    HighValueCustomerResponse,
    MostFrequentCustomerResponse,
)
from app.utils.dependencies import get_db

router = APIRouter()


@router.get("/", response_model=List[CustomerResponse])
async def get_customers(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[CustomerResponse]:
    """Get all customers"""
    customers = customer_repository.get_all(db, skip=skip, limit=limit)
    return customers  # type: ignore[return-value]


@router.get("/most-frequent", response_model=List[MostFrequentCustomerResponse])
async def get_most_frequent_customers(
    limit: int = Query(5, gt=0, description="Number of top customers to return"),
    db: Session = Depends(get_db),
) -> List[MostFrequentCustomerResponse]:
    """Get top N customers ordered by total number of purchases"""
    return customer_repository.get_most_frequent(db, limit=limit)  # type: ignore[return-value]


@router.get("/high-value", response_model=List[HighValueCustomerResponse])
async def get_high_value_customers(
    total: bool = Query(
        True,
        description="True: rank by total spending (SUM). False: rank by highest single order (MAX)",
    ),
    db: Session = Depends(get_db),
) -> List[HighValueCustomerResponse]:
    """Get customers ranked by monetary value"""
    return customer_repository.get_high_value(db, total=total)  # type: ignore[return-value]


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(customer_id: int, db: Session = Depends(get_db)) -> CustomerResponse:
    """Get a specific customer by ID"""
    customer = customer_repository.get_by_id(db, customer_id=customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer  # type: ignore[return-value]
