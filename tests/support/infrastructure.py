from pathlib import Path

import docker
import psycopg2
from testcontainers.postgres import PostgresContainer

PROJECT_ROOT = Path(__file__).resolve().parents[2]
INIT_SQL = PROJECT_ROOT / "init.sql"


def db_params(container: PostgresContainer) -> dict:
    return {
        "host": container.get_container_host_ip(),
        "port": int(container.get_exposed_port(5432)),
        "database": container.dbname,
        "user": container.username,
        "password": container.password,
    }


def ensure_docker_available() -> None:
    try:
        docker.from_env().ping()
    except docker.errors.DockerException as exc:
        raise RuntimeError("Docker is not running — required for tests.") from exc


class PostgresInfrastructure:
    """Shared Postgres Testcontainers setup for pytest service tests and Behave."""

    def __init__(self) -> None:
        self._container_cm = None
        self.container: PostgresContainer | None = None

    def start(self) -> None:
        ensure_docker_available()
        self._container_cm = PostgresContainer(
            image="postgres:15-alpine",
            username="weather_user",
            password="weather_pass",
            dbname="weather_db",
        )
        self.container = self._container_cm.__enter__()
        conn = psycopg2.connect(**db_params(self.container))
        try:
            conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute(INIT_SQL.read_text(encoding="utf-8"))
        finally:
            conn.close()

    def stop(self) -> None:
        if self._container_cm is not None:
            self._container_cm.__exit__(None, None, None)
            self._container_cm = None
            self.container = None

    def truncate_readings(self) -> None:
        if self.container is None:
            raise RuntimeError("Postgres infrastructure is not started.")
        conn = psycopg2.connect(**db_params(self.container))
        try:
            conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute("TRUNCATE TABLE weather_reading RESTART IDENTITY")
        finally:
            conn.close()

    def connection_params(self) -> dict:
        if self.container is None:
            raise RuntimeError("Postgres infrastructure is not started.")
        return db_params(self.container)
