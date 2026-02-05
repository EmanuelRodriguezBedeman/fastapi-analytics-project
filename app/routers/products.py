"""
Product router endpoints
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import product_repository
from app.schemas.product import ProductResponse
from app.utils.dependencies import get_db

router = APIRouter()


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
