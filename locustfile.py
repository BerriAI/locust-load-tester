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
            "messages": [
                {"role": "system", "content": "You are a chat bot."},
                {"role": "user", "content": "Hello, how are you?"}
            ],
            "metadata": {
                "tags": ["jobID:214590dsff09fds", "taskName:jmeter_load_test"]
            }
        }
        response = self.client.post("chat/completions", json=payload)
        if response.status_code != 200:
            # log the errors in error.txt
            with open("error.txt", "a") as error_log:
                error_log.write(response.text + "\n")
    


    def on_start(self):
        self.api_key = os.getenv('API_KEY', 'sk-KEjSlM8iPbUdtnzid0YiEA')
        self.client.headers.update({'Authorization': f'Bearer {self.api_key}'})