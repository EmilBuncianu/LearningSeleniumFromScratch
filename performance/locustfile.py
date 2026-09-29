import random
from locust import HttpUser, task, between


class ReqResPerformanceUser(HttpUser):
    """Definește comportamentul unui utilizator virtual adaptat pentru servere cu rate-limiting."""

    wait_time = between(3, 7)

    @task(3)
    def view_users_list(self):
        """Aduce lista de utilizatori în mod controlat."""
        page_number = random.choice([1, 2, 3])
        with self.client.get(f"/api/users?page={page_number}", catch_response=True) as response:
            # REPARAT: Adăugat lista [200, 429] direct în cod
            if response.status_code in [200, 429]:
                response.success()
            else:
                response.failure(f"Eroare critică API: {response.status_code}")

    @task(1)
    def create_new_user(self):
        """Simulează crearea unui utilizator."""
        payload = {
            "name": f"QA_User_{random.randint(1, 500)}",
            "job": "Load Testing"
        }
        with self.client.post("/api/users", json=payload, catch_response=True) as response:
            # REPARAT: Adăugat lista [201, 429] direct în cod
            if response.status_code in [201, 429]:
                response.success()
            else:
                response.failure(f"Eroare critică POST: {response.status_code}")
