# Library Lots design and behavior specification

## Status and scope

This is the November 16, 2026 planning baseline for the human-requested local
React/Vite and Python application. It does not claim implemented screens, an
approved visual mockup, live endpoint verification or test completion.
All design/functionality is due November 24; see [PLAN.md](PLAN.md).

Read [../AGENTS.md](../AGENTS.md), [STYLE_GUIDE.md](STYLE_GUIDE.md),
[HUMAN.md](HUMAN.md) and human-maintained [EXPECTATIONS.md](EXPECTATIONS.md).
Do not edit EXPECTATIONS.md. SECURE.md and LEGAL.md are excluded from agent work
through November 29 inclusive; first eligible use is November 30.

## Main journey and navigation

Use a small shared shell with Library Lots branding and clear access to:
**Load library**, **Library**, **Statistics**, and **Pick a game**. Views may share
one page or use focused routes; do not add a routing package solely for this list.
The selected public account and import status remain visible. No signup or
application account is part of this scope.

At a narrow width, stack controls and results. Wider screens may place results
beside explanations. Avoid a dashboard full of decorative cards. Make the primary
task loading a library or picking a game easy to find.

## Load library

- A labeled field accepts a SteamID64 or Steam Community profile URL. Examples
  use placeholders, not an unapproved person's account.
- Explain that profile and game-detail visibility determine available results.
  Provide an intentional Load library action and preserve input on errors.
- Parse /profiles/<SteamID64> and /id/<vanity> forms and resolve identity in
  Python. Keep IDs as strings; unsupported ID forms get clear guidance.
- Display profile/library loading separately from metadata enrichment progress.
  Prevent repeated requests and stale results from overwriting a new account.
- Distinguish invalid input, not found, hidden/unavailable game details, a
  confirmed empty visible library, temporary failure and partial data.
  A public profile does not guarantee public game details.
- Refresh updates the snapshot and timestamp. Switching profiles clears prior
  results or labels any retained content explicitly until the new import succeeds.

## Library

Show game name, recorded hours, current Steam price/currency when available, and
available genre/theme labels. Artwork is optional when supplied by Steam; handle
missing images without broken placeholders.

Provide name search, played/unplayed and genre filters and appropriate sorting.
The controls request Python results; the browser does not calculate aggregates,
similarity, cost/hour, filter or sort the analytical dataset itself. Preserve
useful view state during recoverable navigation and offer Reset filters.

Rows need stable AppID identity. A game detail surface may show its source-backed
metadata and a correct external Steam link. Do not invent completion, installation,
purchase, rating, theme or last-played information.

## Statistics

Show Python-computed library count, played/unplayed counts and recorded total hours
for the available dataset. Distinguish missing hours from known zero. Include a
genre/theme playtime summary and a Lets-Plot figure with an equivalent table.

Explain that multi-genre games can contribute to more than one label; the analysis
must document allocation and denominators so grouped results do not silently
appear to equal the account total. Label coverage for missing metadata.

## Pick a game: current-price value opportunity

Ask: **Which played game has the highest current Steam price per recorded hour?**

Use current final individual-game store price divided by lifetime recorded
minutes / 60. Include an active discount if returned. Compare only the selected
region/currency and price basis. Sort descending at full precision; break ties
by normalized game name then AppID, and round only for display.

Beside the result show game, price, currency, region, recorded hours, cost/hour,
price timestamp and: **Based on today's Steam store price and recorded playtime,
not what you paid.** In an older cached snapshot, replace "today's" with
"the retrieved" and show the retrieval date.

For example, a fixture price of USD 30 and 120 recorded minutes yields USD 15/hour.
This is a synthetic arithmetic example, not a current Steam price.

- Zero hours: show **Unplayed** and no numeric cost/hour; keep this group separate.
- Known free price with positive hours: valid zero cost/hour.
- Missing/delisted/regional price or unknown hours: unavailable, with explanation.
- No eligible rows: explain why without manufacturing a winner.
- This metric is a prompt to consider revisiting an owned game; it does not measure
  enjoyment, value as a person, waste, or money that can be recovered by playing.

## Pick a game: similar unplayed recommendations

Ask: **Which unplayed owned games match the genres/themes of played games?**

Candidates must belong to the imported library and have known zero recorded
minutes. Build preference evidence in Python from played games with usable
Steam metadata. Emphasize stronger playtime evidence. Use NumPy for numerical
similarity calculations; record the chosen formula, weighting, normalization,
metadata handling, deterministic ties and version during Plan-09.

Use lifetime playtime and recent playtime where available as evidence. Lifetime
hours alone do not establish session frequency. Do not invent daily sessions or
claim the person likes every game they have played. Themes/tags are optional
source-backed features; genre matches suffice when themes are unavailable.

Show a recommended game, ranked alternatives, shared attributes and played-game
examples explaining each match. Similarity scores are relative analytical scores,
not probabilities of enjoyment. Handle no played games, no unplayed games,
unavailable metadata and no positive matches with an honest explanation. Never
replace an unavailable recommendation with an unlabeled random pick.

## Sources, figures and local operation

Display data source, last import/enrichment time, selected store region/currency
and missing-data coverage near the relevant results. Do not label current prices
as the account's spending, purchase cost or library resale value.

All analysis and analytical plot generation use Python. Lets-Plot output can be
served as a local figure or displayed through a compatible renderer; choose the
delivery format in Plan-10 and keep analytical logic backend-only.
Provide a readable table/text equivalent. Do not add a separate JavaScript
analytics implementation or a frontend analytical chart package.

The frontend and Python server run locally. Live Steam calls need internet.
Cached/fixture views must be explicitly identified and never silently substituted
for a successful import. Test fixtures do not establish live endpoint support.

## Acceptance evidence

Verify loading, partial, empty, unavailable, no matches, error/retry and success
states. Cover narrow/wide layout, long names, large libraries, keyboard navigation,
200% zoom and plot/table agreement. Human visual review and a bounded real Steam
journey are separate from mocked unit/component tests. All are pending until
actually performed and recorded in the owning plan segment.
