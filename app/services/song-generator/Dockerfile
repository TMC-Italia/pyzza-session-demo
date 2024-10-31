# Dockerfile for pdf_generator service

FROM python:3.9-slim

WORKDIR /app

# Copy the application code
COPY main.py /app/main.py
COPY kafka_consumer.py /app/kafka_consumer.py
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port
EXPOSE 8000

CMD ["python", "main.py"]
