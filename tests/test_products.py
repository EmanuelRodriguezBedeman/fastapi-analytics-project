# """
# Tests for product endpoints
# """

# from fastapi.testclient import TestClient
# from app.main import app

# client = TestClient(app)


# def test_get_products():
#     """Test getting all products"""
#     response = client.get("/api/v1/products/")
#     assert response.status_code in [200, 404]


# def test_get_product():
#     """Test getting a specific product"""
#     response = client.get("/api/v1/products/1")
#     assert response.status_code in [200, 404]


# def test_create_product():
#     """Test creating a product"""
#     product_data = {
#         "name": "Test Product",
#         "description": "A test product",
#         "price": 29.99,
#         "stock": 100
#     }
#     response = client.post("/api/v1/products/", json=product_data)
#     assert response.status_code in [201, 400, 422]
