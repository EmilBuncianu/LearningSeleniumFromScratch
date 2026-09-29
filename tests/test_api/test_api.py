import pytest

def test_get_users_list(api_client):
    """Test case to verify extracting a list of users (GET Method)."""
    # Folosește clientul unificat în loc de requests.get() direct
    response = api_client.get("/users", params={"page": 2})

    assert response.status_code == 200, f"Incorrect status code: {response.status_code}"

    response_data = response.json()
    assert "page" in response_data
    assert response_data["page"] == 2
    assert len(response_data["data"]) > 0, "The users list is empty!"


def test_create_user(api_client):
    """Test case to verify creating a new user (POST Method)."""
    payload = {"name": "Mihai Popescu", "job": "QA Automation Engineer"}

    # Transmitem payload-ul corect structurat prin json_data
    response = api_client.post("/users", json_data=payload)

    assert response.status_code == 201, f"User was not created! Status: {response.status_code}"

    response_data = response.json()
    assert response_data["name"] == payload["name"]
    assert response_data["job"] == payload["job"]
    assert "id" in response_data, "The server did not generate an ID for the user!"


def test_user_not_found(api_client):
    """Test case to verify error handling when a resource does not exist (404 Not Found)."""
    response = api_client.get("/users/23")

    assert response.status_code == 404, f"Expected 404, but received: {response.status_code}"


def test_access_secure_resource(api_client, auth_headers):
    """Test case simulating access to a protected resource using the authentication Token."""
    # Injectăm atât clientul cât și headerele unificate generate de conftest
    response = api_client.get("/users/4", headers=auth_headers)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["data"]["id"] == 4


def test_update_user_secure(api_client, auth_headers):
    """Test case for updating a user's data (PUT) within a secured environment."""
    update_payload = {"name": "Mihai Popescu Modificat", "job": "Lead QA Engineer"}

    # Executăm modificarea securizată prin APIClient wrapper
    response = api_client.put("/users/4", json_data=update_payload, headers=auth_headers)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == update_payload["name"]
    assert response_data["job"] == update_payload["job"]
