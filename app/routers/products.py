from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.repositories import product_repository
from app.schemas.product import ProductResponse, TopRevenueResponse
from app.utils.dependencies import get_db

router = APIRouter()


@router.get("/top-revenue", response_model=TopRevenueResponse)
async def get_top_products_by_revenue(
    limit: int = Query(5, gt=0, description="Number of top products to return"),
    country: Optional[str] = Query(None, description="Filter by country"),
    year: Optional[int] = Query(None, description="Filter by year"),
    db: Session = Depends(get_db),
) -> TopRevenueResponse:
    """Get top products by revenue (delivered orders only)"""
    try:
        data = product_repository.get_top_products_by_revenue(
            db, limit=limit, country=country, year=year
        )

        return TopRevenueResponse(
            metadata={
                "requested_at": datetime.now(timezone.utc),
                "currency": "USD",
                "total_groups": data["total_groups"],
                "applied_filters": {
                    "limit": limit,
                    "country": country,
                    "year": year,
                },
            },
            results=data["results"],
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[ProductResponse])
async def get_products(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
) -> List[ProductResponse]:
    """Get all products"""
    products = product_repository.get_all(db, skip=skip, limit=limit, category=category)
    return products  # type: ignore[return-value]


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)) -> ProductResponse:
    """Get a specific product by ID"""
    product = product_repository.get_by_id(db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product  # type: ignore[return-value]
