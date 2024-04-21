from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def hello_world():
    print("Hello World!")

with DAG(
    'hello_world',
    description='Simple Hello World DAG',
    schedule_interval='0 12 * * *',
    start_date=datetime(2024, 4, 21),
    catchup=False,
    owner_links={'tanay': 'https://github.com/tanayseven'},
):
    PythonOperator(
        task_id='hello_world',
        python_callable=hello_world,
        owner='tanay',
    )
