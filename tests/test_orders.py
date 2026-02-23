"""
Tests for order endpoints
"""

from fastapi.testclient import TestClient

from app.main import app


def test_get_orders():
    """Test getting all orders"""
    with TestClient(app) as client:
        response = client.get("/orders?skip=0&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert "metadata" in data
        assert "results" in data
        assert data["metadata"]["applied_filters"] == {"skip": 0, "limit": 10}


def test_get_order():
    """Test getting a specific order"""
    with TestClient(app) as client:
        # First, get the list to find a valid ID
        list_response = client.get("/orders?limit=1")
        orders = list_response.json()["results"]

        if orders:
            order_id = orders[0]["id"]
            response = client.get(f"/orders/{order_id}")
            assert response.status_code == 200
            data = response.json()
            assert data["metadata"]["total_groups"] == 1
            assert len(data["results"]) == 1
            assert data["results"][0]["id"] == order_id
        else:
            print("No orders found to test individual GET")


def test_order_statuses():
    """Test order statuses analytics endpoint"""
    with TestClient(app) as client:
        response = client.get("/orders/statuses")
        assert response.status_code == 200
        data = response.json()

        assert "metadata" in data
        assert "results" in data
        assert data["metadata"]["total_groups"] == len(data["results"])
        assert data["metadata"]["applied_filters"] == {"order_status": None}

        order_statuses = data["results"]
        if order_statuses:
            assert "status" in order_statuses[0]
            assert "count" in order_statuses[0]
