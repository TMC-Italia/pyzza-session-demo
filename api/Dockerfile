# Dockerfile

# Use the official FastAPI Docker image
FROM python:3.10-slim-buster

# Copy the application code
COPY main.py /api/main.py
COPY requirements.txt /api/requirements.txt

# Set the working directory in the container
WORKDIR /api

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
