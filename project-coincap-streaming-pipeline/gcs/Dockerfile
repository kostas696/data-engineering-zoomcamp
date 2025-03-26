# Use an official lightweight Python image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the code and credentials
COPY gcs/kafka_consumer_to_gcs.py ./
COPY gcloud/kafka-consumer-key.json /app/gcloud-key.json

# Install Python dependencies
RUN pip install --no-cache-dir \
    confluent-kafka \
    google-cloud-storage

# Set environment variables (pass these in docker run if you prefer)
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/gcloud-key.json" \
    KAFKA_BROKER="kafka:9092" \
    KAFKA_TOPIC="crypto-prices" \
    GCP_BUCKET_NAME="souf-de-zoomcamp-project" \
    GCP_BASE_PATH="crypto/raw"

# Run the script
CMD ["python", "kafka_consumer_to_gcs.py"]