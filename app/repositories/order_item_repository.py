"""
OrderItem repository - Database access layer for order items
"""

from sqlalchemy.orm import Session

from app.models.order_item import OrderItem


def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[OrderItem]:
    """Get all order items with pagination"""
    return db.query(OrderItem).offset(skip).limit(limit).all()  # type: ignore[return-value]


def get_by_id(db: Session, order_item_id: int) -> OrderItem | None:
    """Get a specific order item by ID"""
    return db.query(OrderItem).filter(OrderItem.id == order_item_id).first()  # type: ignore[return-value]
