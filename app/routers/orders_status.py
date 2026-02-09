"""
Order Status router endpoints
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.models.order import OrderStatus
from app.repositories import order_status_repository
from app.schemas.orders_status import OrderStatusBase
from app.utils.dependencies import get_db

router = APIRouter()


@router.get("/", response_model=List[OrderStatusBase])
async def get_order_statuses(
    order_status: Optional[OrderStatus] = Query(None, description="Filter by order status"),
    db: Session = Depends(get_db),
) -> List[OrderStatusBase]:
    """Get all order statuses"""
    try:
        order_statuses = order_status_repository.get_order_counts_by_status(db, order_status)
        return order_statuses
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
