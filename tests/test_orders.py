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
        # Request to the endpoint
        response = client.get("orders/500")

        # Asserts that the response status code is 200
        assert response.status_code == 200
