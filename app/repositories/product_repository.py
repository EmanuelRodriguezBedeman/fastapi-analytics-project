"""
Product repository - Database access layer for products
"""

from sqlalchemy.orm import Session

from app.models.product import Product


def get_all(
    db: Session, skip: int = 0, limit: int = 100, category: str | None = None
) -> list[Product]:
    """Get all products with optional category filter and pagination"""
    query = db.query(Product)
    if category:
        query = query.filter(Product.category == category)
    return query.offset(skip).limit(limit).all()  # type: ignore[return-value]


def get_by_id(db: Session, product_id: int) -> Product | None:
    """Get a specific product by ID"""
    return db.query(Product).filter(Product.id == product_id).first()  # type: ignore[return-value]
