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
        # Request to the endpoint
        response = client.get("products/300")

        # Asserts that the response status code is 200
        assert response.status_code == 200
