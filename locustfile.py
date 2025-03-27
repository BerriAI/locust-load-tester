import os
import uuid
from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 3)  # Random wait time between requests

    @task
    def litellm_completion(self):
        # no cache hits with this
        # Customize the payload with "model" and "messages" keys
        payload = {
            "model": "fake-openai-endpoint",
            "messages": [{"role": "user", "content": f"Hello, how are you? {uuid.uuid4()}" * 100}],
            "metadata": {
                "tags": ["jobID:214590dsff09fds", "taskName:jmeter_load_test"]
            }
        }
        response = self.client.post("/v1/chat/completions", json=payload)
        if response.status_code != 200:
            # log the errors in error.txt
            with open("error.txt", "a") as error_log:
                error_log.write(response.text + "\n")
    


    def on_start(self):
        self.api_key = os.getenv('API_KEY', 'sk-U6np9GX-BnDQap5w4sqEGQ')
        self.client.headers.update({'Authorization': f'Bearer {self.api_key}'})