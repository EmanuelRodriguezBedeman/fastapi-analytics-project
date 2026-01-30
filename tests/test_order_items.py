"""
Tests for order_items endpoints
"""

from fastapi.testclient import TestClient

from app.main import app


def test_get_order_items():
    """Test getting all order_items"""
    with TestClient(app) as client:
        # Request to the endpoint
        response = client.get("order_items/")

        # Asserts that the response status code is 200
        assert response.status_code == 200


def test_get_order_item():
    """Test getting a specific order_item"""
    with TestClient(app) as client:
        # Request to the endpoint
        response = client.get("order_items/500")

        # Asserts that the response status code is 200
        assert response.status_code == 200
