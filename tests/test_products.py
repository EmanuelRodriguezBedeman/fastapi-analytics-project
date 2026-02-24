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
        assert metadata["applied_filters"] == {
            "limit": 5,
            "country": None,
            "year": None,
            "category": None,
        }

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
        assert "category" in data["metadata"]["applied_filters"]

        # Test with invalid limit
        response = client.get("/products/top-revenue?limit=0")
        assert response.status_code == 422


def test_top_revenue_category_filter():
    """Test top revenue products with category filter"""
    with TestClient(app) as client:
        # 1. Get a valid category from general products list
        list_res = client.get("/products?limit=10")
        products = list_res.json()["results"]
        if not products:
            return

        target_category = products[0]["category"]

        # 2. Test specific category
        res = client.get(f"/products/top-revenue?category={target_category}")
        assert res.status_code == 200
        data = res.json()
        assert data["metadata"]["applied_filters"]["category"] == target_category

        # 3. Test category="any" (should be null in metadata)
        res_any = client.get("/products/top-revenue?category=any")
        assert res_any.status_code == 200
        data_any = res_any.json()
        assert data_any["metadata"]["applied_filters"]["category"] is None

        # 4. Test combined filters (category + country)
        res_comb = client.get(f"/products/top-revenue?category={target_category}&limit=3")
        assert res_comb.status_code == 200
        data_comb = res_comb.json()
        assert data_comb["metadata"]["applied_filters"]["category"] == target_category
        assert data_comb["metadata"]["applied_filters"]["limit"] == 3
        assert len(data_comb["results"]) <= 3
