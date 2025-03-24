import os
from dotenv import load_dotenv

# Load .env if available
load_dotenv()

# Kafka Configuration
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "crypto-prices")

# Load asset list from assets.txt or .env
def load_assets():
    asset_env = os.getenv("COINCAP_ASSETS")
    if asset_env:
        return [asset.strip() for asset in asset_env.split(",") if asset.strip()]

    asset_file_path = os.path.join(os.path.dirname(__file__), "assets.txt")
    try:
        with open(asset_file_path, "r") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        # Fallback default
        return ["bitcoin", "ethereum", "solana"]

ASSET_LIST = load_assets()

# Construct CoinCap WebSocket URL
COINCAP_WS_URL = f"wss://ws.coincap.io/prices?assets={','.join(ASSET_LIST)}"