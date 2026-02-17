"""
Tests for customers endpoints
"""

from fastapi.testclient import TestClient

from app.main import app


def test_get_all_customers():
    """Test getting all customers"""

    with TestClient(app) as client:
        # Request to the endpoint
        response = client.get("/customers")

        # Asserts that the response status code is 200
        assert response.status_code == 200


def test_get_customer():
    """Test getting a specific customer by ID"""

    with TestClient(app) as client:
        # First, get the list to find a valid ID
        list_response = client.get("/customers")
        customers = list_response.json()

        if customers:
            customer_id = customers[0]["id"]
            response = client.get(f"/customers/{customer_id}")
            assert response.status_code == 200
        else:
            # If no customers, just skip or fail with a clear message
            print("No customers found to test individual GET")


def test_most_frequent_default_limit():
    """Test most frequent customers endpoint with default limit (5)"""

    with TestClient(app) as client:
        response = client.get("/customers/most-frequent")

        assert response.status_code == 200

        top_customers = response.json()
        assert isinstance(top_customers, list)
        assert len(top_customers) <= 5

        if top_customers:
            # Verify all required fields are present
            expected_fields = ["name", "email", "country", "city", "signup_date", "purchases_count"]
            for field in expected_fields:
                assert field in top_customers[0]

            assert isinstance(top_customers[0]["purchases_count"], int)

            # Verify descending order by purchases_count
            counts = [c["purchases_count"] for c in top_customers]
            assert counts == sorted(counts, reverse=True)


def test_most_frequent_custom_limit():
    """Test most frequent customers endpoint with custom limit"""

    with TestClient(app) as client:
        response = client.get("/customers/most-frequent?limit=3")

        assert response.status_code == 200

        top_customers = response.json()
        assert isinstance(top_customers, list)
        assert len(top_customers) <= 3

        if top_customers:
            # Verify descending order by purchases_count
            counts = [c["purchases_count"] for c in top_customers]
            assert counts == sorted(counts, reverse=True)
