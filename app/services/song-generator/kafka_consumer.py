from kafka import KafkaConsumer
import redis
import json
import os

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")

# Set up Kafka consumer
consumer = KafkaConsumer(
    "pdf_task",
    bootstrap_servers=[KAFKA_BROKER],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Set up Redis client
redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0)

def consume_tasks():
    print("PDF Generator is listening for tasks...")
    for message in consumer:
        task_data = message.value
        task_id = task_data["task_id"]
        print(f"Received PDF task: {task_data}")

        # Call the PDF generation logic and store the result in Redis
        result = generate_pdf(task_data)
        redis_client.set(task_id, result)

def generate_pdf(task_data):
    # Placeholder for PDF generation logic
    print("Generating PDF with content:", task_data.get("content"))
    return "PDF generated successfully with content: " + task_data.get("content")
