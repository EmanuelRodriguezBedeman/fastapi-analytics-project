from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.repositories import product_repository
from app.schemas.base import BaseResponse
from app.schemas.product import ProductResponse, RevenueByCategoryResult, TopRevenueResultItem
from app.utils.dependencies import get_db

router = APIRouter()


@router.get("/top-revenue", response_model=BaseResponse[TopRevenueResultItem])
async def get_top_products_by_revenue(
    limit: int = Query(5, gt=0, description="Number of top products to return"),
    country: Optional[str] = Query(None, description="Filter by country"),
    year: Optional[int] = Query(None, description="Filter by year"),
    category: Optional[str] = Query(None, description="Filter by category"),
    db: Session = Depends(get_db),
) -> BaseResponse[TopRevenueResultItem]:
    """Get top products by revenue (delivered orders only)"""
    try:
        results, total_groups = product_repository.get_top_products_by_revenue(
            db, limit=limit, country=country, year=year, category=category
        )

        formatted_results = [
            {
                "product_id": r.id,
                "product_name": r.name,
                "category": r.category,
                "revenue": float(r.revenue) if r.revenue is not None else 0.0,
            }
            for r in results
        ]

        return BaseResponse(
            metadata={
                "requested_at": datetime.now(timezone.utc),
                "currency": "USD",
                "total_groups": total_groups,
                "applied_filters": {
                    "limit": limit,
                    "country": country,
                    "year": year,
                    "category": category,
                },
            },
            results=formatted_results,
        )

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
    "/revenue-by-category",
    response_model=BaseResponse[RevenueByCategoryResult],
    response_model_exclude_none=True,
)
async def get_revenue_category_stats(
    country: Optional[str] = Query(None, description="Filter by country"),
    year: Optional[int] = Query(None, description="Filter by year"),
    metrics: Optional[str] = Query(
        None,
        description="Comma-separated metrics to include: average, median, max",
    ),
    db: Session = Depends(get_db),
) -> BaseResponse[RevenueByCategoryResult]:
    """Get revenue statistics (average, median and max) per product category"""
    try:
        # Determine metrics to include
        include_average = True
        include_median = True
        include_max = True
        requested_metrics = ["average", "median", "max"]

        if metrics:
            requested_metrics = [m.strip().lower() for m in metrics.split(",")]
            include_average = "average" in requested_metrics
            include_median = "median" in requested_metrics
            include_max = "max" in requested_metrics

        results, total_groups = product_repository.get_revenue_statistics_per_category(
            db,
            country=country,
            year=year,
            include_average=include_average,
            include_median=include_median,
            include_max=include_max,
        )

        formatted_results = []
        for r in results:
            item = {"category": r.category if r.category else "Uncategorized"}
            if include_average:
                item["average_revenue"] = (
                    float(r.average_revenue) if r.average_revenue is not None else 0.0
                )
            if include_median:
                item["median_revenue"] = (
                    float(r.median_revenue) if r.median_revenue is not None else 0.0
                )
            if include_max:
                item["max_revenue"] = float(r.max_revenue) if r.max_revenue is not None else 0.0
            formatted_results.append(item)

        return BaseResponse(
            metadata={
                "requested_at": datetime.now(timezone.utc),
                "currency": "USD",
                "total_groups": total_groups,
                "applied_filters": {
                    "country": country,
                    "year": year,
                    "metrics": requested_metrics,
                },
            },
            results=formatted_results,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=BaseResponse[ProductResponse])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, gt=0),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
) -> BaseResponse[ProductResponse]:
    """Get all products"""
    products = product_repository.get_all(db, skip=skip, limit=limit, category=category)
    return BaseResponse(
        metadata={
            "requested_at": datetime.now(timezone.utc),
            "total_groups": len(products),
            "applied_filters": {"skip": skip, "limit": limit, "category": category},
        },
        results=products,
    )


@router.get("/{product_id}", response_model=BaseResponse[ProductResponse])
async def get_product(
    product_id: int, db: Session = Depends(get_db)
) -> BaseResponse[ProductResponse]:
    """Get a specific product by ID"""
    product = product_repository.get_by_id(db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return BaseResponse(
        metadata={
            "requested_at": datetime.now(timezone.utc),
            "total_groups": 1,
            "applied_filters": {"product_id": product_id},
        },
        results=[product],
    )
