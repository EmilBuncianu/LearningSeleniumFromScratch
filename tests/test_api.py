import pytest
import requests

# URL-ul de bază al API-ului de test
BASE_URL = "https://reqres.in/api"


def test_get_users_list():
    """Test pentru a verifica extragerea unei liste de utilizatori (Metoda GET)"""
    # 1. Trimitem cererea HTTP GET
    response = requests.get(f"{BASE_URL}/users?page=2")

    # 2. Validăm Codul de Status HTTP (200 OK înseamnă succes)
    assert response.status_code == 200, f"Status cod greșit: {response.status_code}"

    # 3. Parsăm răspunsul JSON primit de la backend
    response_data = response.json()

    # 4. Aserțiuni pe structura de date primită
    assert "page" in response_data
    assert response_data["page"] == 2
    assert len(response_data["data"]) > 0, "Lista de utilizatori este goală!"
    print(f"\n[API DEBUG] Primul utilizator găsit: {response_data['data'][0]['email']}")


def test_create_user():
    """Test pentru a verifica crearea unui utilizator nou (Metoda POST)"""
    # 1. Definim corpul JSON (payload-ul) pe care îl trimitem la server
    payload = {
        "name": "Mihai Popescu",
        "job": "QA Automation Engineer"
    }

    # 2. Trimitem cererea HTTP POST cu datele noastre
    response = requests.post(f"{BASE_URL}/users", json=payload)

    # 3. Validăm codul de status (201 Created se întoarce la salvare cu succes)
    assert response.status_code == 201, f"Utilizatorul nu a fost creat! Status: {response.status_code}"

    # 4. Verificăm că serverul ne întoarce datele corecte înapoi, plus un ID generat
    response_data = response.json()
    assert response_data["name"] == payload["name"]
    assert response_data["job"] == payload["job"]
    assert "id" in response_data, "Serverul nu a generat un ID pentru utilizator!"
    print(f"\n[API DEBUG] Utilizator creat cu succes! ID Generat: {response_data['id']}")


def test_user_not_found():
    """Test pentru a verifica gestionarea erorilor când resursa nu există (404 Not Found)"""
    # Trimitem un ID de utilizator inexistent (ex: 23)
    response = requests.get(f"{BASE_URL}/users/23")

    # Serverul trebuie să răspundă cu codul standard 404
    assert response.status_code == 404, f"Așteptat 404, dar s-a primit: {response.status_code}"


def test_access_secure_resource(auth_headers):
    """Test care simulează accesarea unei resurse protejate folosind Token-ul"""
    # Trimitem Headers-ul primit automat din fixture ca parametru
    response = requests.get(f"{BASE_URL}/users/4", headers=auth_headers)

    # Validăm succesul
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["data"]["id"] == 4
    print(f"\n[API DEBUG] Acces autorizat! Utilizator extras securizat: {response_data['data']['first_name']}")


def test_update_user_secure(auth_headers):
    """Test pentru actualizarea datelor unui utilizator (PUT) într-un mediu securizat"""
    update_payload = {
        "name": "Mihai Popescu Modificat",
        "job": "Lead QA Engineer"
    }

    # Trimitem request-ul de tip PUT alături de payload și Headers-ul securizat
    response = requests.put(f"{BASE_URL}/users/4", json=update_payload, headers=auth_headers)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == update_payload["name"]
    assert response_data["job"] == update_payload["job"]
    print(f"\n[API DEBUG] Resursă actualizată cu succes folosind autorizarea Bearer!")