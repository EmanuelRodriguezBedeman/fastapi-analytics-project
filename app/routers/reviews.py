from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.repositories import review_repository
from app.schemas.base import BaseResponse
from app.schemas.review import ReviewResponse
from app.utils.dependencies import get_db

router = APIRouter()


@router.get("/", response_model=BaseResponse[ReviewResponse])
async def get_reviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, gt=0),
    product_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
) -> BaseResponse[ReviewResponse]:
    """Get all reviews, optionally filtered by product"""
    reviews = review_repository.get_all(db, skip=skip, limit=limit, product_id=product_id)
    return BaseResponse(
        metadata={
            "requested_at": datetime.now(timezone.utc),
            "total_groups": len(reviews),
            "applied_filters": {"skip": skip, "limit": limit, "product_id": product_id},
        },
        results=reviews,
    )


@router.get("/{review_id}", response_model=BaseResponse[ReviewResponse])
async def get_review(review_id: int, db: Session = Depends(get_db)) -> BaseResponse[ReviewResponse]:
    """Get a specific review by ID"""
    review = review_repository.get_by_id(db, review_id=review_id)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return BaseResponse(
        metadata={
            "requested_at": datetime.now(timezone.utc),
            "total_groups": 1,
            "applied_filters": {"review_id": review_id},
        },
        results=[review],
    )
