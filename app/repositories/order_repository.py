"""
Order repository - Database access layer for orders
"""

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.order import Order


def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[Order]:
    """Get all orders with pagination"""
    return db.query(Order).offset(skip).limit(limit).all()  # type: ignore[return-value]


def get_by_id(db: Session, order_id: int) -> Order | None:
    """Get a specific order by ID"""
    return db.query(Order).filter(Order.id == order_id).first()  # type: ignore[return-value]


def get_order_counts_by_status(db: Session, order_status: str):
    """
    Groups orders by status and counts them
    """
    if not order_status:
        return (
            db.query(Order.status, func.count(Order.status).label("count"))
            .group_by(Order.status)
            .all()
        )
    return (
        db.query(Order.status, func.count(Order.status).label("count"))
        .filter(Order.status == order_status)
        .group_by(Order.status)
        .all()
    )


def get_top_buyers(db: Session, limit: int = 5):
    """
    Returns top N customers ordered by total number of purchases (descending).
    """
    return (
        db.query(
            Customer.name,
            Customer.email,
            Customer.country,
            Customer.city,
            Customer.signup_date,
            func.count(Order.id).label("purchases_count"),
        )
        .join(Order, Customer.id == Order.customer_id)
        .group_by(Customer.id)
        .order_by(func.count(Order.id).desc())
        .limit(limit)
        .all()
    )
