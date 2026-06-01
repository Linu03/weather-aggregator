from pathlib import Path

import docker
import psycopg2
import pytest
from testcontainers.postgres import PostgresContainer

from adapters.postgres_repo import PostgresWeatherRepo
from db_helper import db_params

PROJECT_ROOT = Path(__file__).resolve().parents[2]
INIT_SQL = PROJECT_ROOT / "init.sql"


@pytest.fixture(scope="session")
def postgres_container():
    try:
        docker.from_env().ping()
    except docker.errors.DockerException:
        pytest.skip("Docker is not running — required for integration tests.")

    with PostgresContainer(
        image="postgres:15-alpine",
        username="weather_user",
        password="weather_pass",
        dbname="weather_db",
    ) as postgres:
        yield postgres


@pytest.fixture(scope="session")
def db_schema(postgres_container):
    params = db_params(postgres_container)
    conn = psycopg2.connect(**params)
    try:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(INIT_SQL.read_text(encoding="utf-8"))
    finally:
        conn.close()
    yield


@pytest.fixture
def repo(postgres_container, db_schema):
    params = db_params(postgres_container)
    conn = psycopg2.connect(**params)
    try:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE weather_reading RESTART IDENTITY")
    finally:
        conn.close()

    yield PostgresWeatherRepo(
        host=params["host"],
        port=params["port"],
        database=params["database"],
        user=params["user"],
        password=params["password"],
    )
