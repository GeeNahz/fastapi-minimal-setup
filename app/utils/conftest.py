import pytest
from fastapi.testclient import TestClient
from app.core.config import settings
from app.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(
        app,
        base_url=f"http://127.0.0.1:8000{settings.API_V1_STR}",
    ) as c:
        yield c
