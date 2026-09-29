import pytest


def test_api_get_single_user(api_client):
    """Validează extragerea unui singur utilizator existent."""
    response = api_client.get("/users/2")

    assert response.status_code == 200
    json_data = response.json()
    assert "data" in json_data
    assert json_data["data"]["id"] == 2
    assert "email" in json_data["data"]


def test_api_delete_user(api_client):
    """Validează ștergerea unui utilizator din sistem (status 204 No Content)."""
    response = api_client.delete("/users/2")

    assert response.status_code == 204
