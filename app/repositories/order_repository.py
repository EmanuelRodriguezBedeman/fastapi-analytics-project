"""
Order repository - Database access layer for orders
"""

from typing import Optional

from sqlalchemy import extract, func
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


def get_sales_summary(
    db: Session,
    aggregation: str = "avg",
    country: Optional[str] = None,
    year: Optional[int] = None,
):
    """
    Returns a sales summary aggregated by country and year.
    Supported aggregations: avg, max, median.
    """
    # Extract year from created_at
    order_year = extract("year", Order.created_at).label("year")

    # Define the aggregation column
    if aggregation == "avg":
        agg_func = func.avg(Order.total_amount)
    elif aggregation == "max":
        agg_func = func.max(Order.total_amount)
    elif aggregation == "median":
        # PostgreSQL specific median calculation using percentile_cont
        agg_func = func.percentile_cont(0.5).within_group(Order.total_amount)
    else:
        raise ValueError(f"Unsupported aggregation: {aggregation}")

    query = db.query(
        Customer.country.label("country"),
        order_year,
        agg_func.label("value"),
    ).join(Customer, Order.customer_id == Customer.id)

    if country:
        query = query.filter(Customer.country == country)
    if year:
        query = query.filter(order_year == year)

    results = query.group_by(Customer.country, order_year).all()

    # Format the results to match the schema
    return [
        {
            "country": r.country,
            "year": int(r.year),
            "aggregation": aggregation,
            "value": float(r.value) if r.value is not None else 0.0,
        }
        for r in results
    ]
