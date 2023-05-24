DBT Intro
=========

```shell
export PYTHONPATH=$PWD
```

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