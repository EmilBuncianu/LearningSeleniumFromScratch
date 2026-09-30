import pytest
from jsonschema import validate

# ==========================================
# DEFINIREA SCHEMELOR JSON (CONTRACTUL API)
# ==========================================

# Contract strict pentru structura returnată de GET /users?page=2
USER_LIST_SCHEMA = {
    "type": "object",
    "properties": {
        "page": {"type": "integer"},
        "per_page": {"type": "integer"},
        "total": {"type": "integer"},
        "total_pages": {"type": "integer"},
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "email": {"type": "string"},  # Păstrat ca string simplu pentru compatibilitate 100% universală
                    "first_name": {"type": "string"},
                    "last_name": {"type": "string"},
                    "avatar": {"type": "string"}
                },
                "required": ["id", "email", "first_name", "last_name", "avatar"]
            }
        },
        "support": {
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "text": {"type": "string"}
            },
            "required": ["url", "text"]
        }
    },
    "required": ["page", "per_page", "total", "total_pages", "data"]
}

# Contract strict pentru structura returnată la crearea unei resurse noi (POST /users)
CREATE_USER_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "job": {"type": "string"},
        "id": {"type": "string"},  # ReqRes generează ID-ul dinamic sub formă de string numeric
        "createdAt": {"type": "string"}  # Validăm prezența timestamp-ului generat de backend
    },
    "required": ["name", "job", "id", "createdAt"]
}


# ==========================================
# IMPLEMENTAREA TESTELOR AUTOMATIZATE
# ==========================================

def test_get_users_list(api_client):
    """Test case to verify extracting a list of users (GET Method) and validating its schema."""
    response = api_client.get("/users", params={"page": 2})

    assert response.status_code == 200, f"Incorrect status code: {response.status_code}"

    response_data = response.json()

    # VALIDARE AVANSATĂ: Asigură-te că tipurile de date din răspuns nu au fost alterate pe server
    validate(instance=response_data, schema=USER_LIST_SCHEMA)

    assert response_data["page"] == 2
    assert len(response_data["data"]) > 0, "The users list is empty!"


def test_create_user(api_client):
    """Test case to verify creating a new user (POST Method) and validating its contract."""
    payload = {"name": "Mihai Popescu", "job": "QA Automation Engineer"}

    response = api_client.post("/users", json_data=payload)

    assert response.status_code == 201, f"User was not created! Status: {response.status_code}"

    response_data = response.json()

    # VALIDARE AVANSATĂ: Verifică existența structurală a cheilor obligatorii întoarse la salvare
    validate(instance=response_data, schema=CREATE_USER_SCHEMA)

    assert response_data["name"] == payload["name"]
    assert response_data["job"] == payload["job"]
    assert "id" in response_data, "The server did not generate an ID for the user!"


def test_user_not_found(api_client):
    """Test case to verify error handling when a resource does not exist (404 Not Found)."""
    response = api_client.get("/users/23")

    assert response.status_code == 404, f"Expected 404, but received: {response.status_code}"


def test_access_secure_resource(api_client, auth_headers):
    """Test case simulating access to a protected resource using the authentication Token."""
    response = api_client.get("/users/4", headers=auth_headers)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["data"]["id"] == 4


def test_update_user_secure(api_client, auth_headers):
    """Test case for updating a user's data (PUT) within a secured environment."""
    update_payload = {"name": "Mihai Popescu Modificat", "job": "Lead QA Engineer"}

    response = api_client.put("/users/4", json_data=update_payload, headers=auth_headers)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == update_payload["name"]
    assert response_data["job"] == update_payload["job"]
