# --- ENVIRONMENT SETUP ---

VENV_DIR = .venv
PYTHON = python

# --- PYTHON ENVIRONMENT ---

create-venv:
	$(PYTHON) -m venv $(VENV_DIR)

install-deps:
	$(PYTHON) -m pip install --upgrade pip
	pip install -r requirements.txt

# --- DOCKER SETUP ---

docker-up:
	docker-compose up -d --build

docker-down:
	docker-compose down

rebuild:
	docker-compose down -v
	docker-compose up -d --build

logs:
	docker-compose logs -f

ps:
	docker-compose ps

# --- KAFKA INGESTION ---

run-producer:
	docker-compose up -d producer
	docker-compose logs -f producer

run-consumer:
	docker-compose up -d consumer
	docker-compose logs -f consumer

# --- SPARK JOBS ---

submit-spark-job:
	spark-submit \
	  --jars jars/spark-bigquery-with-dependencies_2.12-0.36.1.jar,jars/gcs-connector-hadoop3-latest.jar \
	  spark_jobs/spark_gcs_to_bq.py

# --- TERRAFORM ---

terraform-init:
	cd terraform && terraform init

terraform-plan:
	cd terraform && terraform plan

terraform-apply:
	cd terraform && terraform apply -auto-approve

terraform-destroy:
	cd terraform && terraform destroy -auto-approve

# --- VALIDATION ---

validate:
	$(PYTHON) validation/validate_data.py

# --- UTILITIES ---

clean-pyc:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

format:
	black .

lint:
	flake8 .

# --- DEFAULT ---

.PHONY: create-venv install-deps docker-up docker-down rebuild logs ps run-producer run-consumer \
	 submit-spark-job terraform-init terraform-plan terraform-apply terraform-destroy \
	 validate clean-pyc format lint