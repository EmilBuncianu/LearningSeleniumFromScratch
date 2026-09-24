import pytest
import requests

# Base URL for the target test API
BASE_URL = "https://reqres.in/api"


def test_get_users_list():
    """Test case to verify extracting a list of users (GET Method)."""
    # 1. Send the HTTP GET request
    response = requests.get(f"{BASE_URL}/users?page=2")

    # 2. Validate the HTTP Status Code (200 OK indicates success)
    assert response.status_code == 200, f"Incorrect status code: {response.status_code}"

    # 3. Parse the received JSON response from the backend
    response_data = response.json()

    # 4. Assertions on the returned data structure
    assert "page" in response_data
    assert response_data["page"] == 2
    assert len(response_data["data"]) > 0, "The users list is empty!"
    print(f"\n[API DEBUG] First user found: {response_data['data'][0]['email']}")


def test_create_user():
    """Test case to verify creating a new user (POST Method)."""
    # 1. Define the JSON body (payload) to send to the server
    payload = {
        "name": "Mihai Popescu",
        "job": "QA Automation Engineer"
    }

    # 2. Send the HTTP POST request with our data
    response = requests.post(f"{BASE_URL}/users", json=payload)

    # 3. Validate the status code (201 Created is returned upon successful save)
    assert response.status_code == 201, f"User was not created! Status: {response.status_code}"

    # 4. Verify that the server returns the correct data along with a generated ID
    response_data = response.json()
    assert response_data["name"] == payload["name"]
    assert response_data["job"] == payload["job"]
    assert "id" in response_data, "The server did not generate an ID for the user!"
    print(f"\n[API DEBUG] User created successfully! Generated ID: {response_data['id']}")


def test_user_not_found():
    """Test case to verify error handling when a resource does not exist (404 Not Found)."""
    # Send a non-existent user ID (e.g., 23)
    response = requests.get(f"{BASE_URL}/users/23")

    # The server must respond with the standard 404 code
    assert response.status_code == 404, f"Expected 404, but received: {response.status_code}"


def test_access_secure_resource(auth_headers):
    """Test case simulating access to a protected resource using the authentication Token."""
    # Send the Headers automatically received from the fixture as a parameter
    response = requests.get(f"{BASE_URL}/users/4", headers=auth_headers)

    # Validate success
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["data"]["id"] == 4
    print(f"\n[API DEBUG] Authorized access! Safely extracted user: {response_data['data']['first_name']}")


def test_update_user_secure(auth_headers):
    """Test case for updating a user's data (PUT) within a secured environment."""
    update_payload = {
        "name": "Mihai Popescu Modificat",
        "job": "Lead QA Engineer"
    }

    # Send the PUT request along with the payload and the secured Headers
    response = requests.put(f"{BASE_URL}/users/4", json=update_payload, headers=auth_headers)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == update_payload["name"]
    assert response_data["job"] == update_payload["job"]
    print(f"\n[API DEBUG] Resource successfully updated using Bearer authorization!")
