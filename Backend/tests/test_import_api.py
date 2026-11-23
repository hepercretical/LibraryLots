from fastapi.testclient import TestClient

from library_lots.api import app as api
from library_lots.steam.importer import ImportErrorState

client = TestClient(api.app)


def test_import_endpoint_returns_normalized_rows(monkeypatch):
    monkeypatch.setattr(
        api,
        "import_library",
        lambda _: {
            "steamid": "76561198000000000",
            "name": "Synthetic",
            "imported_at": "time",
            "games": [{"appid": 1, "name": "Example", "playtime_forever": 0}],
            "partial": False,
            "reported_count": 1,
        },
    )
    response = client.post("/api/library/import", json={"profile": "synthetic"})
    assert response.status_code == 200
    row = response.json()["games"][0]
    assert row["playtime_minutes"] == 0 and row["current_price_minor"] is None


def test_import_errors_return_only_safe_codes(monkeypatch):
    def fail(_):
        raise ImportErrorState("rate_limited")

    monkeypatch.setattr(api, "import_library", fail)
    response = client.post("/api/library/import", json={"profile": "synthetic"})
    assert response.status_code == 429
    assert response.json() == {"detail": "rate_limited"}
