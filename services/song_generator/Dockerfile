# Dockerfile

FROM python:3.9-slim

# Copy the application code
COPY . /song_generator
WORKDIR /song_generator

# Install dependencies
RUN pip install -r requirements.txt

# Expose the service on a specific port
EXPOSE 8002

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]
