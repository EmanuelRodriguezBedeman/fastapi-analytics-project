"""
Customer repository - Database access layer for customers
"""

from sqlalchemy.orm import Session

from app.models.customer import Customer


def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[Customer]:
    """Get all customers with pagination"""
    return db.query(Customer).offset(skip).limit(limit).all()  # type: ignore[return-value]


def get_by_id(db: Session, customer_id: int) -> Customer | None:
    """Get a specific customer by ID"""
    return db.query(Customer).filter(Customer.id == customer_id).first()  # type: ignore[return-value]
