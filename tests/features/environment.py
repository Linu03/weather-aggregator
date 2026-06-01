import sys
from pathlib import Path

import respx

_REPO_ROOT = Path(__file__).resolve().parents[2]
_BACKEND = _REPO_ROOT / "backend"

if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
if str(_BACKEND) not in sys.path:
    sys.path.insert(0, str(_BACKEND))

from tests.support.app_client import clear_test_client, create_test_client
from tests.support.infrastructure import PostgresInfrastructure


def before_all(context):
    context.infra = PostgresInfrastructure()
    context.infra.start()


def after_all(context):
    context.infra.stop()


def before_scenario(context, scenario):
    context.infra.truncate_readings()
    context.client = create_test_client(context.infra.connection_params())
    respx.mock.__enter__()
    context.last_response = None


def after_scenario(context, scenario):
    respx.mock.__exit__(None, None, None)
    clear_test_client()
