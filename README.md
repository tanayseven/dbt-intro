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
