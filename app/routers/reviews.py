"""
Review router endpoints
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import review_repository
from app.schemas.review import ReviewResponse
from app.utils.dependencies import get_db

router = APIRouter()


@router.get("/", response_model=List[ReviewResponse])
async def get_reviews(
    skip: int = 0,
    limit: int = 100,
    product_id: Optional[int] = None,
    db: Session = Depends(get_db),
) -> List[ReviewResponse]:
    """Get all reviews, optionally filtered by product"""
    reviews = review_repository.get_all(db, skip=skip, limit=limit, product_id=product_id)
    return reviews  # type: ignore[return-value]


@router.get("/{review_id}", response_model=ReviewResponse)
async def get_review(review_id: int, db: Session = Depends(get_db)) -> ReviewResponse:
    """Get a specific review by ID"""
    review = review_repository.get_by_id(db, review_id=review_id)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return review  # type: ignore[return-value]
