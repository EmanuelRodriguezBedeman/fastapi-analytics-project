"""
Tests for sales summary endpoint
"""

from fastapi.testclient import TestClient

from app.main import app


def test_sales_summary_structure():
    """Test the overall structure of the sales summary response"""
    with TestClient(app) as client:
        response = client.get("/orders/sales-summary")
        assert response.status_code == 200
        data = response.json()

        assert "metadata" in data
        assert "results" in data

        metadata = data["metadata"]
        assert "requested_at" in metadata
        assert "currency" in metadata
        assert metadata["currency"] == "USD"
        assert "total_groups" in metadata
        assert "applied_filters" in metadata

        if data["results"]:
            group = data["results"][0]
            assert "country" in group
            assert "year" in group
            assert "metrics" in group

            metrics = group["metrics"]
            # Should have all 5 metrics by default
            expected_metrics = ["average", "max", "median", "sum", "count"]
            for m in expected_metrics:
                assert m in metrics


def test_sales_summary_metric_filter():
    """Test filtering by a specific metric"""
    with TestClient(app) as client:
        response = client.get("/orders/sales-summary?metric=sum")
        assert response.status_code == 200
        data = response.json()

        if data["results"]:
            metrics = data["results"][0]["metrics"]
            # Should have sum and count
            assert "sum" in metrics
            assert "count" in metrics
            # Should NOT have avg, max, median
            assert "average" not in metrics
            assert "max" not in metrics
            assert "median" not in metrics


def test_sales_summary_filters_and_metadata():
    """Test filtering by country and year, and check applied_filters in metadata (status is always delivered)"""
    with TestClient(app) as client:
        # First get any group to use valid filters
        init_res = client.get("/orders/sales-summary")
        init_data = init_res.json()

        if init_data["results"]:
            target = init_data["results"][0]
            country = target["country"]
            year = target["year"]

            params = f"country={country}&year={year}"
            response = client.get(f"/orders/sales-summary?{params}")
            assert response.status_code == 200
            data = response.json()

            # Check metadata applied_filters - country and year should match, status MUST BE delivered
            filters = data["metadata"]["applied_filters"]
            assert filters["country"] == country
            assert filters["year"] == year
            assert filters["status"] == "delivered"
            assert "metric" in filters
            assert filters["metric"] is None

            # Check results match filters
            for res in data["results"]:
                assert res["country"] == country
                assert res["year"] == year


def test_sales_summary_ordering():
    """Test that results are ordered by year DESC, then sum DESC"""
    with TestClient(app) as client:
        response = client.get("/orders/sales-summary")
        assert response.status_code == 200
        data = response.json()
        results = data["results"]

        if len(results) > 1:
            for i in range(len(results) - 1):
                curr = results[i]
                nxt = results[i + 1]

                # Year DESC
                assert curr["year"] >= nxt["year"]

                # If same year, Sum DESC
                if curr["year"] == nxt["year"]:
                    assert curr["metrics"]["sum"] >= nxt["metrics"]["sum"]


def test_sales_summary_invalid_metric():
    """Test sales summary with invalid metric parameter"""
    with TestClient(app) as client:
        response = client.get("/orders/sales-summary?metric=invalid")
        # FastAPI returns 422 for Literal validation failure
        assert response.status_code == 422
