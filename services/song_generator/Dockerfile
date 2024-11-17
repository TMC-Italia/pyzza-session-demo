# Dockerfile

FROM python:3.9-slim

# Set the working directory in the container

# Copy the application code
COPY main.py /song_generator/main.py
COPY service.py /song_generator/service.py
COPY requirements.txt /song_generator/requirements.txt

WORKDIR /song_generator

# Install dependencies
RUN pip install -r requirements.txt

# Expose the service on a specific port
EXPOSE 8002

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]
