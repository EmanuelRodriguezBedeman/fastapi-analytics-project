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
    metric: Optional[str] = None,
    country: Optional[str] = None,
    year: Optional[int] = None,
):
    """
    Returns a sales summary with aggregated metrics grouped by country and year.
    Only includes 'delivered' orders for data reliability.
    Supported metrics: sum, avg, median, max, count.
    """
    from datetime import datetime, timezone

    # Extract year from created_at
    order_year = extract("year", Order.created_at).label("year")

    # Metrics to calculate
    sum_agg = func.sum(Order.total_amount).label("sum")
    avg_agg = func.avg(Order.total_amount).label("average")
    max_agg = func.max(Order.total_amount).label("max")
    median_agg = func.percentile_cont(0.5).within_group(Order.total_amount).label("median")
    count_agg = func.count(Order.id).label("count")

    # Base query for aggregation - Restricted to 'delivered'
    query = (
        db.query(
            Customer.country.label("country"),
            order_year,
            sum_agg,
            avg_agg,
            max_agg,
            median_agg,
            count_agg,
        )
        .join(Customer, Order.customer_id == Customer.id)
        .filter(Order.status == "delivered")
    )

    # Filters
    if country:
        query = query.filter(Customer.country == country)
    if year:
        query = query.filter(order_year == year)

    # Grouping and Ordering
    results = (
        query.group_by(Customer.country, order_year)
        .order_by(order_year.desc(), sum_agg.desc())
        .all()
    )

    # Calculate last_data_point from the filtered 'delivered' Orders
    filter_query = (
        db.query(func.max(Order.created_at))
        .join(Customer, Order.customer_id == Customer.id)
        .filter(Order.status == "delivered")
    )
    if country:
        filter_query = filter_query.filter(Customer.country == country)
    if year:
        filter_query = filter_query.filter(order_year == year)

    last_data_point = filter_query.scalar()

    # Format the metrics
    formatted_results = []
    for r in results:
        metrics = {"count": int(r.count)}
        metric_map = {
            "sum": ("sum", "sum"),
            "avg": ("average", "average"),
            "median": ("median", "median"),
            "max": ("max", "max"),
        }

        if metric:
            if metric in metric_map:
                key, attr = metric_map[metric]
                metrics[key] = float(getattr(r, attr)) if getattr(r, attr) is not None else 0.0
        else:
            for key, attr in metric_map.values():
                metrics[key] = float(getattr(r, attr)) if getattr(r, attr) is not None else 0.0

        formatted_results.append(
            {
                "country": r.country,
                "year": int(r.year),
                "metrics": metrics,
            }
        )

    return {
        "metadata": {
            "requested_at": datetime.now(timezone.utc),
            "last_data_point": last_data_point,
            "currency": "USD",
            "total_groups": len(formatted_results),
            "applied_filters": {
                "country": country,
                "year": year,
                "status": "delivered",
            },
        },
        "results": formatted_results,
    }
