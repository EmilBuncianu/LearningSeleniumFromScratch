import random
from locust import HttpUser, task, between


class ReqResPerformanceUser(HttpUser):
    """Definește comportamentul unui utilizator virtual care atacă API-ul."""

    # Fiecare utilizator virtual va aștepta între 1 și 3 secunde între acțiuni (simulează comportamentul uman)
    wait_time = between(1, 3)

    @task(3)
    def view_users_list(self):
        """Task cu pondere mai mare (3) - simulează navigarea desasă pe lista de utilizatori."""
        # Locust folosește self.client care funcționează exact ca librăria requests utilizată de noi
        page_number = random.choice([1, 2, 3])
        with self.client.get(f"/api/users?page={page_number}", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Serverul a răspuns cu status {response.status_code}")

    @task(1)
    def create_new_user(self):
        """Task cu pondere mai mică (1) - simulează crearea rară de resurse."""
        payload = {
            "name": f"User_{random.randint(1, 1000)}",
            "job": "Performance Tested Automation"
        }
        with self.client.post("/api/users", json=payload, catch_response=True) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure("Eșec la crearea utilizatorului virtual în testul de stres")
