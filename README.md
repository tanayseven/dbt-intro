DBT Movie Recommendation System
================================

### Setup

```shell
export PYTHONPATH=$PWD # in project root
```

```shell
cd alembic
python populate_alembic.py
```

### Alembic commands

```shell
alembic history
```

```shell
alembic revision --autogenerate -m "initial tables"
```

```shell
alembic upgrade head
```

```shell
alembic downgrade base
```

### DBT commands

```shell
dbt run
```

```shell
dbt seed
```

```shell
dbt test
```

```shell
dbt docs generate && dbt docs serve
```

### Airflow on local commands

#### Run Airflow in Docker compose

```shell
docker-compose up
```

#### Get the admin password for Airflow

```shell
docker exec -it dbt-intro-airflow-1 cat standalone_admin_password.txt && echo
```

#### Copy DBT project to DAGs folder

```shell
cp -r ./dbt_intro/ ./airflow/dags/
```

## Run recommendation engine and generate recommendations

```shell
python -m recommendation_system.train # make sure the table is deleted before running this
```
