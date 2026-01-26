"""
User router endpoints
"""

# from sqlalchemy.orm import Session
from typing import List

from fastapi import APIRouter, HTTPException, status

# from app.utils.dependencies import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate

# from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    # db: Session = Depends(get_db)
):
    """Get all users"""
    # users = db.query(User).offset(skip).limit(limit).all()
    # return users
    return []  # Return empty list for now


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):  # db: Session = Depends(get_db)
    """Get a specific user by ID"""
    # user = db.query(User).filter(User.id == user_id).first()
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="User not found"
    #     )
    # return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):  # db: Session = Depends(get_db)
    """Create a new user"""
    # TODO: Implement user creation logic
    # pass
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Database functionality is disabled"
    )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    # db: Session = Depends(get_db)
):
    """Update a user"""
    # TODO: Implement user update logic
    # pass
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Database functionality is disabled"
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):  # db: Session = Depends(get_db)
    """Delete a user"""
    # TODO: Implement user deletion logic
    # pass
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Database functionality is disabled"
    )
