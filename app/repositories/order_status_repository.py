"""
Order Status repository - Database access layer for order statuses
"""

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.order import Order


def get_order_counts_by_status(db: Session):
    """
    Groups orders by status and counts them.
    Corresponds to: SELECT status, COUNT(status) FROM orders GROUP BY status;
    """
    return (
        db.query(Order.status, func.count(Order.status).label("count")).group_by(Order.status).all()
    )
