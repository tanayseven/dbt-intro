import json
import os
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator
import snowflake.connector
from datetime import datetime


def ingest_data():
    print("Ingesting data...")
    creds = json.loads((Path(os.environ["AIRFLOW_HOME"]) / 'dags' / 'snowflake_creds.json').read_text())
    connection = snowflake.connector.connect(
        user=creds["user"],
        password=creds["password"],
        account=creds["account"],
        database=creds["database"],
        schema=creds["schema"],
    )
    data = connection.cursor().execute(
        """
        select
            *
        from MOVIES.LANDING.MOVIE_METADATA_RAW
        limit 10
        """
    )
    for row in data:
        print(row)
    connection.close()

with DAG(
    'ingest_data',
    description='Ingest data from Snowflake',
    schedule_interval='@daily',
    start_date=datetime(2024, 4, 21),
    catchup=False,
    owner_links={'tanay': 'https://github.com/tanayseven'},
):
    PythonOperator(
        task_id='ingest_data',
        python_callable=ingest_data,
        owner='tanay',
    )