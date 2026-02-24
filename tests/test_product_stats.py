"""
Tests for product category revenue statistics
"""

from fastapi.testclient import TestClient

from app.main import app


def test_revenue_by_category_basic():
    """
    Test revenue statistics aggregation using existing data.
    Does not insert, update, or delete records.
    """
    with TestClient(app) as client:
        response = client.get("/products/revenue-by-category")
        assert response.status_code == 200
        data = response.json()

        assert "metadata" in data
        assert "results" in data
        # We check structure and basic sanity, not exact values, to avoid dependencies on seed data
        assert data["metadata"]["currency"] == "USD"

        if data["results"]:
            group = data["results"][0]
            assert "category" in group
            # Check for default metrics
            assert "average_revenue" in group
            assert "median_revenue" in group
            assert "max_revenue" in group


def test_revenue_by_category_metrics_selection():
    """
    Test metric selection query parameter.
    Does not insert, update, or delete records.
    """
    with TestClient(app) as client:
        # Request only max_revenue
        response = client.get("/products/revenue-by-category?metrics=max")
        assert response.status_code == 200
        data = response.json()

        if data["results"]:
            item = data["results"][0]
            assert "max_revenue" in item
            assert "average_revenue" not in item
            assert "median_revenue" not in item

        assert data["metadata"]["applied_filters"]["metrics"] == ["max"]


def test_revenue_by_category_metadata():
    """
    Test metadata structure.
    Does not insert, update, or delete records.
    """
    with TestClient(app) as client:
        response = client.get("/products/revenue-by-category")
        assert response.status_code == 200
        data = response.json()

        metadata = data["metadata"]
        assert "requested_at" in metadata
        assert metadata["currency"] == "USD"
        assert "total_groups" in metadata
        assert "applied_filters" in metadata
        assert "metrics" in metadata["applied_filters"]
