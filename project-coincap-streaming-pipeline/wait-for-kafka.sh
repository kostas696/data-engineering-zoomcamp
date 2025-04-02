#!/bin/bash

KAFKA_HOST=${KAFKA_BROKER:-kafka:9092}
echo "Waiting for Kafka to be ready at $KAFKA_HOST..."

RETRIES=40
until nc -z ${KAFKA_HOST%:*} ${KAFKA_HOST##*:} || [ $RETRIES -eq 0 ]; do
  echo "Kafka not yet ready... retrying"
  sleep 3
  ((RETRIES--))
done

if [ $RETRIES -eq 0 ]; then
  echo "Failed to connect to Kafka at $KAFKA_HOST"
  exit 1
fi

echo "Kafka port is open — giving it 5 seconds to stabilize..."
sleep 5

echo "Kafka is ready — continuing with command: $@"
exec "$@"
