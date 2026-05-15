from locust import HttpUser, task, between


class TaxiPredictionUser(HttpUser):
    wait_time = between(1, 3)

    @task(7)
    def predict_trip(self):
        payload = {
            "PULocationID": "132",
            "DOLocationID": "161",
        }
        self.client.post("/api/v1/predict", json=payload)
