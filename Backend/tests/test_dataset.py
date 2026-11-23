import polars as pl
import json
from pathlib import Path

from library_lots.analysis.dataset import SCHEMA, normalize


def test_normalization_preserves_zero_null_and_partial():
    frame, partial = normalize(
        [
            {"appid": 1, "name": "Played", "playtime_forever": 120, "playtime_2weeks": 0},
            {"appid": 2, "name": "Unplayed", "playtime_forever": 0},
            {"appid": 3, "name": "Unknown", "playtime_forever": -1},
            {"appid": 2, "name": "Duplicate", "playtime_forever": 30},
            {"appid": "bad"},
        ],
        "2026-11-18T00:00:00Z",
    )
    assert frame.schema == pl.Schema(SCHEMA)
    assert frame["appid"].to_list() == [1, 2, 3]
    assert frame["playtime_minutes"].to_list() == [120, 0, None]
    assert frame["recent_minutes"].to_list() == [0, None, None]
    assert frame["current_price_minor"].to_list() == [None, None, None]
    assert partial


def test_empty_has_typed_schema_and_preserves_partial():
    frame, partial = normalize([], "time", True)
    assert frame.schema == pl.Schema(SCHEMA)
    assert frame.height == 0 and partial


def test_synthetic_fixture_has_checkable_examples():
    path = Path(__file__).resolve().parents[2] / "Data" / "fixtures" / "library_v1.json"
    games = json.loads(path.read_text(encoding="utf-8"))["games"]
    assert sum(game["playtime_minutes"] or 0 for game in games) == 240
    assert games[0]["current_price_minor"] / (games[0]["playtime_minutes"] / 60) == 1500
    assert games[4]["current_price_minor"] / (games[4]["playtime_minutes"] / 60) == 1500
    assert games[1]["current_price_minor"] == 0 and games[2]["playtime_minutes"] == 0
    assert games[3]["playtime_minutes"] is None and len(games[0]["genres"]) == 2
