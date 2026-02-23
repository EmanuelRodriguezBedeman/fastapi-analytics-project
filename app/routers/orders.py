"""
Order router endpoints
"""

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.models.order import OrderStatus
from app.repositories import order_repository
from app.schemas.base import BaseResponse
from app.schemas.order import OrderResponse, OrderStatusBase, SalesGroup
from app.utils.dependencies import get_db

router = APIRouter()


@router.get("/", response_model=BaseResponse[OrderResponse])
async def get_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, gt=0),
    db: Session = Depends(get_db),
) -> BaseResponse[OrderResponse]:
    """Get all orders"""
    orders = order_repository.get_all(db, skip=skip, limit=limit)
    return BaseResponse(
        metadata={
            "requested_at": datetime.now(timezone.utc),
            "total_groups": len(orders),
            "applied_filters": {"skip": skip, "limit": limit},
        },
        results=orders,
    )


@router.get("/statuses", response_model=BaseResponse[OrderStatusBase])
async def get_order_status_counts(
    order_status: Optional[OrderStatus] = Query(None, description="Filter by order status"),
    db: Session = Depends(get_db),
) -> BaseResponse[OrderStatusBase]:
    """Get order counts grouped by status"""
    try:
        results, total_groups = order_repository.get_order_counts_by_status(db, order_status)
        return BaseResponse(
            metadata={
                "requested_at": datetime.now(timezone.utc),
                "total_groups": total_groups,
                "applied_filters": {"order_status": order_status},
            },
            results=[{"status": r.status, "count": r.count} for r in results],
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
    "/sales-summary",
    response_model=BaseResponse[SalesGroup],
    response_model_exclude_none=True,
)
async def get_sales_summary(
    metric: Optional[str] = Query(
        None,
        description="Filter by a specific metric",
        pattern="^(sum|avg|median|max|count)$",
    ),
    country: Optional[str] = Query(None, description="Filter by country"),
    year: Optional[int] = Query(None, description="Filter by year"),
    db: Session = Depends(get_db),
) -> BaseResponse[SalesGroup]:
    """Get sales metrics grouped by country and year (delivered orders only)"""
    results, total_groups = order_repository.get_sales_summary(
        db, metric=metric, country=country, year=year
    )

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

    return BaseResponse(
        metadata={
            "requested_at": datetime.now(timezone.utc),
            "currency": "USD",
            "total_groups": total_groups,
            "applied_filters": {
                "metric": metric,
                "country": country,
                "year": year,
                "status": "delivered",
            },
        },
        results=formatted_results,
    )


@router.get("/{order_id}", response_model=BaseResponse[OrderResponse])
async def get_order(order_id: int, db: Session = Depends(get_db)) -> BaseResponse[OrderResponse]:
    """Get a specific order by ID"""
    order = order_repository.get_by_id(db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return BaseResponse(
        metadata={
            "requested_at": datetime.now(timezone.utc),
            "total_groups": 1,
            "applied_filters": {"order_id": order_id},
        },
        results=[order],
    )
