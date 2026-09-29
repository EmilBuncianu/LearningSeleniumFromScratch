import pytest


def test_api_login_successful(api_client):
    """Validează un flux pozitiv de autentificare prin API-ul ReqRes."""
    # ReqRes are nevoie de un email valid din sistemul lor
    payload = {"email": "eve.holt@reqres.in", "password": "cityslicker"}

    # FIXED: Am schimbat 'data=' în 'json_data=' pentru a trimite un JSON valid către microserviciu
    response = api_client.post("/login", json_data=payload)

    # Verificăm statusul de succes 200
    assert response.status_code == 200, f"Răspuns neașteptat: {response.status_code}"

    # Validăm că serverul ne-a întors token-ul de autentificare
    json_data = response.json()
    assert "token" in json_data, "Token-ul de autentificare lipsește din răspuns!"


def test_api_login_invalid_credentials(api_client):
    """Validează comportamentul API-ului la date de autentificare greșite."""
    # ReqRes cere în mod specific câmpul 'email', chiar dacă valoarea este greșită, pentru a valida payload-ul
    payload = {"email": "invalid_user@reqres.in", "password": "wrong_password"}

    # FIXED: Am eliminat '/api' duplicat din endpoint și am trecut la 'json_data='
    response = api_client.post("/login", json_data=payload)

    # ReqRes returnează 400 Bad Request pentru utilizatori lipsă/invalizi în baza lor de date
    assert response.status_code == 400, f"Așteptat status 400, dar s-a primit {response.status_code}"

    json_data = response.json()
    assert "error" in json_data, "Mesajul de eroare lipsește din răspuns!"
