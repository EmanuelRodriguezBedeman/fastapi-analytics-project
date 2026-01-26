"""
Product router endpoints
"""

# from sqlalchemy.orm import Session
from typing import List

from fastapi import APIRouter, HTTPException, status

# from app.utils.dependencies import get_db
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

# from app.models.product import Product

router = APIRouter()


@router.get("/", response_model=List[ProductResponse])
async def get_products(
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    # db: Session = Depends(get_db)
):
    """Get all products"""
    # query = db.query(Product)
    # if category:
    #     query = query.filter(Product.category == category)
    # products = query.offset(skip).limit(limit).all()
    # return products
    return []  # Return empty list for now


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int):  # db: Session = Depends(get_db)
    """Get a specific product by ID"""
    # product = db.query(Product).filter(Product.id == product_id).first()
    # if not product:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Product not found"
    #     )
    # return product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):  # db: Session = Depends(get_db)
    """Create a new product"""
    # TODO: Implement product creation logic
    # pass
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Database functionality is disabled"
    )


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    # db: Session = Depends(get_db)
):
    """Update a product"""
    # TODO: Implement product update logic
    # pass
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Database functionality is disabled"
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int):  # db: Session = Depends(get_db)
    """Delete a product"""
    # TODO: Implement product deletion logic
    # pass
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Database functionality is disabled"
    )
