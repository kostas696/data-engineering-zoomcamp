# airflow/Dockerfile
FROM apache/airflow:2.7.2

USER root
RUN apt-get update && apt-get install -y procps && apt-get clean

USER airflow
