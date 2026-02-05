"""
Order router endpoints
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import order_repository
from app.schemas.order import OrderResponse
from app.utils.dependencies import get_db

router = APIRouter()


@router.get("/", response_model=List[OrderResponse])
async def get_orders(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[OrderResponse]:
    """Get all orders"""
    orders = order_repository.get_all(db, skip=skip, limit=limit)
    return orders  # type: ignore[return-value]


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: Session = Depends(get_db)) -> OrderResponse:
    """Get a specific order by ID"""
    order = order_repository.get_by_id(db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order  # type: ignore[return-value]
