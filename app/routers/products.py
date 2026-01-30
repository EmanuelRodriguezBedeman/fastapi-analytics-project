"""
Product router endpoints
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductResponse
from app.utils.dependencies import get_db

router = APIRouter()


@router.get("/", response_model=List[ProductResponse])
async def get_products(
    skip: int = 0, limit: int = 100, category: str = None, db: Session = Depends(get_db)
):
    """Get all products"""
    query = db.query(Product)
    if category:
        query = query.filter(Product.category == category)
    products = query.offset(skip).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product by ID"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product
