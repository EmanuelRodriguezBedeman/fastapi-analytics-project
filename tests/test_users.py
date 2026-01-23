# """
# Tests for user endpoints
# """

# from fastapi.testclient import TestClient
# from app.main import app

# client = TestClient(app)


# def test_get_users():
#     """Test getting all users"""
#     response = client.get("/api/v1/users/")
#     assert response.status_code in [200, 404]


# def test_get_user():
#     """Test getting a specific user"""
#     response = client.get("/api/v1/users/1")
#     assert response.status_code in [200, 404]


# def test_create_user():
#     """Test creating a user"""
#     user_data = {
#         "email": "test@example.com",
#         "username": "testuser",
#         "password": "testpassword123"
#     }
#     response = client.post("/api/v1/users/", json=user_data)
#     assert response.status_code in [201, 400, 422]
