from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    'dbt_seed',
    description='Runs DBT seed',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    owner_links={'tanay': 'https://github.com/tanayseven'},
):
    BashOperator(
        task_id='dbt_seed',
        bash_command="cd $AIRFLOW_HOME/dags/dbt_intro/ && dbt seed",
        owner='tanay',
    )
