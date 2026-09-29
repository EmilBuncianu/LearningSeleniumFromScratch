import requests
import logging

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        logger.info(f"Client API instanțiat cu succes pentru URL-ul: {self.base_url}")

    def get(self, endpoint, headers=None, params=None):
        logger.info(f"[API REQ] GET către endpoint-ul: {endpoint} | Params: {params}")
        response = requests.get(f"{self.base_url}{endpoint}", headers=headers, params=params)
        logger.info(f"[API RES] Status primit: {response.status_code}")
        return response

    def post(self, endpoint, json_data=None, headers=None):
        logger.info(f"[API REQ] POST către endpoint-ul: {endpoint}")
        response = requests.post(f"{self.base_url}{endpoint}", json=json_data, headers=headers)
        logger.info(f"[API RES] Status primit: {response.status_code}")
        return response

    def put(self, endpoint, json_data=None, headers=None):
        logger.info(f"[API REQ] PUT către endpoint-ul: {endpoint}")
        response = requests.put(f"{self.base_url}{endpoint}", json=json_data, headers=headers)
        logger.info(f"[API RES] Status primit: {response.status_code}")
        return response

    def delete(self, endpoint, headers=None):
        logger.info(f"[API REQ] DELETE către endpoint-ul: {endpoint}")
        response = requests.delete(f"{self.base_url}{endpoint}", headers=headers)
        logger.info(f"[API RES] Status primit: {response.status_code}")
        return response
