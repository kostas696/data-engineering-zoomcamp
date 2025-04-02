FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy script, code, and credentials
COPY gcs/kafka_consumer_to_gcs.py ./kafka_consumer_to_gcs.py
COPY gcloud/kafka-consumer-key.json /app/gcloud-key.json
COPY wait-for-kafka.sh ./wait-for-kafka.sh

# Make wait script executable
RUN chmod +x wait-for-kafka.sh

# Install dependencies
RUN pip install --no-cache-dir \
    confluent-kafka \
    google-cloud-storage

ENV GOOGLE_APPLICATION_CREDENTIALS="/app/gcloud-key.json" \
    KAFKA_BROKER="kafka:9092" \
    KAFKA_TOPIC="crypto-prices" \
    GCP_BUCKET_NAME="souf-de-zoomcamp-project" \
    GCP_BASE_PATH="crypto/raw"

CMD ["sh", "wait-for-kafka.sh", "python", "kafka_consumer_to_gcs.py"]