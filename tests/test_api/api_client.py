import requests

class APIClient:
    def __init__(self, base_url):
        # Asigură-te că eliminăm eventualele slash-uri finale duplicat
        self.base_url = base_url.rstrip('/')

    def get(self, endpoint, headers=None, params=None):
        return requests.get(f"{self.base_url}{endpoint}", headers=headers, params=params)

    def post(self, endpoint, json_data=None, headers=None):
        return requests.post(f"{self.base_url}{endpoint}", json=json_data, headers=headers)

    def put(self, endpoint, json_data=None, headers=None):
        return requests.put(f"{self.base_url}{endpoint}", json=json_data, headers=headers)

    def delete(self, endpoint, headers=None):
        return requests.delete(f"{self.base_url}{endpoint}", headers=headers)
