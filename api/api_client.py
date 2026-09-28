import pytest
import requests


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        # Aici poți adăuga headere globale (ex: Content-Type, Auth Tokens)
        self.session.headers.update({"Content-Type": "application/json"})

    def post(self, endpoint, data=None):
        """Efectuează o cerere HTTP POST generică."""
        url = f"{self.base_url}{endpoint}"
        return self.session.post(url, json=data)

    def get(self, endpoint, params=None):
        """Efectuează o cerere HTTP GET generică."""
        url = f"{self.base_url}{endpoint}"
        return self.session.get(url, params=params)

    @pytest.fixture(scope="session")
    def api_client(base_url_api):
        """Inițializează clientul API cu adresa ReqRes citită din JSON."""
        return APIClient(base_url=base_url_api)
