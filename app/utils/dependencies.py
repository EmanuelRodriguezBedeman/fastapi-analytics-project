"""
FastAPI dependencies
"""

from fastapi import HTTPException, status

# from sqlalchemy.orm import Session

# from app.database import get_db as get_database_session
# from app.models.user import User
# from app.services.auth import AuthService


def get_db():
    """
    Dependency to get database session
    """
    # return next(get_database_session())
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Database functionality is disabled"
    )


# async def get_current_user(
#     token: str,
#     db: Session = Depends(get_db)
# ) -> User:
#     """
#     Dependency to get current authenticated user
#
#     Args:
#         token: JWT token from request
#         db: Database session
#
#     Returns:
#         User: Current authenticated user
#
#     Raises:
#         HTTPException: If token is invalid or user not found
#     """
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#
#     payload = AuthService.verify_token(token)
#     if payload is None:
#         raise credentials_exception
#
#     user_id: int = payload.get("sub")
#     if user_id is None:
#         raise credentials_exception
#
#     user = db.query(User).filter(User.id == user_id).first()
#     if user is None:
#         raise credentials_exception
#
#     return user


# async def get_current_active_user(
#     current_user: User = Depends(get_current_user)
# ) -> User:
#     """
#     Dependency to get current active user
#
#     Args:
#         current_user: Current user from get_current_user
#
#     Returns:
#         User: Active user
#
#     Raises:
#         HTTPException: If user is inactive
#     """
#     if not current_user.is_active:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Inactive user"
#         )
#     return current_user
