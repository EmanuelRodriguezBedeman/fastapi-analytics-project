"""
Product repository - Database access layer for products
"""

from typing import Optional

from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.order import Order
from app.models.order_item import OrderItem
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


def get_top_products_by_revenue(
    db: Session,
    limit: int = 5,
    country: Optional[str] = None,
    year: Optional[int] = None,
    category: Optional[str] = None,
):
    """
    Returns top products ranked by revenue.
    Revenue is computed only for 'delivered' orders.
    """
    # CTE for delivered orders
    delivered_orders_cte = (
        db.query(Order.id, Order.customer_id, Order.created_at)
        .filter(Order.status == "delivered")
        .cte("delivered_orders")
    )

    # Base query for revenue aggregation
    revenue_agg = func.sum(OrderItem.quantity * OrderItem.price).label("revenue")

    query = (
        db.query(Product.id, Product.name, Product.category, revenue_agg)
        .join(OrderItem, Product.id == OrderItem.product_id)
        .join(delivered_orders_cte, OrderItem.order_id == delivered_orders_cte.c.id)
    )

    # Optional filters
    if country:
        query = query.join(Customer, delivered_orders_cte.c.customer_id == Customer.id).filter(
            Customer.country == country
        )

    if year:
        query = query.filter(extract("year", delivered_orders_cte.c.created_at) == year)

    if category:
        query = query.filter(Product.category == category)

    # Group by product
    query = query.group_by(Product.id, Product.name, Product.category)

    # Get total groups before limit (safe way for grouped queries)
    total_groups = db.query(query.subquery()).count()

    # Final results with ordering and limit
    results = query.order_by(revenue_agg.desc()).limit(limit).all()

    return results, total_groups


def get_revenue_statistics_per_category(
    db: Session,
    country: Optional[str] = None,
    year: Optional[int] = None,
    include_average: bool = True,
    include_median: bool = True,
    include_max: bool = True,
):
    """
    Returns revenue statistics (avg, median, max) per category.
    Revenue is computed as quantity * price per order line from 'delivered' orders.
    """
    # CTE for delivered orders
    delivered_orders = (
        db.query(Order.id, Order.customer_id, Order.created_at)
        .filter(Order.status == "delivered")
        .cte("delivered_orders")
    )

    revenue_expr = OrderItem.quantity * OrderItem.price

    # Prepare selection
    selected_cols = [Product.category.label("category")]
    if include_average:
        selected_cols.append(func.avg(revenue_expr).label("average_revenue"))
    if include_median:
        selected_cols.append(
            func.percentile_cont(0.5).within_group(revenue_expr).label("median_revenue")
        )
    if include_max:
        selected_cols.append(func.max(revenue_expr).label("max_revenue"))

    query = (
        db.query(*selected_cols)
        .join(OrderItem, Product.id == OrderItem.product_id)
        .join(delivered_orders, OrderItem.order_id == delivered_orders.c.id)
    )

    # Optional filters
    if country:
        query = query.join(Customer, delivered_orders.c.customer_id == Customer.id).filter(
            Customer.country == country
        )

    if year:
        query = query.filter(extract("year", delivered_orders.c.created_at) == year)

    query = query.group_by(Product.category)

    # Get total groups
    total_groups = db.query(query.subquery()).count()

    # Get results
    results = query.all()

    return results, total_groups
