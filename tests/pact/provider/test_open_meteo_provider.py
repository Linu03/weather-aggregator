import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

import pytest
from pact import Verifier

from pact_data import CONSUMER, FORECAST_RESPONSE, GEOCODING_RESPONSE, PROVIDER

PACT_FILE = Path(__file__).resolve().parent.parent / "pacts" / f"{CONSUMER}-{PROVIDER}.json"


class _OpenMeteoStub(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/v1/search":
            body = json.dumps(GEOCODING_RESPONSE).encode()
        elif path == "/v1/forecast":
            body = json.dumps(FORECAST_RESPONSE).encode()
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)


def test_open_meteo_provider_verification():
    if not PACT_FILE.is_file():
        pytest.skip("Run consumer pact tests first to generate the pact file.")

    server = HTTPServer(("127.0.0.1", 0), _OpenMeteoStub)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    provider_url = f"http://127.0.0.1:{server.server_address[1]}"

    try:
        return_code, logs = Verifier(PROVIDER, provider_url).verify_pacts(str(PACT_FILE))
        assert return_code == 0, logs
    finally:
        server.shutdown()
