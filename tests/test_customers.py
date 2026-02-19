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


def test_high_value_total_true():
    """Test high value customers endpoint with total=true (default, SUM)"""

    with TestClient(app) as client:
        response = client.get("/customers/high-value")

        assert response.status_code == 200

        customers = response.json()
        assert isinstance(customers, list)
        assert len(customers) <= 5

        if customers:
            # Verify all required fields are present
            expected_fields = ["name", "email", "country", "city", "value"]
            for field in expected_fields:
                assert field in customers[0]

            assert isinstance(customers[0]["value"], (int, float))

            # Verify descending order by value
            values = [c["value"] for c in customers]
            assert values == sorted(values, reverse=True)


def test_high_value_total_false():
    """Test high value customers endpoint with total=false (MAX)"""

    with TestClient(app) as client:
        response = client.get("/customers/high-value?total=false")

        assert response.status_code == 200

        customers = response.json()
        assert isinstance(customers, list)
        assert len(customers) <= 5

        if customers:
            # Verify all required fields are present
            expected_fields = ["name", "email", "country", "city", "value"]
            for field in expected_fields:
                assert field in customers[0]

            assert isinstance(customers[0]["value"], (int, float))

            # Verify descending order by value
            values = [c["value"] for c in customers]
            assert values == sorted(values, reverse=True)


def test_high_value_custom_limit():
    """Test high value customers endpoint with custom limit"""

    with TestClient(app) as client:
        response = client.get("/customers/high-value?limit=3")

        assert response.status_code == 200

        customers = response.json()
        assert isinstance(customers, list)
        assert len(customers) <= 3

        if customers:
            # Verify descending order by value
            values = [c["value"] for c in customers]
            assert values == sorted(values, reverse=True)


def test_customers_per_country():
    """Test customer count per country endpoint"""

    with TestClient(app) as client:
        response = client.get("/customers/per-country")

        assert response.status_code == 200

        counts = response.json()
        assert isinstance(counts, list)

        if counts:
            # Verify all required fields are present
            expected_fields = ["country", "customer_count"]
            for field in expected_fields:
                assert field in counts[0]

            assert isinstance(counts[0]["customer_count"], int)

            # Verify deterministic order by country
            countries = [c["country"] for c in counts if c["country"] is not None]
            assert countries == sorted(countries)
