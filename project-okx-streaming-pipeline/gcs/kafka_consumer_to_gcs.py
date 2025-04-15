import json
import os
from datetime import datetime
from confluent_kafka import Consumer
from google.cloud import storage

# Environment variables
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "crypto-prices")
GCP_BUCKET = os.getenv("GCP_BUCKET_NAME", "souf-de-zoomcamp-project")
GCP_FOLDER = os.getenv("GCP_BASE_PATH", "crypto/raw")

# Initialize GCS client
gcs_client = storage.Client()
bucket = gcs_client.bucket(GCP_BUCKET)

# Kafka config
conf = {
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'crypto-gcs-writer',
    'auto.offset.reset': 'latest',
    'enable.auto.commit': False
}
consumer = Consumer(conf)
consumer.subscribe([KAFKA_TOPIC])

def write_to_gcs(data_batch):
    now = datetime.utcnow()
    path = f"{GCP_FOLDER}/{now.strftime('%Y-%m-%d/%H')}/data_{now.strftime('%M%S')}.json"
    blob = bucket.blob(path)
    blob.upload_from_string(json.dumps(data_batch), content_type='application/json')
    print(f"Uploaded {len(data_batch)} records to GCS: {path}", flush=True)

def main():
    print("Listening to Kafka and writing to GCS...", flush=True)
    batch = []
    batch_size = 50

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("Error:", msg.error(), flush=True)
            continue

        try:
            record = json.loads(msg.value().decode("utf-8"))
            batch.append(record)

            if len(batch) >= batch_size:
                write_to_gcs(batch)
                batch = []

        except Exception as e:
            print("Failed to process message:", e, flush=True)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Stopping consumer...", flush=True)
    finally:
        consumer.close()
