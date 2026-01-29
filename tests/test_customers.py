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
        # Request to the endpoint
        response = client.get("/customers/500")
        
        # Asserts that the response status code is 200
        assert response.status_code == 200