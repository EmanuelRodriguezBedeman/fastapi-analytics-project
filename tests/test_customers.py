"""
Tests for customers endpoints
"""

from fastapi.testclient import TestClient

from app.main import app


def test_get_all_customers():
    """Test getting all customers"""
    with TestClient(app) as client:
        response = client.get("/customers?skip=0&limit=10")
        assert response.status_code == 200
        data = response.json()

        assert "metadata" in data
        assert "results" in data
        assert data["metadata"]["total_groups"] == len(data["results"])
        assert data["metadata"]["applied_filters"] == {"skip": 0, "limit": 10}


def test_get_customer():
    """Test getting a specific customer by ID"""
    with TestClient(app) as client:
        # First, get the list to find a valid ID
        list_response = client.get("/customers?limit=1")
        customers = list_response.json()["results"]

        if customers:
            customer_id = customers[0]["id"]
            response = client.get(f"/customers/{customer_id}")
            assert response.status_code == 200
            data = response.json()
            assert data["metadata"]["total_groups"] == 1
            assert data["metadata"]["applied_filters"] == {"customer_id": customer_id}
            assert len(data["results"]) == 1
            assert data["results"][0]["id"] == customer_id
        else:
            print("No customers found to test individual GET")


def test_most_frequent_default_limit():
    """Test most frequent customers endpoint with default limit (5)"""
    with TestClient(app) as client:
        response = client.get("/customers/most-frequent")
        assert response.status_code == 200
        data = response.json()

        assert "metadata" in data
        assert "results" in data
        assert data["metadata"]["applied_filters"] == {"limit": 5}

        top_customers = data["results"]
        assert isinstance(top_customers, list)
        assert len(top_customers) <= 5

        if top_customers:
            expected_fields = [
                "name",
                "email",
                "country",
                "city",
                "signup_date",
                "purchases_count",
            ]
            for field in expected_fields:
                assert field in top_customers[0]
            counts = [c["purchases_count"] for c in top_customers]
            assert counts == sorted(counts, reverse=True)


def test_most_frequent_custom_limit():
    """Test most frequent customers endpoint with custom limit"""
    with TestClient(app) as client:
        response = client.get("/customers/most-frequent?limit=3")
        assert response.status_code == 200
        data = response.json()
        assert data["metadata"]["applied_filters"] == {"limit": 3}
        assert len(data["results"]) <= 3


def test_high_value_total_true():
    """Test high value customers endpoint with total=true (default, SUM)"""
    with TestClient(app) as client:
        response = client.get("/customers/high-value")
        assert response.status_code == 200
        data = response.json()

        assert data["metadata"]["currency"] == "USD"
        assert data["metadata"]["applied_filters"] == {"total": True, "limit": 5}

        customers = data["results"]
        if customers:
            expected_fields = ["name", "email", "country", "city", "value"]
            for field in expected_fields:
                assert field in customers[0]
            values = [c["value"] for c in customers]
            assert values == sorted(values, reverse=True)


def test_high_value_total_false():
    """Test high value customers endpoint with total=false (MAX)"""
    with TestClient(app) as client:
        response = client.get("/customers/high-value?total=false")
        assert response.status_code == 200
        data = response.json()
        assert data["metadata"]["applied_filters"] == {"total": False, "limit": 5}


def test_customers_per_country():
    """Test customer count per country endpoint with metadata"""
    with TestClient(app) as client:
        response = client.get("/customers/per-country")
        assert response.status_code == 200
        data = response.json()

        assert "metadata" in data
        assert "results" in data
        assert data["metadata"]["total_groups"] == len(data["results"])
        assert "currency" not in data["metadata"]
