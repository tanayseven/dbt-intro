DBT Intro
=========

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
dbt test
```

```shell
dbt docs generate && dbt docs serve
```
