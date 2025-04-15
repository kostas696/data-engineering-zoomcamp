FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "wait-for-kafka.sh", "python", "okx_ws_producer.py"]
