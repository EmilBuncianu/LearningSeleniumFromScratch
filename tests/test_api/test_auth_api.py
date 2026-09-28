import pytest


def test_api_login_successful(api_client):
    """Validează un flux pozitiv de autentificare prin API-ul ReqRes."""
    # ReqRes are nevoie de un email valid din sistemul lor (ex: eve.holt@reqres.in)
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicker"
    }

    # Trimitem cererea către endpoint-ul de login (/login se adaugă la https://reqres.in)
    response = api_client.post("/login", data=payload)

    # Verificăm statusul de succes 200
    assert response.status_code == 200, f"Răspuns neașteptat: {response.status_code}"

    # Validăm că serverul ne-a întors token-ul de autentificare
    json_data = response.json()
    assert "token" in json_data, "Token-ul de autentificare lipsește din răspuns!"



def test_api_login_invalid_credentials(api_client):
    """Validează comportamentul API-ului la date de autentificare greșite."""
    payload = {
        "username": "invalid_user",
        "password": "wrong_password"
    }

    response = api_client.post("/api/login", data=payload)

    # Backend-ul ar trebui să întoarcă 401 Unauthorized sau 400 Bad Request
    assert response.status_code in [400, 401]
