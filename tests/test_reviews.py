"""
Tests for reviews endpoints
"""

from fastapi.testclient import TestClient

from app.main import app


def test_get_reviews():
    """Test getting all reviews"""
    with TestClient(app) as client:
        # Request to the endpoint
        response = client.get("reviews/")

        # Asserts that the response status code is 200
        assert response.status_code == 200


def test_get_review():
    """Test getting a specific review"""
    with TestClient(app) as client:
        # Request to the endpoint
        response = client.get("reviews/200")

        # Asserts that the response status code is 200
        assert response.status_code == 200
