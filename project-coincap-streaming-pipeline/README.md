# Crypto Streaming Pipeline: Real-Time Crypto Price Dashboard

## ✨ Project Overview

This project is the final course deliverable for the Data Engineering Zoomcamp. It demonstrates an **end-to-end streaming data pipeline** built on **Google Cloud Platform (GCP)** using a real-time data source (OKX WebSocket API), Apache Kafka, Spark, BigQuery, and Looker Studio.

The primary goal is to process, validate, and visualize live cryptocurrency pricing data through a fully orchestrated pipeline.

---

## 💡 Problem Statement

Create a streaming pipeline that:
- Ingests crypto prices from a real-time API.
- Writes the data to a raw storage layer (GCS).
- Transforms and cleans the data using Spark.
- Loads the results into a partitioned BigQuery table.
- Validates the processed data.
- Visualizes the data with a dynamic Looker Studio dashboard.

---

## 🌐 Cloud Setup

- **Cloud Provider**: Google Cloud Platform (GCP)
- **IaC**: Terraform for provisioning (VM, IAM, service account)
- **VM**: Self-hosted Airflow + Spark running on GCE

---

## Architecture

![Architecture](images\crypto_pipeline_architecture.png)

---

## ♻️ Streaming Pipeline Architecture

```
OKX WebSocket API
        ⬇
  Dockerized Kafka Producer
        ⬇
        Kafka
        ⬇
  Dockerized Kafka Consumer
        ⬇
      GCS (raw)
        ⬇
     Spark Job (on GCE)
        ⬇
    BigQuery Table (partitioned)
        ⬇
  Data Validation (Python script)
        ⬇
     Looker Studio Dashboard
```

---

## 📆 Technologies Used

- **Streaming**: WebSocket, Apache Kafka (via Docker Compose)
- **Ingestion**: Kafka Consumer ➔ GCS
- **Processing**: Apache Spark (PySpark)
- **Orchestration**: Apache Airflow
- **Storage**: Google Cloud Storage (GCS)
- **Data Warehouse**: Google BigQuery (partitioned by ingestion time)
- **Dashboard**: Looker Studio
- **IaC**: Terraform
- **Containerization**: Docker

---

## 💼 Project Structure

```
📦project-coincap-streaming-pipeline
 ┣ 📂.env
 ┣ 📂.venv
 ┣ 📂dags
 ┃ ┣ 📜.env
 ┃ ┣ 📜Dockerfile
 ┃ ┗ 📜streaming_pipeline_dag.py
 ┣ 📂data_ingestion
 ┃ ┣ 📜assets.txt
 ┃ ┣ 📜Dockerfile
 ┃ ┣ 📜okx_ws_producer.py
 ┃ ┗ 📜requirements.txt
 ┣ 📂gcloud
 ┃ ┗ 📜kafka-consumer-key.json
 ┣ 📂gcs
 ┃ ┣ 📜Dockerfile
 ┃ ┣ 📜kafka_consumer_to_gcs.py
 ┃ ┗ 📜requirements.txt
 ┣ 📂images
 ┃ ┣ 📜airflow.png
 ┃ ┣ 📜bigquery.png
 ┃ ┣ 📜crypto_pipeline_architecture.png
 ┃ ┣ 📜gcs_bucket.png
 ┃ ┣ 📜looker_studio.png
 ┃ ┗ 📜running_consumer.png
 ┣ 📂reports
 ┃ ┗ 📜Looker_Studio_Reporting_-_4_14_25,_3_48 PM.pdf
 ┣ 📂spark_jobs
 ┃ ┗ 📜spark_gcs_to_bq.py
 ┣ 📂terraform
 ┃ ┣ 📂.terraform
 ┃ ┣ 📂modules
 ┃ ┃ ┣ 📂gcs
 ┃ ┃ ┃ ┣ 📜main.tf
 ┃ ┃ ┃ ┣ 📜outputs.tf
 ┃ ┃ ┃ ┗ 📜variables.tf
 ┃ ┃ ┣ 📂network
 ┃ ┃ ┃ ┣ 📜main.tf
 ┃ ┃ ┃ ┣ 📜outputs.tf
 ┃ ┃ ┃ ┗ 📜variables.tf
 ┃ ┃ ┗ 📂vm
 ┃ ┃ ┃ ┣ 📜main.tf
 ┃ ┃ ┃ ┣ 📜outputs.tf
 ┃ ┃ ┃ ┣ 📜startup.sh
 ┃ ┃ ┃ ┗ 📜variables.tf
 ┃ ┣ 📜.terraform.lock.hcl
 ┃ ┣ 📜enable_apis.tf
 ┃ ┣ 📜main.tf
 ┃ ┣ 📜outputs.tf
 ┃ ┣ 📜providers.tf
 ┃ ┣ 📜terraform.tfstate
 ┃ ┣ 📜terraform.tfstate.backup
 ┃ ┣ 📜terraform.tfvars
 ┃ ┗ 📜variables.tf
 ┣ 📂tests
 ┃ ┗ 📜sample.json
 ┣ 📂validation
 ┃ ┗ 📜validate_data.py
 ┣ 📜.gitignore
 ┣ 📜docker-compose.yml
 ┣ 📜Makefile
 ┣ 📜README.md
 ┣ 📜requirements.txt
 ┗ 📜wait-for-kafka.sh
```

---

## ⚡ Pipeline Execution

### 🚀 Using Makefile

```bash
# Start Docker containers and producer/consumer
make run-producer
make run-consumer

# Submit Spark transformation job manually
make submit-spark-job

# Validate latest day's data
make validate

# Run full workflow (useful for testing end-to-end)
make run-all
```

### 🌬️ Trigger via Airflow

1. Run the Airflow webserver:
```bash
airflow webserver
```

2. Run the scheduler:
```bash
airflow scheduler
```

3. Open the Airflow UI at `http://<vm_ip>:8080` and trigger the `crypto_streaming_pipeline` DAG.

---

## 🚧 Terraform Infrastructure Setup

```bash
cd terraform
terraform init
terraform apply -auto-approve
```

This provisions:
- GCE VM for Airflow and Spark
- Service accounts and IAM roles
- GCS bucket

---

## 🔹 BigQuery Table: `crypto_streaming.prices`

- Partitioned by `DATE(time)`
- Schema:
  - `symbol` (STRING)
  - `priceUsd` (FLOAT)
  - `time` (TIMESTAMP)

---

## 📊 Dashboard in Looker Studio

Dashboard contains:
- **Bar Chart**: Number of records on cloud
- **Bar Chart**: Average price by crypto symbol
- **Time Series Line Chart**: Price evolution over time

Title: `Real-Time Crypto Streaming Dashboard`

> Link to the dashboard: [reports\Looker_Studio_Reporting_-_4_14_25,_3_48 PM.pdf]

---

## 🔍 Future Improvements

- Add DBT for transformation versioning
- Setup CI/CD using GitHub Actions for DAG and script deployment

---

## 🚀 Author

**Konstantinos Soufleros**
- GitHub: [@kostas696](https://github.com/kostas696)
- Email: soufleros.kostas@gmail.com

---

> This project is part of the Data Engineering Zoomcamp course by DataTalksClub.

