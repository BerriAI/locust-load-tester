import os
import uuid
from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(0.5, 1)  # Random wait time between requests

    @task(100)
    def litellm_completion(self):
        # no cache hits with this
        # Customize the payload with "model" and "messages" keys
        payload = {
            "model": "gemini-vision",
            "messages": [
                {
                    "role": "user", 
                    "content": [
                                {"type": "text", "text": "What is in this image?"}
                    ]
                }
            ]
        }

        response = self.client.post("chat/completions", json=payload)
        if response.status_code != 200:
            # log the errors in error.txt
            with open("error.txt", "a") as error_log:
                error_log.write(response.text + "\n")
    


    def on_start(self):
        self.api_key = os.getenv('API_KEY', 'sk-1234')
        self.client.headers.update({'Authorization': f'Bearer {self.api_key}'})
