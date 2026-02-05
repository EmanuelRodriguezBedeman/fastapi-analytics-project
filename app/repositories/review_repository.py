"""
Review repository - Database access layer for reviews
"""

from sqlalchemy.orm import Session

from app.models.review import Review


def get_all(
    db: Session, skip: int = 0, limit: int = 100, product_id: int | None = None
) -> list[Review]:
    """Get all reviews with optional product filter and pagination"""
    query = db.query(Review)
    if product_id:
        query = query.filter(Review.product_id == product_id)
    return query.offset(skip).limit(limit).all()  # type: ignore[return-value]


def get_by_id(db: Session, review_id: int) -> Review | None:
    """Get a specific review by ID"""
    return db.query(Review).filter(Review.id == review_id).first()  # type: ignore[return-value]
