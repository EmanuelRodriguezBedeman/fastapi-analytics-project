"""
FastAPI E-commerce Main Application
"""

from fastapi import FastAPI

# from app.database import engine, Base
# from app.routers import users, products, orders

# Create database tables
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI E-commerce",
    description="A modern e-commerce API built with FastAPI",
    version="0.1.0",
)

# Include routers
# app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
# app.include_router(products.router, prefix="/api/v1/products", tags=["products"])
# app.include_router(orders.router, prefix="/api/v1/orders", tags=["orders"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to FastAPI E-commerce API"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
