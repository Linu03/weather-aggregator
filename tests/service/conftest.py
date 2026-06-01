import pytest

from tests.support.app_client import clear_test_client, create_test_client
from tests.support.infrastructure import PostgresInfrastructure, ensure_docker_available


@pytest.fixture(scope="session")
def postgres_infrastructure():
    try:
        ensure_docker_available()
    except RuntimeError as exc:
        pytest.skip(str(exc))

    infra = PostgresInfrastructure()
    infra.start()
    yield infra
    infra.stop()


@pytest.fixture
def client(postgres_infrastructure):
    postgres_infrastructure.truncate_readings()
    test_client = create_test_client(postgres_infrastructure.connection_params())
    yield test_client
    clear_test_client()
