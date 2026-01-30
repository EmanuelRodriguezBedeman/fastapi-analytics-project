"""
Order_item router endpoints
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.order_item import OrderItem
from app.schemas.order_item import OrderItemResponse
from app.utils.dependencies import get_db

router = APIRouter()


@router.get("/", response_model=List[OrderItemResponse])
async def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all orders"""
    orders = db.query(OrderItem).offset(skip).limit(limit).all()
    return orders


@router.get("/{order_id}", response_model=OrderItemResponse)
async def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get a specific order by ID"""
    order = db.query(OrderItem).filter(OrderItem.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order
