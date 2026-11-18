from fastapi.testclient import TestClient

from library_lots.api.app import app


def test_health_endpoint_reports_local_service() -> None:
    response = TestClient(app).get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "library-lots-backend"}
