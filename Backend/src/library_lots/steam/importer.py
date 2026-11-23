"""Bounded public Steam imports. Request URLs and upstream errors are never exposed."""

import json
import os
import re
import threading
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, build_opener

from dotenv import load_dotenv

BASE = "https://api.steampowered.com/"
_lock = threading.Lock()
_day = ""
_calls = 0
MAX_DAILY_CALLS = 1000


class ImportErrorState(Exception):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


def parse_identity(value: str) -> tuple[str, str]:
    value = value.strip()
    if re.fullmatch(r"[0-9]{17}", value):
        return "steamid", value
    try:
        url = urlsplit(value)
        if (
            url.scheme != "https"
            or url.netloc.lower() != "steamcommunity.com"
            or url.query
            or url.fragment
        ):
            raise ValueError
        match = re.fullmatch(r"/(profiles|id)/([A-Za-z0-9_-]+)/?", url.path)
        if not match:
            raise ValueError
        kind, identifier = match.groups()
        if kind == "profiles" and not re.fullmatch(r"[0-9]{17}", identifier):
            raise ValueError
        return ("steamid" if kind == "profiles" else "vanity"), identifier
    except ValueError:
        raise ImportErrorState("invalid_input") from None


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def request_steam(path: str, params: dict) -> dict:
    """One HTTPS request, no redirects or retries; cap calls per process per day."""
    global _day, _calls
    load_dotenv(Path(__file__).resolve().parents[3] / ".env")
    key = os.environ.get("STEAM_WEB_API_KEY", "")
    if not key or key == "replace-with-your-steam-web-api-key":
        raise ImportErrorState("configuration")
    with _lock:
        today = datetime.now(timezone.utc).date().isoformat()
        if today != _day:
            _day, _calls = today, 0
        if _calls >= MAX_DAILY_CALLS:
            raise ImportErrorState("rate_limited")
        _calls += 1
    url = BASE + path + "?" + urlencode({"key": key, **params})
    try:
        with build_opener(NoRedirect()).open(url, timeout=10) as response:
            payload = response.read(10_000_001)
        if len(payload) > 10_000_000:
            raise ImportErrorState("unavailable")
        data = json.loads(payload)
        if not isinstance(data, dict) or not isinstance(data.get("response"), dict):
            raise ImportErrorState("unavailable")
        return data["response"]
    except HTTPError as exc:
        raise ImportErrorState("rate_limited" if exc.code == 429 else "unavailable") from None
    except (URLError, TimeoutError, ValueError, OSError):
        raise ImportErrorState("unavailable") from None


def import_library(value: str, request=request_steam) -> dict:
    kind, identity = parse_identity(value)
    if kind == "vanity":
        resolved = request("ISteamUser/ResolveVanityURL/v1/", {"vanityurl": identity})
        if resolved.get("success") != 1:
            raise ImportErrorState("not_found")
        identity = str(resolved.get("steamid", ""))
        if not re.fullmatch(r"[0-9]{17}", identity):
            raise ImportErrorState("unavailable")
    profile = request("ISteamUser/GetPlayerSummaries/v2/", {"steamids": identity})
    players = profile.get("players")
    if not isinstance(players, list):
        raise ImportErrorState("unavailable")
    if not players:
        raise ImportErrorState("not_found")
    player = players[0]
    if not isinstance(player, dict) or str(player.get("steamid")) != identity:
        raise ImportErrorState("unavailable")
    if player.get("communityvisibilitystate") != 3:
        raise ImportErrorState("hidden")
    owned = request(
        "IPlayerService/GetOwnedGames/v1/",
        {"steamid": identity, "include_appinfo": "true", "include_played_free_games": "true"},
    )
    if "game_count" not in owned:
        raise ImportErrorState("hidden")
    count = owned["game_count"]
    games = owned.get("games", [] if count == 0 else None)
    if (
        not isinstance(count, int)
        or isinstance(count, bool)
        or count < 0
        or not isinstance(games, list)
    ):
        raise ImportErrorState("unavailable")
    return {
        "steamid": identity,
        "name": player.get("personaname") or "Steam profile",
        "games": games,
        "reported_count": count,
        "partial": count != len(games),
        "imported_at": datetime.now(timezone.utc).isoformat(),
    }
