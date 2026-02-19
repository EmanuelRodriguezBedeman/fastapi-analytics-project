"""
Tests for sales summary endpoint
"""

from fastapi.testclient import TestClient

from app.main import app


def test_sales_summary_default():
    """Test sales summary with default parameters"""
    with TestClient(app) as client:
        response = client.get("/orders/sales-summary")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if data:
            item = data[0]
            assert "country" in item
            assert "year" in item
            assert "aggregation" in item
            assert "value" in item
            assert item["aggregation"] == "avg"
            assert isinstance(item["value"], (int, float))


def test_sales_summary_aggregation_max():
    """Test sales summary with max aggregation"""
    with TestClient(app) as client:
        response = client.get("/orders/sales-summary?aggregation=max")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if data:
            assert data[0]["aggregation"] == "max"


def test_sales_summary_aggregation_median():
    """Test sales summary with median aggregation"""
    with TestClient(app) as client:
        # This will test if the DB (PostgreSQL) supports percentile_cont
        response = client.get("/orders/sales-summary?aggregation=median")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if data:
            assert data[0]["aggregation"] == "median"


def test_sales_summary_filtering():
    """Test sales summary with country and year filtering"""
    with TestClient(app) as client:
        # First get all to find a valid country and year
        all_response = client.get("/orders/sales-summary")
        all_data = all_response.json()

        if all_data:
            target = all_data[0]
            country = target["country"]
            year = target["year"]

            # Filter by country
            response = client.get(f"/orders/sales-summary?country={country}")
            assert response.status_code == 200
            for item in response.json():
                assert item["country"] == country

            # Filter by year
            response = client.get(f"/orders/sales-summary?year={year}")
            assert response.status_code == 200
            for item in response.json():
                assert item["year"] == year

            # Combined
            response = client.get(f"/orders/sales-summary?country={country}&year={year}")
            assert response.status_code == 200
            for item in response.json():
                assert item["country"] == country
                assert item["year"] == year


def test_sales_summary_invalid_aggregation():
    """Test sales summary with invalid aggregation parameter"""
    with TestClient(app) as client:
        response = client.get("/orders/sales-summary?aggregation=invalid")
        # FastAPI returns 422 for Literal validation failure
        assert response.status_code == 422
