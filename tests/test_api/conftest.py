import pytest
import requests
from tests.test_api.api_client import APIClient

@pytest.fixture(scope="session")
def api_client(base_url_api):
    """Creează instanța globală de APIClient folosită în teste."""
    return APIClient(base_url=base_url_api)

@pytest.fixture(scope="session")
def auth_headers():
    """Generează token-ul de securitate din backend și returnează headerele corecte."""
    # FIXED: Modificat din 'https://reqres.in' în 'https://reqres.in/api' ca să nu mai returneze HTML
    base_url = "https://reqres.in/api"
    login_payload = {"email": "eve.holt@reqres.in", "password": "cityslicker"}

    response = requests.post(f"{base_url}/login", json=login_payload)
    assert response.status_code == 200, f"Autentificarea a eșuat! Status primit: {response.status_code}"

    token = response.json().get("token")
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
