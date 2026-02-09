"""
Tests for order endpoints
"""

from fastapi.testclient import TestClient

from app.main import app


def test_get_orders():
    """Test getting all orders"""

    with TestClient(app) as client:
        # Request to the endpoint
        response = client.get("orders/")

        # Asserts that the response status code is 200
        assert response.status_code == 200


def test_get_order():
    """Test getting a specific order"""

    with TestClient(app) as client:
        # First, get the list to find a valid ID
        list_response = client.get("/orders")
        orders = list_response.json()

        if orders:
            order_id = orders[0]["id"]
            response = client.get(f"/orders/{order_id}")
            assert response.status_code == 200

        else:
            print("No orders found to test individual GET")


def test_order_statuses():
    """Test order statuses analytics endpoint"""

    with TestClient(app) as client:
        # Request to the new endpoint location
        response = client.get("/orders/statuses")

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
