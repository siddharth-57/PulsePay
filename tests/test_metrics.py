# This File Verifies that the monitoring endpoint is reachable.
from tests.conftest import client

def test_metrics_endpoint():

    response = client.get("/metrics/")

    assert response.status_code == 200