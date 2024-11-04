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
            "model": "db-openai-endpoint",
            "messages": [
                {
                    "role": "user", 
                    "content": [
                                {"type": "text", "text": "What is in this image?"},
                                {"type": "image_url",
                                "image_url": {"url": "https://i.etsystatic.com/6267543/r/il/077fe2/3271243073/il_1588xN.3271243073_cmph.jpg"}
                                }
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