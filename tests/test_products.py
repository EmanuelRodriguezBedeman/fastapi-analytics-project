"""
Tests for product endpoints
"""

from fastapi.testclient import TestClient

from app.main import app


def test_get_products():
    """Test getting all products"""
    with TestClient(app) as client:
        response = client.get("/products?skip=0&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert "metadata" in data
        assert "results" in data
        assert data["metadata"]["applied_filters"] == {
            "skip": 0,
            "limit": 10,
            "category": None,
        }


def test_get_product():
    """Test getting a specific product"""
    with TestClient(app) as client:
        # First, get the list to find a valid ID
        list_response = client.get("/products?limit=1")
        products = list_response.json()["results"]

        if products:
            product_id = products[0]["id"]
            response = client.get(f"/products/{product_id}")
            assert response.status_code == 200
            data = response.json()
            assert data["metadata"]["total_groups"] == 1
            assert len(data["results"]) == 1
            assert data["results"][0]["id"] == product_id
        else:
            print("No products found to test individual GET")


def test_top_revenue_products():
    """Test top revenue products endpoint"""
    with TestClient(app) as client:
        response = client.get("/products/top-revenue")
        assert response.status_code == 200
        data = response.json()

        assert "metadata" in data
        assert "results" in data

        metadata = data["metadata"]
        assert "requested_at" in metadata
        assert metadata["currency"] == "USD"
        assert "total_groups" in metadata
        assert metadata["applied_filters"] == {"limit": 5, "country": None, "year": None}

        results = data["results"]
        assert len(results) <= 5


def test_top_revenue_with_filters():
    """Test top revenue products with filters"""
    with TestClient(app) as client:
        # Test with limit
        response = client.get("/products/top-revenue?limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) <= 2
        assert data["metadata"]["applied_filters"]["limit"] == 2

        # Test with invalid limit
        response = client.get("/products/top-revenue?limit=0")
        assert response.status_code == 422
