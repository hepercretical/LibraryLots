import pytest

from library_lots.steam.importer import ImportErrorState, import_library, parse_identity

ID = "76561198000000000"


@pytest.mark.parametrize(
    "value, expected",
    [
        (ID, ("steamid", ID)),
        (f"https://steamcommunity.com/profiles/{ID}/", ("steamid", ID)),
        ("https://steamcommunity.com/id/example", ("vanity", "example")),
    ],
)
def test_identity(value, expected):
    assert parse_identity(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        "https://evil.test/id/example",
        "https://x@steamcommunity.com/id/a",
        f"https://steamcommunity.com/profiles/{ID}?x=1",
        "http://steamcommunity.com/id/a",
        "https://steamcommunity.com/id/a/extra",
        "123",
    ],
)
def test_rejects_invalid_identity(value):
    with pytest.raises(ImportErrorState, match="invalid_input"):
        parse_identity(value)


def test_import_vanity_and_partial_response():
    responses = iter(
        [
            {"success": 1, "steamid": ID},
            {"players": [{"steamid": ID, "communityvisibilitystate": 3}]},
            {"game_count": 2, "games": [{"appid": 1}]},
        ]
    )
    result = import_library("https://steamcommunity.com/id/example", lambda *_: next(responses))
    assert result["steamid"] == ID
    assert result["partial"] is True


@pytest.mark.parametrize(
    "owned, expected",
    [({}, "hidden"), ({"game_count": 0}, None), ({"game_count": 1}, "unavailable")],
)
def test_library_states(owned, expected):
    responses = iter([{"players": [{"steamid": ID, "communityvisibilitystate": 3}]}, owned])
    if expected:
        with pytest.raises(ImportErrorState, match=expected):
            import_library(ID, lambda *_: next(responses))
    else:
        assert import_library(ID, lambda *_: next(responses))["games"] == []
