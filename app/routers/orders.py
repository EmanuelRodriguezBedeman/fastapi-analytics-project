"""
Order router endpoints
"""

from typing import List, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.models.order import OrderStatus
from app.repositories import order_repository
from app.schemas.order import OrderResponse, OrderStatusBase, SalesSummaryResponse
from app.utils.dependencies import get_db

router = APIRouter()


@router.get("/", response_model=List[OrderResponse])
async def get_orders(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[OrderResponse]:
    """Get all orders"""
    orders = order_repository.get_all(db, skip=skip, limit=limit)
    return orders  # type: ignore[return-value]


@router.get("/statuses", response_model=List[OrderStatusBase])
async def get_order_status_counts(
    order_status: Optional[OrderStatus] = Query(None, description="Filter by order status"),
    db: Session = Depends(get_db),
) -> List[OrderStatusBase]:
    """Get order counts grouped by status"""
    try:
        return order_repository.get_order_counts_by_status(db, order_status)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/sales-summary", response_model=SalesSummaryResponse, response_model_exclude_none=True)
async def get_sales_summary(
    metric: Optional[Literal["sum", "avg", "median", "max"]] = Query(
        None, description="Specific metric to return (sum, avg, median, max)"
    ),
    country: Optional[str] = Query(None, description="Filter by country"),
    year: Optional[int] = Query(None, description="Filter by year"),
    db: Session = Depends(get_db),
) -> SalesSummaryResponse:
    """Get sales summary aggregated by country and year (Delivered orders only)"""
    try:
        return order_repository.get_sales_summary(db, metric, country, year)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: Session = Depends(get_db)) -> OrderResponse:
    """Get a specific order by ID"""
    order = order_repository.get_by_id(db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order  # type: ignore[return-value]
