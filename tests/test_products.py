"""
Tests for product endpoints
"""

from fastapi.testclient import TestClient

from app.main import app


def test_get_products():
    """Test getting all products"""

    with TestClient(app) as client:
        # Request to the endpoint
        response = client.get("products/")

        # Asserts that the response status code is 200
        assert response.status_code == 200


def test_get_product():
    """Test getting a specific product"""

    with TestClient(app) as client:
        # First, get the list to find a valid ID
        list_response = client.get("/products")
        products = list_response.json()

        if products:
            product_id = products[0]["id"]
            response = client.get(f"/products/{product_id}")
            assert response.status_code == 200
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

        # Check metadata
        metadata = data["metadata"]
        assert "requested_at" in metadata
        assert metadata["currency"] == "USD"
        assert "total_groups" in metadata
        assert "applied_filters" in metadata

        # Check results
        results = data["results"]
        assert isinstance(results, list)
        assert len(results) <= 5  # default limit

        if results:
            item = results[0]
            assert "product_id" in item
            assert "product_name" in item
            assert "revenue" in item
            assert isinstance(item["revenue"], (int, float))

            # Verify descending order
            revenues = [r["revenue"] for r in results]
            assert revenues == sorted(revenues, reverse=True)


def test_top_revenue_with_filters():
    """Test top revenue products with filters"""
    with TestClient(app) as client:
        # Test with limit
        response = client.get("/products/top-revenue?limit=2")
        assert response.status_code == 200
        assert len(response.json()["results"]) <= 2

        # Test with invalid limit
        response = client.get("/products/top-revenue?limit=0")
        assert response.status_code == 422
