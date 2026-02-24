"""
Tests for product category revenue statistics
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.database import SessionLocal
from app.main import app


@pytest.fixture
def sess():
    """Get a database session for testing"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def mock_revenue_data(sess):
    """Seed data for revenue statistics testing (delivered orders only)"""
    # Clean up
    sess.execute(text("DELETE FROM order_items"))
    sess.execute(text("DELETE FROM orders"))
    sess.execute(text("DELETE FROM products"))
    sess.execute(text("DELETE FROM customers"))
    sess.commit()

    # Products
    sess.execute(
        text(
            "INSERT INTO products (id, name, price, category) VALUES "
            "(1, 'P1', 10, 'CatA'), (2, 'P2', 20, 'CatA'), "
            "(3, 'P3', 30, 'CatB'), (4, 'P4', 40, 'CatB')"
        )
    )

    # Customer
    sess.execute(
        text(
            "INSERT INTO customers (id, name, email, country) VALUES (1, 'C1', 'c1@ex.com', 'USA')"
        )
    )

    # Delivered Orders
    # CatA: OI1(10*1=10), OI2(20*2=40) -> Stats: Avg 25, Median 25, Max 40
    # CatB: OI3(30*1=30), OI4(40*1=40), OI5(50*1=50) -> Stats: Avg 40, Median 40, Max 50
    # Note: price in order_items can be different from product table
    sess.execute(
        text(
            "INSERT INTO orders (id, customer_id, total_amount, status, created_at) VALUES "
            "(1, 1, 50, 'delivered', '2024-01-01 10:00:00')"
        )
    )

    sess.execute(
        text(
            "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES "
            "(1, 1, 1, 10), (1, 2, 2, 20), "
            "(1, 3, 1, 30), (1, 4, 1, 40)"
        )
    )

    # Add one more to CatB for median test
    sess.execute(
        text("INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (1, 4, 1, 50)")
    )

    # Non-delivered order (should be ignored)
    sess.execute(
        text(
            "INSERT INTO orders (id, customer_id, total_amount, status, created_at) VALUES "
            "(2, 1, 100, 'pending', '2024-01-01 10:00:00')"
        )
    )
    sess.execute(
        text(
            "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (2, 1, 10, 10)"
        )
    )

    sess.commit()


def test_revenue_by_category_basic(mock_revenue_data):
    """Test basic revenue statistics aggregation"""
    with TestClient(app) as client:
        response = client.get("/products/revenue-by-category")
        assert response.status_code == 200
        data = response.json()

        assert data["metadata"]["total_groups"] == 2
        results = {r["category"]: r for r in data["results"]}

        # CatA: [10, 40] -> Avg 25, Median 25, Max 40
        assert results["CatA"]["average_revenue"] == 25.0
        assert results["CatA"]["median_revenue"] == 25.0
        assert results["CatA"]["max_revenue"] == 40.0

        # CatB: [30, 40, 50] -> Avg 40, Median 40, Max 50
        assert results["CatB"]["average_revenue"] == 40.0
        assert results["CatB"]["median_revenue"] == 40.0
        assert results["CatB"]["max_revenue"] == 50.0


def test_revenue_by_category_metrics_selection(mock_revenue_data):
    """Test selecting specific metrics"""
    with TestClient(app) as client:
        # Only max
        response = client.get("/products/revenue-by-category?metrics=max")
        assert response.status_code == 200
        data = response.json()

        item = data["results"][0]
        assert "max_revenue" in item
        assert "average_revenue" not in item
        assert "median_revenue" not in item
        assert data["metadata"]["applied_filters"]["metrics"] == ["max"]

        # Average and Median
        response = client.get("/products/revenue-by-category?metrics=average,median")
        assert response.status_code == 200
        data = response.json()

        item = data["results"][0]
        assert "average_revenue" in item
        assert "median_revenue" in item
        assert "max_revenue" not in item
        assert set(data["metadata"]["applied_filters"]["metrics"]) == {"average", "median"}


def test_revenue_by_category_metadata():
    """Test metadata correctness"""
    with TestClient(app) as client:
        response = client.get("/products/revenue-by-category")
        assert response.status_code == 200
        data = response.json()

        metadata = data["metadata"]
        assert metadata["currency"] == "USD"
        assert "metrics" in metadata["applied_filters"]
        assert set(metadata["applied_filters"]["metrics"]) == {"average", "median", "max"}


def test_revenue_by_category_empty(sess):
    """Test endpoint with no delivered orders"""
    sess.execute(text("DELETE FROM order_items"))
    sess.execute(text("DELETE FROM orders"))
    sess.commit()

    with TestClient(app) as client:
        response = client.get("/products/revenue-by-category")
        assert response.status_code == 200
        data = response.json()
        assert data["results"] == []
        assert data["metadata"]["total_groups"] == 0
