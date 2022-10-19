from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from app import app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


def test_can_serve_static_files(client: TestClient) -> None:
    response = client.get("/static/styles.css")
    assert response.status_code == HTTPStatus.OK.value
    assert response.content


def test_can_render_index(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK.value


def test_can_render_register_page(client: TestClient) -> None:
    response = client.get("/register/")
    assert response.status_code == HTTPStatus.OK.value


def test_can_register_user(client: TestClient) -> None:
    response = client.post("/register/")
    assert response.status_code == HTTPStatus.OK.value
