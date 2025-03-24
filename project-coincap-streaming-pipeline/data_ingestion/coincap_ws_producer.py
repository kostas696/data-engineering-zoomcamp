import json
import time
import websocket
from kafka import KafkaProducer
from datetime import datetime
from config import KAFKA_BROKER, KAFKA_TOPIC, COINCAP_WS_URL

# Set up Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def on_message(ws, message):
    data = json.loads(message)
    timestamp = int(datetime.utcnow().timestamp() * 1000)

    for asset, price in data.items():
        try:
            event = {
                "asset": asset,
                "price": float(price),
                "timestamp": timestamp
            }
            print(f"Sending: {event}")
            producer.send(KAFKA_TOPIC, value=event)
        except Exception as e:
            print(f"Error processing asset: {asset} - {e}")

def on_error(ws, error):
    print("WebSocket Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("WebSocket Closed")

def on_open(ws):
    print("WebSocket Connected to CoinCap")

def start_stream():
    print("Connecting to:", COINCAP_WS_URL)
    ws = websocket.WebSocketApp(
        COINCAP_WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    while True:
        try:
            ws.run_forever()
        except Exception as e:
            print("WebSocket error, retrying in 5s:", e)
            time.sleep(5)

if __name__ == "__main__":
    start_stream()
