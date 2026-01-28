"""
FastAPI E-commerce Main Application
"""

from fastapi import FastAPI

from app.routers import customers, orders, products, reviews
from app.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=f"A modern analytics API built with {settings.PROJECT_NAME}",
    version="0.1.0",
)

# Include routers
app.include_router(customers.router, prefix="/api/v1/customers", tags=["customers"])
app.include_router(products.router, prefix="/api/v1/products", tags=["products"])
app.include_router(orders.router, prefix="/api/v1/orders", tags=["orders"])
app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["reviews"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
