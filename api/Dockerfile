# Dockerfile

# Use the official FastAPI Docker image
FROM python:3.10-slim-buster

# Install necessary packages
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONPATH=.

# Set the working directory in the container
WORKDIR $PRJ

# Copy the entire project to the container
COPY . /api

# Install dependencies
RUN pip install fastapi uvicorn requests

# Expose the port
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
