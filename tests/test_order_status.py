"""
Tests for order statuses endpoint
"""

from fastapi.testclient import TestClient

from app.main import app


def test_order_statuses():
    """Test order statuses analytics endpoint"""

    with TestClient(app) as client:
        # Request to the endpoint
        response = client.get("/orders_status/")

        # Asserts that the response status code is 200
        assert response.status_code == 200

        order_statuses = response.json()

        # Check that we got a list
        assert isinstance(order_statuses, list)

        if order_statuses:
            # Asserts that the first element contains the expected aggregate fields
            assert "status" in order_statuses[0]
            assert "count" in order_statuses[0]
            assert isinstance(order_statuses[0]["count"], int)
