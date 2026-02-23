from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.repositories import order_item_repository
from app.schemas.base import BaseResponse
from app.schemas.order_item import OrderItemResponse
from app.utils.dependencies import get_db

router = APIRouter()


@router.get("/", response_model=BaseResponse[OrderItemResponse])
async def get_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, gt=0),
    db: Session = Depends(get_db),
) -> BaseResponse[OrderItemResponse]:
    """Get all order items"""
    items = order_item_repository.get_all(db, skip=skip, limit=limit)
    return BaseResponse(
        metadata={
            "requested_at": datetime.now(timezone.utc),
            "total_groups": len(items),
            "applied_filters": {"skip": skip, "limit": limit},
        },
        results=items,
    )


@router.get("/{order_item_id}", response_model=BaseResponse[OrderItemResponse])
async def get_order_item(
    order_item_id: int, db: Session = Depends(get_db)
) -> BaseResponse[OrderItemResponse]:
    """Get a specific order item by ID"""
    item = order_item_repository.get_by_id(db, order_item_id=order_item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order item not found")
    return BaseResponse(
        metadata={
            "requested_at": datetime.now(timezone.utc),
            "total_groups": 1,
            "applied_filters": {"order_item_id": order_item_id},
        },
        results=[item],
    )
