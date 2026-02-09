"""
Order Status router endpoints
"""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.repositories import order_status_repository
from app.schemas.orders_status import OrderStatusBase
from app.utils.dependencies import get_db

router = APIRouter()


@router.get("/", response_model=List[OrderStatusBase])
async def get_order_statuses(db: Session = Depends(get_db)) -> List[OrderStatusBase]:
    """Get all order statuses"""
    order_statuses = order_status_repository.get_order_counts_by_status(db)
    return order_statuses  # type: ignore[return-value]
