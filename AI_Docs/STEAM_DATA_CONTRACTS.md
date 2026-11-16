# Steam data contracts

## Plan-01 review record

Reviewed November 16, 2026, using America/Denver dates. This record captures
the contracts and limits needed by later implementation plans. It does not
claim a successful live library import. No Steam key, profile URL, SteamID,
personal record, or account snapshot is stored here.

## Accepted profile inputs

The importer will accept these forms and preserve the resolved SteamID64 as a
string at every application boundary:

- A SteamID64 string containing exactly 17 decimal digits.
- `https://steamcommunity.com/profiles/<SteamID64>/`, with an optional trailing
  slash and no query or fragment.
- `https://steamcommunity.com/id/<vanity>/`, with an optional trailing slash;
  the non-empty vanity segment is resolved by Steam before any player lookup.

The parser will reject other hosts, arbitrary URLs, embedded credentials,
missing path segments, non-decimal `/profiles/` values, and extra path/query
components. A profile URL is input syntax only; the backend calls fixed Steam
endpoints and does not fetch an arbitrary address supplied by the user.

## Official Web API contract

The official public host is `https://api.steampowered.com`. Valve's Web API
overview says that methods with access restrictions require a Web API key and
that requests should use HTTPS. Steam service interfaces use the `input_json`
parameter when the method accepts structured arguments.

| Need | Official method | Key | Relevant request fields | Expected useful response shape |
| --- | --- | --- | --- | --- |
| Vanity resolution | `ISteamUser/ResolveVanityURL/v1/` | User Web API key | `vanityurl`, optional `url_type=1` | `response.success`, and on success `response.steamid` |
| Profile summary | `ISteamUser/GetPlayerSummaries/v2/` | User Web API key | `steamids` (comma-delimited, max 100) | `response.players[]`, including string-like `steamid`, `personaname`, `profileurl`, `communityvisibilitystate` |
| Owned library | `IPlayerService/GetOwnedGames/v1/` | User Web API key | `steamid`, `include_appinfo=true`, `include_played_free_games=true` | `response.game_count`, `response.games[]`; game rows include `appid`, `name`, `playtime_forever` minutes and, when present, icon/hash fields |
| Recent playtime | `IPlayerService/GetRecentlyPlayedGames/v1/` | User Web API key | `steamid`, optional bounded `count` | `response.total_count`, `response.games[]`; rows include `appid`, `name`, `playtime_2weeks` minutes and often lifetime minutes |

The key is a user Web API key, not a publisher-only key. It must stay in
backend-only ignored configuration. The frontend never receives or constructs
key-bearing URLs. The backend will use bounded timeouts, request counts and
retries, and will classify a missing `response` or an HTTP/API error rather
than treating it as an empty library.

Steam documents that `GetOwnedGames` returns games only when the user's owned
games/game details are visible to the caller. Free games are excluded by
default unless `include_played_free_games` is enabled. Therefore hidden game
details, an unavailable response, and a genuinely visible empty library are
different states. Missing playtime is nullable and never converted to zero.

Official references:

- [Web API overview](https://partner.steamgames.com/doc/webapi_overview)
- [IPlayerService](https://partner.steamgames.com/doc/webapi/IPlayerService)
- [ISteamUser](https://partner.steamgames.com/doc/webapi/ISteamUser)

## Store prices and metadata

Valve's documented `IStoreService` is an official Steam Web API service for
public Store information. Its documented `GetAppList` method requires any Web
API key, returns a bounded list, and exposes app IDs plus modification/price
change indicators. It is not a per-AppID price-and-genre lookup suitable by
itself for enrichment.

For the needed per-owned-AppID lookup, the candidate is:

`GET https://store.steampowered.com/api/appdetails?appids=<AppID>&cc=<country>&l=<language>`

This Store JSON endpoint is public and commonly returns a keyed object such as:

```json
{
  "440": {
    "success": true,
    "data": {
      "type": "game",
      "steam_appid": 440,
      "name": "<store name>",
      "is_free": true,
      "price_overview": {
        "currency": "USD",
        "initial": 0,
        "final": 0,
        "discount_percent": 0,
        "final_formatted": "Free"
      },
      "genres": [{"id": "1", "description": "<genre>"}]
    }
  }
}
```

The example is a redacted field-shape example, not a saved live response. The
consumer must check the per-AppID `success` flag before reading `data` and must
allow absent or null fields. Paid apps commonly expose `price_overview.initial`
and `final` as integer minor units plus `currency`, discount percentage and
formatted values. A free app may have `is_free=true` and no `price_overview`;
that is a confirmed zero only when the response explicitly says it is free.
Missing, delisted, age-gated, or region-blocked data is unknown, not zero.

`cc` selects the requested store country/region and the returned currency is
authoritative for that response. Plan-06 must select and display one region and
currency per comparison, store the price basis (final individual-game price,
including an active discount when returned), and record retrieval time. It must
not infer the user's region, convert currencies, use bundle prices, or imply
purchase history. Store responses are snapshots, not proof of what a person
paid.

The per-AppID `appdetails` endpoint is a public Steam Store endpoint, but Valve
does not provide a stable official API reference for its response contract in
the reviewed `IStoreService` documentation. It is therefore an explicitly
undocumented dependency: isolate it behind an adapter, request only needed
AppIDs, cache briefly, handle shape changes/rate limits, and make partial
enrichment visible. `genres` are source-backed when present. Themes/tags are
optional and must not be assumed from this endpoint; later plans must either
use an additional public Steam source after a separate check or proceed with
genres only. No third-party provider is approved.

## Verification record

- Official documentation was reviewed for the Web API host, authentication,
  service-interface calling convention, vanity resolution, player summaries,
  owned games, recent playtime, and `IStoreService/GetAppList`.
- The human supplied a SteamID64 for the bounded check. The identifier is
  intentionally not repeated in this project record. The profile summary call
  returned HTTP 200 with one player, `communityvisibilitystate=3`,
  `profilestate=1`, and a profile URL. This confirms the selected account was
  reachable and publicly visible for the check without recording personal
  profile fields.
- The key-backed `GetOwnedGames` call returned HTTP 200 with a response,
  `game_count=131`, and 131 rows. A sanitized shape check confirmed `appid`,
  `name`, and `playtime_forever` fields on a returned row. The
  `GetRecentlyPlayedGames` call returned HTTP 200 with `total_count=3` and
  three rows. Counts are verification evidence only; no game names or records
  are stored here.
- The bounded Store `appdetails` call for one known public AppID returned HTTP
  200 with `success=true`, `data`, `price_overview.currency=USD`, a final-price
  field, and at least one genre. This confirms the tested response shape for
  the selected US region. It does not establish that every AppID or region
  will have price or genre data.
- The first attempts through the restricted environment's proxy failed before
  receiving HTTP responses. An approved proxy-bypassed retry succeeded. The
  key was never printed, logged, or stored in this document; it was read only
  from ignored `Backend/.env` for the bounded requests.
- The check used no Steam password and did not request or save a profile
  snapshot. Future calls must retain the same backend-only key handling,
  bounded request policy, and honest missing/private-data states.
