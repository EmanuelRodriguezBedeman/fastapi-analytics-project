"""
Customer repository - Database access layer for customers
"""

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.order import Order


def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[Customer]:
    """Get all customers with pagination"""
    return db.query(Customer).offset(skip).limit(limit).all()  # type: ignore[return-value]


def get_by_id(db: Session, customer_id: int) -> Customer | None:
    """Get a specific customer by ID"""
    return db.query(Customer).filter(Customer.id == customer_id).first()  # type: ignore[return-value]


def get_most_frequent(db: Session, limit: int = 5):
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
