"""
Order repository - Database access layer for orders
"""

from sqlalchemy.orm import Session

from app.models.order import Order


def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[Order]:
    """Get all orders with pagination"""
    return db.query(Order).offset(skip).limit(limit).all()  # type: ignore[return-value]


def get_by_id(db: Session, order_id: int) -> Order | None:
    """Get a specific order by ID"""
    return db.query(Order).filter(Order.id == order_id).first()  # type: ignore[return-value]
