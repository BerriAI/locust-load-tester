# locust-load-tester

Locust load test for a LiteLLM proxy. It sends chat completions to the `fake-openai-endpoint` model and reports the `x-litellm-overhead-duration-ms` header as a custom metric

The container has no default API key. Pass a key the proxy accepts at run time with `-e API_KEY=...`, and the load test exits right away with an error when it is missing

```bash
docker build -t locust-load-tester .
docker run --rm -p 8089:8089 -e API_KEY=<your proxy key> locust-load-tester
```

Open http://localhost:8089 and set the host to your proxy URL. To run headless instead, append the Locust flags to the run command

```bash
docker run --rm -e API_KEY=<your proxy key> locust-load-tester \
  locust -f locustfile.py --headless -u 10 -r 2 -t 60s --host http://<proxy host>:4000
```
