# --- ENVIRONMENT SETUP ---

VENV_DIR = .venv
PYTHON = python

# --- PYTHON ENVIRONMENT ---

create-venv:
\t$(PYTHON) -m venv $(VENV_DIR)

install-deps:
\t$(PYTHON) -m pip install --upgrade pip
\tpip install -r requirements.txt

# --- DOCKER SETUP ---

docker-up:
\tdocker-compose up -d --build

docker-down:
\tdocker-compose down

docker-clean:
\tdocker-compose down -v --remove-orphans

rebuild:
\tdocker-compose down -v
\tdocker-compose up -d --build

logs:
\tdocker-compose logs -f

ps:
\tdocker-compose ps

# --- KAFKA INGESTION ---

run-producer:
\tdocker-compose up -d producer
\tdocker-compose logs -f producer

run-consumer:
\tdocker-compose up -d consumer
\tdocker-compose logs -f consumer

# --- SPARK JOBS ---

submit-spark-job:
\tspark-submit \\
\t  --jars jars/spark-bigquery-with-dependencies_2.12-0.36.1.jar,jars/gcs-connector-hadoop3-latest.jar \\
\t  spark_jobs/spark_gcs_to_bq.py

# --- FULL PIPELINE RUN ---

run-all: docker-up wait submit-spark-job validate

wait:
\t@echo "⏳ Waiting 60 seconds for data to land in GCS..."
\tsleep 60
\t@echo "⏳ Waiting 60 seconds for data to be processed by Spark..."
\tsleep 60
\t@echo "⏳ Waiting 60 seconds for data to be ingested into BigQuery..."
\tsleep 60
\t@echo "⏳ Waiting 60 seconds for data to be validated..."
\tsleep 60

# --- AIRFLOW TASKS ---

trigger-dag:
\tairflow dags trigger crypto_streaming_pipeline

airflow-ui:
\tairflow webserver --port 8080

airflow-scheduler:
\tairflow scheduler

# --- FULL LOCAL WORKFLOW ---

full-local: terraform-apply docker-up trigger-dag

hard-reset:
\tmake terraform-destroy
\tmake terraform-apply
\tmake rebuild
\tmake trigger-dag

# --- TERRAFORM ---

terraform-init:
\tcd terraform && terraform init

terraform-plan:
\tcd terraform && terraform plan

terraform-apply:
\tcd terraform && terraform apply -auto-approve

terraform-destroy:
\tcd terraform && terraform destroy -auto-approve

# --- VALIDATION ---

validate:
\t$(PYTHON) validation/validate_data.py

# --- UTILITIES ---

clean-pyc:
\tfind . -name "*.pyc" -delete
\tfind . -name "__pycache__" -delete

format:
\tblack .

lint:
\tflake8 .

# --- DEFAULT ---

.PHONY: create-venv install-deps docker-up docker-down docker-clean rebuild logs ps run-producer run-consumer \\
\tsubmit-spark-job terraform-init terraform-plan terraform-apply terraform-destroy \\
\tvalidate clean-pyc format lint trigger-dag airflow-ui airflow-scheduler full-local hard-reset