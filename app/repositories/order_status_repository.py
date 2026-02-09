"""
Order Status repository - Database access layer for order statuses
"""

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.order import Order


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
