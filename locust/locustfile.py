from locust import HttpUser, task, between

class DummyApiUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_dummy(self):
        self.client.get("/dummy")
