"""
Tests for reviews endpoints
"""

from fastapi.testclient import TestClient

from app.main import app


def test_get_reviews():
    """Test getting all reviews"""
    with TestClient(app) as client:
        response = client.get("/reviews")
        assert response.status_code == 200
        data = response.json()
        assert "metadata" in data
        assert "results" in data


def test_get_review():
    """Test getting a specific review"""
    with TestClient(app) as client:
        # First, get the list to find a valid ID
        list_response = client.get("/reviews?limit=1")
        reviews = list_response.json()["results"]

        if reviews:
            review_id = reviews[0]["id"]
            response = client.get(f"/reviews/{review_id}")
            assert response.status_code == 200
            data = response.json()
            assert data["metadata"]["total_groups"] == 1
            assert len(data["results"]) == 1
        else:
            print("No reviews found to test individual GET")
