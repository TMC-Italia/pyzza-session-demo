from kafka_consumer import consume_tasks
import threading

if __name__ == "__main__":
    # Run the Kafka consumer in a separate thread
    consumer_thread = threading.Thread(target=consume_tasks)
    consumer_thread.start()
