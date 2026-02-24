from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.repositories import product_repository
from app.schemas.base import BaseResponse
from app.schemas.product import ProductResponse, TopRevenueResultItem
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
        # Normalize category: None or "any" means no filter
        repo_category = category
        if repo_category and repo_category.lower() == "any":
            repo_category = None

        results, total_groups = product_repository.get_top_products_by_revenue(
            db, limit=limit, country=country, year=year, category=repo_category
        )

        formatted_results = [
            {
                "product_id": r.id,
                "product_name": r.name,
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
                    "category": repo_category if repo_category else None,
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
