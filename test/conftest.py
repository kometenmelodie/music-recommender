import pytest
from litestar.testing import TestClient

from app import app


@pytest.fixture(scope="function")  # noqa: PT003
def test_client() -> TestClient:
    return TestClient(app=app)
