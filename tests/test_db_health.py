"""
DB Health check tests
"""

from fastapi.testclient import TestClient

from app.main import app


def test_db_health():
    """Test DB health endpoint returns 200 OK and correct status"""

    with TestClient(app) as client:
        # Request to the endpoint
        response = client.get("/health")

        # Asserts that the response status code is 200
        assert response.status_code == 200

        # Gets the response body
        body = response.json()

        # Asserts that the response body contains the correct keys and values
        assert body["status"] == "healthy"
        assert body["database"] == "connected"
