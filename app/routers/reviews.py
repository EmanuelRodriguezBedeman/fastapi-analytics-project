"""
Review router endpoints
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.review import Review
from app.schemas.review import ReviewResponse
from app.utils.dependencies import get_db

router = APIRouter()


@router.get("/", response_model=List[ReviewResponse])
async def get_reviews(
    skip: int = 0, limit: int = 100, product_id: int = None, db: Session = Depends(get_db)
):
    """Get all reviews, optionally filtered by product"""
    query = db.query(Review)
    if product_id:
        query = query.filter(Review.product_id == product_id)
    reviews = query.offset(skip).limit(limit).all()
    return reviews


@router.get("/{review_id}", response_model=ReviewResponse)
async def get_review(review_id: int, db: Session = Depends(get_db)):
    """Get a specific review by ID"""
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return review
