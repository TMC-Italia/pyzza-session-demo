# Dockerfile

FROM python:3.9-slim

# Copy the entire project to the container
COPY . /hr_assistant
WORKDIR /hr_assistant

# Install dependencies
RUN pip install -r requirements.txt

# Expose the service on a specific port
EXPOSE 8001

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
