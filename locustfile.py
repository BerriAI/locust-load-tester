import os
import uuid
from locust import HttpUser, task, between, events

# Custom metric to track LiteLLM overhead duration
overhead_durations = []

@events.request.add_listener
def on_request(request_type, name, response_time, response_length, response, context, exception, start_time, url, **kwargs):
    if response and hasattr(response, 'headers'):
        overhead_duration = response.headers.get('x-litellm-overhead-duration-ms')
        if overhead_duration:
            try:
                duration_ms = float(overhead_duration)
                overhead_durations.append(duration_ms)
                # Report as custom metric
                events.request.fire(
                    request_type="Custom",
                    name="LiteLLM Overhead Duration (ms)",
                    response_time=duration_ms,
                    response_length=0,
                )
            except (ValueError, TypeError):
                pass


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
