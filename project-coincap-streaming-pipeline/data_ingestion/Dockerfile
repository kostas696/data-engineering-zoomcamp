FROM python:3.10-slim

WORKDIR /app

# Install system packages
RUN apt-get update && apt-get install -y gcc netcat-openbsd && apt-get clean

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Entry point waits for Kafka
CMD ["./wait-for-kafka.sh", "python", "coincap_ws_producer.py"]