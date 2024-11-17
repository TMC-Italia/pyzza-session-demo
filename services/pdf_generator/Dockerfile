# Dockerfile

FROM python:3.9-slim

WORKDIR /app

# Copy the application code
COPY main.py /app/main.py
COPY service.py /app/service.py
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Expose the service on a specific port
EXPOSE 8001

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
