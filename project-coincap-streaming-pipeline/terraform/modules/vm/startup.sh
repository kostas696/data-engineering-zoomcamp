#!/bin/bash

# Update & install Python and pip
sudo apt-get update -y
sudo apt-get install -y python3-pip

# Install Airflow 
pip3 install apache-airflow

# Optional: start Airflow webserver and scheduler (you may want to daemonize later)
airflow db init
airflow users create --username admin --firstname Admin --lastname User --role Admin --email admin@example.com --password admin
airflow webserver -p 8080 &
airflow scheduler &
