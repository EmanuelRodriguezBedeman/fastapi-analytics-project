"""
Order router endpoints
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.models.order import OrderStatus
from app.repositories import order_repository
from app.schemas.order import OrderResponse, OrderStatusBase, TopBuyerResponse
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


@router.get("/top_buyers", response_model=List[TopBuyerResponse])
async def get_top_buyers(
    limit: int = Query(5, gt=0, description="Number of top buyers to return"),
    db: Session = Depends(get_db),
) -> List[TopBuyerResponse]:
    """Get top N customers ordered by total number of purchases"""
    return order_repository.get_top_buyers(db, limit=limit)  # type: ignore[return-value]


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: Session = Depends(get_db)) -> OrderResponse:
    """Get a specific order by ID"""
    order = order_repository.get_by_id(db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order  # type: ignore[return-value]
