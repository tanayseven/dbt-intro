FROM apache/airflow:latest
LABEL authors="tanay"

USER root
RUN apt-get update  \
    && apt-get install -y vim git  \
    && apt-get clean

USER airflow
COPY airflow.requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /requirements.txt
