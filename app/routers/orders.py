"""
Order router endpoints
"""

# from sqlalchemy.orm import Session
from typing import List

from fastapi import APIRouter, HTTPException, status

# from app.utils.dependencies import get_db
from app.schemas.order import OrderCreate, OrderResponse, OrderUpdate

# from app.models.order import Order

router = APIRouter()


@router.get("/", response_model=List[OrderResponse])
async def get_orders(
    skip: int = 0,
    limit: int = 100,
    # db: Session = Depends(get_db)
):
    """Get all orders"""
    # orders = db.query(Order).offset(skip).limit(limit).all()
    # return orders
    return []  # Return empty list for now


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int):  # db: Session = Depends(get_db)
    """Get a specific order by ID"""
    # order = db.query(Order).filter(Order.id == order_id).first()
    # if not order:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Order not found"
    #     )
    # return order
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate):  # db: Session = Depends(get_db)
    """Create a new order"""
    # TODO: Implement order creation logic
    # pass
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Database functionality is disabled"
    )


@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: int,
    order_update: OrderUpdate,
    # db: Session = Depends(get_db)
):
    """Update an order"""
    # TODO: Implement order update logic
    # pass
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Database functionality is disabled"
    )


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int):  # db: Session = Depends(get_db)
    """Delete an order"""
    # TODO: Implement order deletion logic
    # pass
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Database functionality is disabled"
    )
