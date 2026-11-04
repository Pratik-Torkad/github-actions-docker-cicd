"""Tests for the Flask demo service."""

import pytest

from app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def test_home_returns_service_information(client):
    response = client.get("/")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["service"] == "flask-cicd-demo"
    assert payload["status"] == "running"


def test_health_endpoint_returns_healthy(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_unknown_route_returns_not_found(client):
    response = client.get("/this-route-does-not-exist")

    assert response.status_code == 404
