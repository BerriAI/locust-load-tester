# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Locust file and requirements file (if you have one)
COPY locustfile.py .

# Install Locust and any other dependencies
RUN pip install --no-cache-dir locust

# Expose the Locust web interface port
EXPOSE 8089

# Set the API_KEY environment variable (you can override this when running the container)
ENV API_KEY=sk-1234

# Command to run Locust
CMD ["locust", "-f", "locustfile.py", "--processes", "4"]
