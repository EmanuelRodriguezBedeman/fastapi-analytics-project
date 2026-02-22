import pytest

from app.main import app
from app.utils.rate_limiter import rate_limit_dependency


@pytest.fixture(autouse=True)
def disable_rate_limiter():
    """
    Globally disables the rate limiter for all tests to avoid HTTP 429 errors.
    """
    app.dependency_overrides[rate_limit_dependency] = lambda: None
    yield
    app.dependency_overrides.clear()
