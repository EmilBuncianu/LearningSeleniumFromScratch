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
    # REPARAT COMPLET: Adăugat /api ca să trimitem cererea direct către endpoint-ul corect de backend
    base_url = "https://reqres.in/api"
    login_payload = {"email": "eve.holt@reqres.in", "password": "cityslicker"}

    response = requests.post(f"{base_url}/login", json=login_payload)
    assert response.status_code == 200, f"Autentificarea a eșuat! Status primit: {response.status_code}"

    token = response.json().get("token")
    return {
        # Trimitem token-ul brut direct, exact așa cum îl așteaptă serverul ReqRes
        "Authorization": token,
        "Content-Type": "application/json",
    }
