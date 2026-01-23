# """
# Tests for order endpoints
# """

# from fastapi.testclient import TestClient
# from app.main import app

# client = TestClient(app)


# def test_get_orders():
#     """Test getting all orders"""
#     response = client.get("/api/v1/orders/")
#     assert response.status_code in [200, 404]


# def test_get_order():
#     """Test getting a specific order"""
#     response = client.get("/api/v1/orders/1")
#     assert response.status_code in [200, 404]


# def test_create_order():
#     """Test creating an order"""
#     order_data = {
#         "shipping_address": "123 Test St, Test City, 12345"
#     }
#     response = client.post("/api/v1/orders/", json=order_data)
#     assert response.status_code in [201, 400, 422]
