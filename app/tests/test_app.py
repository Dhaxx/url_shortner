import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def created_short_url(client):
    response = client.post(
        "/shorten",
        json={"url": "https://github.com/Dhaxx"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()

def test_short_code_return_302_and_redirect(client, created_short_url):
    short_code = created_short_url["short_url"].rsplit("/", 1)[-1]

    response = client.get(f"/{short_code}", follow_redirects=False)

    assert response.status_code == status.HTTP_302_FOUND
    assert response.headers["location"] == "https://github.com/Dhaxx"