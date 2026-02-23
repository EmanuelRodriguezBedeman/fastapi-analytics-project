from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.repositories import customer_repository
from app.schemas.base import BaseResponse
from app.schemas.customer import (
    CustomerCountPerCountry,
    CustomerResponse,
    HighValueCustomerResponse,
    MostFrequentCustomerResponse,
)
from app.utils.dependencies import get_db

router = APIRouter()


@router.get("/", response_model=BaseResponse[CustomerResponse])
async def get_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, gt=0),
    db: Session = Depends(get_db),
) -> BaseResponse[CustomerResponse]:
    """Get all customers"""
    customers = customer_repository.get_all(db, skip=skip, limit=limit)
    return BaseResponse(
        metadata={
            "requested_at": datetime.now(timezone.utc),
            "total_groups": len(customers),
            "applied_filters": {"skip": skip, "limit": limit},
        },
        results=customers,
    )


@router.get("/per-country", response_model=BaseResponse[CustomerCountPerCountry])
async def get_customer_count_per_country(
    db: Session = Depends(get_db),
) -> BaseResponse[CustomerCountPerCountry]:
    """Get customer counts grouped by country"""
    results, total_groups = customer_repository.get_customer_count_per_country(db)
    return BaseResponse(
        metadata={
            "requested_at": datetime.now(timezone.utc),
            "total_groups": total_groups,
            "applied_filters": {},
        },
        results=[{"country": r.country, "customer_count": r.customer_count} for r in results],
    )


@router.get("/most-frequent", response_model=BaseResponse[MostFrequentCustomerResponse])
async def get_most_frequent_customers(
    limit: int = Query(5, gt=0, description="Number of top customers to return"),
    db: Session = Depends(get_db),
) -> BaseResponse[MostFrequentCustomerResponse]:
    """Get top N customers ordered by total number of purchases"""
    results, total_groups = customer_repository.get_most_frequent(db, limit=limit)
    return BaseResponse(
        metadata={
            "requested_at": datetime.now(timezone.utc),
            "total_groups": total_groups,
            "applied_filters": {"limit": limit},
        },
        results=results,
    )


@router.get("/high-value", response_model=BaseResponse[HighValueCustomerResponse])
async def get_high_value_customers(
    total: bool = Query(
        True,
        description="True: rank by total spending (SUM). False: rank by highest single order (MAX)",
    ),
    limit: int = Query(5, gt=0, description="Number of results to return"),
    db: Session = Depends(get_db),
) -> BaseResponse[HighValueCustomerResponse]:
    """Get customers ranked by monetary value"""
    results, total_groups = customer_repository.get_high_value(db, total=total, limit=limit)
    return BaseResponse(
        metadata={
            "requested_at": datetime.now(timezone.utc),
            "currency": "USD",
            "total_groups": total_groups,
            "applied_filters": {"total": total, "limit": limit},
        },
        results=results,
    )


@router.get("/{customer_id}", response_model=BaseResponse[CustomerResponse])
async def get_customer(
    customer_id: int, db: Session = Depends(get_db)
) -> BaseResponse[CustomerResponse]:
    """Get a specific customer by ID"""
    customer = customer_repository.get_by_id(db, customer_id=customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return BaseResponse(
        metadata={
            "requested_at": datetime.now(timezone.utc),
            "total_groups": 1,
            "applied_filters": {"customer_id": customer_id},
        },
        results=[customer],
    )
