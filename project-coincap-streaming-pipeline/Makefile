# --- ENVIRONMENT SETUP ---

# Set the Python virtual environment directory
VENV_DIR=.venv

# Default Python
PYTHON=python

# --- PYTHON ENVIRONMENT ---

create-venv:
	$(PYTHON) -m venv $(VENV_DIR)

install-deps:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

# --- INGESTION SCRIPTS ---

run-producer:
	$(PYTHON) data_ingestion/coincap_ws_producer.py

# --- CONSUMERS ---

run-consumer:
	$(PYTHON) gcs/kafka_consumer_to_gcs.py

# --- SPARK JOBS ---

submit-spark-job:
	gcloud dataproc jobs submit pyspark spark_jobs/process_to_bigquery.py \
		--cluster=my-dataproc-cluster \
		--region=us-central1 \
		--project=$(shell gcloud config get-value project)

# --- TERRAFORM ---

terraform-init:
	cd terraform && terraform init

terraform-plan:
	cd terraform && terraform plan

terraform-apply:
	cd terraform && terraform apply -auto-approve

terraform-destroy:
	cd terraform && terraform destroy -auto-approve

# --- TESTING ---

test:
	pytest tests/

# --- UTILITIES ---

clean-pyc:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

format:
	black .

lint:
	flake8 .

# --- DEFAULT ---

.PHONY: create-venv install-deps run-producer run-consumer submit-spark-job terraform-init terraform-plan terraform-apply terraform-destroy test clean-pyc format lint
