"""
Health check tests
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    """Test health endpoint returns 200 OK"""
    response = client.get("/api/v1/health/")
    assert response.status_code == 200