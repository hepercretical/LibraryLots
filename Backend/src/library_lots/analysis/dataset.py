"""Version 1 normalized owned-game dataset.

Malformed identifiers and duplicate AppIDs are omitted and mark the import partial;
the first valid occurrence wins. Invalid or missing playtime remains null, never
zero. Enrichment fields are nullable until supplied by a later source adapter.
No account snapshots are persisted.
"""

import polars as pl

SCHEMA = {
    "appid": pl.Int64,
    "name": pl.String,
    "playtime_minutes": pl.Int64,
    "recent_minutes": pl.Int64,
    "source": pl.String,
    "imported_at": pl.String,
    "current_price_minor": pl.Int64,
    "currency": pl.String,
    "region": pl.String,
    "price_basis": pl.String,
    "price_retrieved_at": pl.String,
    "genres": pl.List(pl.String),
    "themes": pl.List(pl.String),
    "enrichment_status": pl.String,
}


def _nonnegative(value):
    return (
        value
        if isinstance(value, int)
        and not isinstance(value, bool)
        and 0 <= value <= 9223372036854775807
        else None
    )


def normalize(games: list, imported_at: str, partial: bool = False) -> tuple[pl.DataFrame, bool]:
    rows = []
    seen = set()
    for game in games:
        if not isinstance(game, dict):
            partial = True
            continue
        appid = _nonnegative(game.get("appid"))
        if appid is None or appid == 0 or appid > 4294967295 or appid in seen:
            partial = True
            continue
        seen.add(appid)
        name = game.get("name")
        lifetime = _nonnegative(game.get("playtime_forever"))
        recent = _nonnegative(game.get("playtime_2weeks"))
        if lifetime is None or not isinstance(name, str) or not name.strip():
            partial = True
        rows.append(
            {
                "appid": appid,
                "name": name if isinstance(name, str) and name.strip() else None,
                "playtime_minutes": lifetime,
                "recent_minutes": recent,
                "source": "Steam Web API: IPlayerService/GetOwnedGames/v1",
                "imported_at": imported_at,
                "current_price_minor": None,
                "currency": None,
                "region": None,
                "price_basis": None,
                "price_retrieved_at": None,
                "genres": None,
                "themes": None,
                "enrichment_status": "not_requested",
            }
        )
    return pl.DataFrame(rows, schema=SCHEMA), partial
