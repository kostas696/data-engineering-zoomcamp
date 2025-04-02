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
        return [line.strip().upper() for line in f if line.strip()]

ASSETS = load_assets()

producer = Producer({'bootstrap.servers': KAFKA_BROKER})

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def on_message(ws, message):
    data = json.loads(message)
    if "arg" in data and "data" in data:
        for item in data["data"]:
            payload = {
                "symbol": item.get("instId"),
                "priceUsd": item.get("last"),
                "timestamp": int(item.get("ts"))  # milliseconds since epoch
            }
            print(f"📥 Received: {payload}")
            producer.produce(KAFKA_TOPIC, value=json.dumps(payload), callback=delivery_report)
            producer.poll(0)

def on_error(ws, error):
    print(f"WebSocket Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("🔌 WebSocket closed")

def on_open(ws):
    print("WebSocket connection opened")
    for asset in ASSETS:
        subscription = {
            "op": "subscribe",
            "args": [{
                "channel": "tickers",
                "instId": f"{asset}-USDT"
            }]
        }
        ws.send(json.dumps(subscription))

if __name__ == "__main__":
    url = "wss://wspap.okx.com:8443/ws/v5/public"
    print(f"Connecting to {url}...")
    ws = WebSocketApp(
        url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()
