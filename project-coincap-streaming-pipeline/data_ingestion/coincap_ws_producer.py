import json
import os
from dotenv import load_dotenv
from confluent_kafka import Producer
from websocket import WebSocketApp

load_dotenv()

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "crypto-prices")
ASSETS_FILE = os.path.join(os.path.dirname(__file__), "assets.txt")

def load_assets():
    with open(ASSETS_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

ASSETS = load_assets()

# Set up Kafka Producer
producer = Producer({'bootstrap.servers': KAFKA_BROKER})

# Callback to handle delivery status
def delivery_report(err, msg):
    if err is not None:
        print(f"❌ Message delivery failed: {err}")
    else:
        print(f"✅ Message delivered to {msg.topic()} [{msg.partition()}]")

# Handle messages from WebSocket
def on_message(ws, message):
    print(f"📥 Received: {message}")
    producer.produce(KAFKA_TOPIC, value=message, callback=delivery_report)
    producer.poll(0)  # Serve delivery callbacks

# Handle errors
def on_error(ws, error):
    print(f"❌ WebSocket Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("🔌 WebSocket closed")

def on_open(ws):
    print("🌐 WebSocket connection opened")

if __name__ == "__main__":
    asset_list = ",".join(ASSETS)
    url = f"wss://ws.coincap.io/prices?assets={asset_list}"
    ws = WebSocketApp(url,
                      on_open=on_open,
                      on_message=on_message,
                      on_error=on_error,
                      on_close=on_close)
    print(f"🔄 Connecting to {url}")
    ws.run_forever()