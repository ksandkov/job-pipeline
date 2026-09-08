"""Health endpoints. /healthz never touches the DB; /readyz does."""

from fastapi.testclient import TestClient

from jobpipeline.main import create_app


def test_healthz_ok():
    client = TestClient(create_app())
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
