"""
FastAPI E-commerce Main Application
"""

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import settings
from app.routers import customers, order_items, orders, products, reviews
from app.utils.dependencies import get_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=f"A modern analytics API built with {settings.PROJECT_NAME}",
    version="0.1.0",
)


# Include routers
app.include_router(customers.router, prefix="/customers", tags=["customers"])
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
app.include_router(order_items.router, prefix="/order_items", tags=["order_items"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}


@app.get("/health", tags=["Health Check"])
async def check_db_health(db: Session = Depends(get_db)):
    """
    Health check endpoint that verifies database connectivity.
    """
    try:
        # We use db.execute(text("SELECT 1")) to check if the DB is responding
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "unhealthy", "database": "disconnected", "error": str(e)},
        )
