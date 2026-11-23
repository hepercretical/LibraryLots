- [ ] The final project must include at least 1 dataset.
- [ ] Software written in Python analyzes and answers two questions about the data.
- [ ] At least 1 use of a filter.
- [ ] At least 1 use of a sort.
- [ ] At least one use of aggregation.

# Library Lots numbered delivery plan

All five boxes above must be completed and verified by **November 24, 2026
(11/24/2026)**. They are requirements, not claims of completed work.

## Delivery contract

One sprint delivers a complete local React/Vite application with a Python
backend. All design and functionality must be complete by November 24 and ready
for local use and final testing that day. Target feature integration November 23
to leave November 24 for the handoff, final tests and corrections. These targets
are a proposed work sequence within the human's deadline, not evidence of capacity
or completed implementation. Raise blockers early; only the human can change scope.

No hosting, database, Neon or Netlify work is included. Live imports use public
Steam accounts via Steam's official Web API, supplemented by free public Steam
data/API endpoints for prices and metadata. Do not download the entire Steam
catalog just to enrich one account.

**SECURE.md and LEGAL.md are dormant and must not be read or used in agent work
through November 29 inclusive. Their first eligible use is November 30, 2026
(America/Denver).** The current authorized rewrite is the only exception.
The November 24 milestone has no acceptance gates drawn from those documents.
AGENTS.md's independent workflow and secret-handling rules remain active.

Read the human-maintained [EXPECTATIONS.md](EXPECTATIONS.md) before implementing
a segment. Do not edit it. Resolve new requirements with the human; do not assume
an incomplete expectations document grants new scope.

## Daily schedule: November 16-24, 2026

Each calendar day below has at least one numbered plan and a concrete expected
outcome. Dates use America/Denver. Follow dependencies within each day, and include
the owning segment's tests and data/error states in that day's work. This table
summarizes the detailed acceptance criteria below; it does not mark work complete
or authorize implementation outside the human's requested task.

| Date | Numbered plans | Expected outcome by the end of the day |
| --- | --- | --- |
| 11/16/2026 | Plan-01, Plan-02 | Confirm Steam contracts, scaffold the local services and verify their connection. |
| 11/17/2026 | Plan-03 | Review the complete screen/interaction design. |
| 11/18/2026 | Plan-04, Plan-05 | Import a public Steam library and normalize it into a typed analysis dataset with repeatable synthetic tests. |
| 11/19/2026 | Plan-06 | Enrich owned games with current Steam prices and available genres/themes, including region/currency, coverage and retry behavior. |
| 11/20/2026 | Plan-07, Plan-08 | Complete Python cost-per-hour ranking and playtime/preference aggregates, with verified filters, sorts and aggregation. |
| 11/21/2026 | Plan-09, Plan-10 | Complete explainable NumPy-based unplayed-game ranking and Python-generated Lets-Plot figures with matching tables. |
| 11/22/2026 | Plan-11, Plan-12 | Complete the library/statistics interface and both game-picking journeys, including filters, explanations and recovery states. |
| 11/23/2026 | Plan-13 | Integrate and verify the full local app, finish all design/functionality, and freeze features for the final handoff. |
| 11/24/2026 | Plan-14 | Deliver the functional local app ready for use and final testing; complete human review, regression fixes and requirement evidence. |

At each daily handoff, compare actual results with the assigned acceptance
criteria and report blockers and remaining work. If dependencies or effort put
November 24 at risk, ask the human for a scope/timing decision immediately; do not
silently defer required features or replace live functionality with mock results.
The five requirements at the top remain due November 24. Plan-15 is outside this
nine-day schedule and cannot move deferred-document work into these dates.

## Required analytical answers and evidence

1. **Which owned game has the highest current Steam store price per recorded
   hour played?** This identifies a game to consider revisiting. It measures
   current-price cost per hour, not actual spending or subjective enjoyment.
2. **Which owned, unplayed games most closely match the genres/themes of played
   games, with stronger evidence from frequently played games?** Explain matches
   using available metadata and playtime; never promise enjoyment.

| Required technique | Planned use | Verification |
| --- | --- | --- |
| Dataset | Normalized imported Steam library joined by AppID to Steam metadata | Typed schema, provenance, timestamps and repeatable synthetic fixture |
| Python analysis | Both questions and supporting statistics in Polars/NumPy | Known-answer Python tests and working local UI |
| Filter | Unplayed candidates; played games with usable prices for value ranking | Explicit Polars filter and boundary tests |
| Sort | Descending cost/hour and descending recommendation scores | Stable ordering and tie tests |
| Aggregation | Total hours and playtime grouped by genre/theme | Explicit Polars aggregation with known totals |
| Lets-Plot | Value ranking and preference summary charts | Python-generated figures matching result tables |

The imported dataset is required for real functionality. A clearly labeled
synthetic dataset supports repeatable tests; it does not prove live import.
All acceptance criteria below begin unchecked. Record actual commands, test
results, limitations and human reviews when work is requested and verified.

## Plan-01: Confirm Steam data contracts

**Target:** November 16, 2026. **Dependencies:** none.

Official starting references: [Web API overview](https://partner.steamgames.com/doc/webapi_overview),
[IPlayerService](https://partner.steamgames.com/doc/webapi/IPlayerService),
[ISteamUser](https://partner.steamgames.com/doc/webapi/ISteamUser) and
[IStoreService](https://partner.steamgames.com/doc/webapi/IStoreService).
The documentation review does not establish a successful live library/metadata
import. Verify actual endpoint responses during this segment.

- [x] Record the supported input forms: SteamID64 string and Steam Community
      /profiles/<SteamID64> or /id/<vanity> profile URL.
- [x] Identify public Web API methods for vanity resolution, player summaries,
      owned games and optional recent playtime; use the public host with a user
      key where required, not publisher-only access.
- [x] Verify the free public Steam metadata endpoint(s) for current prices,
      genres and any themes/tags before making downstream assumptions.
- [x] Record sample field shapes, response limitations, region/currency and
      missing-price/metadata behavior without exposing keys or personal records.
- [x] Record which endpoints are officially documented and which are public
      Steam Store endpoints without a verified stable documentation contract.
      Do not describe endpoint availability as proven until checked.
- [x] Confirm an accessible public account for a bounded live check with the
      human during implementation; never request a Steam password.

## Plan-02: Scaffold the local development environment

**Target:** November 16, 2026. **Dependencies:** Plan-01 contracts.

- [x] Create React/Vite frontend and a small Python HTTP backend with separate
      dev processes; select framework, Python version and dependencies explicitly.
- [x] Include Polars, NumPy, lets-plot, pytest and reviewed lint/format tools in
      repeatable Python dependency configuration and an isolated .venv.
- [x] Provide all frontend scripts listed in AGENTS.md, lockfile, test setup
      and matching ESLint/Prettier configuration.
- [x] Document exact install, dev, test, lint, format and build commands in
      project guidance or package configuration, leaving README.md untouched.
- [x] Keep services local, route frontend requests to the Python API, and provide
      safe placeholder-only environment examples and appropriate ignore coverage.
- [x] Verify a frontend-to-backend health request; do not add a database or hosting.

Verification completed November 16, 2026; commands, results and limitations are
recorded in [DEVELOPMENT.md](../DEVELOPMENT.md#plan-02-verification-november-16-2026).

## Plan-03: Design the complete user journey

**Target:** November 17, 2026. **Dependencies:** Plan-01.

- [x] Design import, library, statistics, value ranking and unplayed recommendation
      views with all loading/validation/empty/error/partial/success states.
- [x] Define navigation, profile switching, refresh and back behavior, preserving
      useful filters without showing one profile's results as another's.
- [x] Define responsive tables/lists, shared controls, design tokens and readable
      chart/table equivalents using DESIGN.md, STYLE_GUIDE.md and HUMAN.md.
- [x] Human reviews the proposed main journey and visual direction; record
      feedback without claiming an unperformed review.

On November 18 the human approved the proposed journey, profile-switching
behavior, palette and responsive direction in [the design proposal](../PLAN_03_DESIGN_PROPOSAL.md).
The proposal was subsequently expanded with a view-state matrix and concrete
error and chart tokens. Those additions have not had a separate human review;
no visual browser review is claimed. Text color contrast was calculated for
the proposed primary, muted, error and secondary-chart pairings; rendered
contrast and responsive behavior remain implementation checks.

## Plan-04: Import public Steam accounts

**Target:** November 18, 2026. **Dependencies:** Plan-02, Plan-03.

- [x] Accept SteamID64 and both profile URL forms, resolve vanity names through
      Steam and preserve identity values as strings.
- [x] Fetch public profile/library information through backend Steam adapters.
      Keep requests bounded and keys backend-only.
- [x] Handle invalid input, unresolved users, hidden game details, unavailable
      responses, rate limiting and genuinely empty visible libraries distinctly.
- [x] Prevent duplicate refresh requests and stale-response overwrites when
      changing accounts; provide progress, cancel/recovery and retry as appropriate.
- [x] Tests mock Steam responses; a separately recorded live check verifies the
      chosen public account when credentials and connectivity are available.

The November 18 live importer check and its limitations are recorded in
[DEVELOPMENT.md](../DEVELOPMENT.md#public-library-import-and-dataset). Mocked
backend and frontend tests passed; this check did not verify store enrichment.

## Plan-05: Build the normalized analysis dataset

**Target:** November 18, 2026. **Dependencies:** Plan-04.

- [x] Define one row per AppID for the selected account with known playtime in
      minutes, nullable recent playtime and source/import timestamps.
- [x] Define join fields for nullable current price, currency, region, price
      basis, genres/themes and enrichment status; preserve missing versus zero.
- [x] Normalize types with Polars; specify duplicate/malformed-row handling and
      distinguish a partial import from a complete available response.
- [x] Add a documented synthetic fixture with manually checkable answers, covering
      played/unplayed games, missing data, free games, ties and multiple genres.
- [x] Keep real account snapshots and generated private artifacts out of Git;
      do not silently save long-term account history.

The schema, partial-import policy and fixture are described in
[DEVELOPMENT.md](../DEVELOPMENT.md#public-library-import-and-dataset) and
[Data/fixtures/README.md](../Data/fixtures/README.md). Automated dataset tests
passed on November 18; prices and genres await Plan-06 enrichment.

## Plan-06: Enrich owned games with Steam metadata

**Target:** November 19, 2026. **Dependencies:** Plan-01, Plan-05.

- [ ] Fetch only needed owned AppIDs from verified free public Steam sources.
      Record currency/region, retrieval time and metadata coverage.
- [ ] Use the current final individual-game price, including an active discount
      when returned; do not substitute bundles or historical purchase costs.
- [ ] Preserve unavailable/delisted/regional prices as unknown, and confirmed
      free prices as zero. Select an explicit store region; do not infer the
      account owner's region or convert currencies without a separate decision.
- [ ] Use a bounded, expiring metadata cache and bounded concurrency/retries.
      Make partial enrichment visible and retryable.
- [ ] Never invent genres/themes, expand to paid/non-Steam providers, or claim
      unavailable metadata works. Report endpoint blockers promptly.

## Plan-07: Implement current-price cost-per-hour analysis

**Target:** November 20, 2026. **Dependencies:** Plan-05, Plan-06.

- [ ] In Python calculate hours = recorded_minutes / 60 and current-price
      cost/hour = current_price / hours for known positive hours and known price.
- [ ] Filter eligible rows with Polars and sort highest cost/hour first with
      deterministic ties; compare one currency/region/price basis at a time.
- [ ] Keep zero-hour games in a separate Unplayed group with no numeric cost/hour.
      Exclude missing-price or unknown-playtime rows with a visible explanation.
- [ ] Show the highest eligible result and ranked alternatives with price, hours,
      currency, timestamp and the current-price estimate explanation.
- [ ] Tests cover known arithmetic, subhour playtime, zero price/hours, nulls,
      malformed values, ties, no eligible games and currency mismatch.

## Plan-08: Aggregate playtime and preference evidence

**Target:** November 20, 2026. **Dependencies:** Plan-05, Plan-06.

- [ ] Use Polars to calculate total recorded hours, played/unplayed counts and
      grouped genre/theme playtime, with documented missing-value denominators.
- [ ] Keep account totals distinct from grouped totals: games can have multiple
      labels, so attribute weights explicitly rather than double-count silently.
- [ ] Use recorded lifetime playtime and, where supplied, recent playtime as
      evidence; do not claim session frequency or completed-game status.
- [ ] Test known totals, overlapping genres, unknown labels, empty datasets and
      zero playtime. Return computed results to the UI.

## Plan-09: Rank similar unplayed games

**Target:** November 21, 2026. **Dependencies:** Plan-08.

- [ ] Define and version an explainable Python scoring method using shared
      Steam genres/themes and playtime-weighted preference evidence. Use NumPy
      for vector/scoring calculations and document normalization and tie handling.
- [ ] Consider only owned games with known zero recorded minutes as unplayed.
      A missing playtime value never qualifies as zero.
- [ ] Give greater influence to stronger playtime evidence; document any use of
      lifetime/recent hours without equating hours with enjoyment or sessions.
- [ ] Return ranked candidates and reasons naming matching attributes and played
      examples; describe scores as similarity rather than calibrated probability.
- [ ] Handle no played games, no unplayed games, no usable metadata, zero-vector
      profiles and no positive matches without fabricated recommendations.
- [ ] Verify hand-checkable orderings, ties and determinism with Python tests.

## Plan-10: Generate analytical plots in Python

**Target:** November 21, 2026. **Dependencies:** Plan-07, Plan-08, Plan-09.

- [ ] Use Lets-Plot to generate a cost/hour ranking figure and genre/theme
      preference summary from the same Python results shown in the tables.
- [ ] Define a local plot delivery format and dependencies; any browser renderer
      only displays Python-generated plots and does not recalculate analysis.
- [ ] Include labels, units, currency, source/time and accessible text/table
      equivalents, with empty/single-result/long-name behavior.
- [ ] Verify chart values, renderability and agreement with fixture answers.

## Plan-11: Complete the library and statistics interface

**Target:** November 22, 2026. **Dependencies:** Plan-03 through Plan-08.

- [ ] Show imported public profile information, library rows and Python-computed
      counts/hours with coverage and last-updated information.
- [ ] Provide useful name, played/unplayed and genre filters and supported sort
      controls; send analysis/filter/sort work to Python.
- [ ] Show current price/currency, recorded hours and metadata availability without
      converting missing data to zero or a hidden library to an empty library.
- [ ] Verify keyboard interaction, loading/error/retry/empty states, responsive
      layout and profile changes in colocated component/integration tests.

## Plan-12: Complete the game-picking journey

**Target:** November 22, 2026. **Dependencies:** Plan-07, Plan-09, Plan-10, Plan-11.

- [ ] Users can switch between current-price value opportunities and similar
      unplayed games and inspect the reasons, figures and supporting tables.
- [ ] Recommend only games returned in that account's available owned library.
      Make unavailable data and limits visible without implying purchase history.
- [ ] Provide correct Steam game links and useful recovery for empty results;
      do not add purchases, installation or game-launch automation.
- [ ] Both recommendations remain consistent with active account/filters and
      backend results through navigation, refresh and failed requests.

## Plan-13: Integrate and freeze design/functionality

**Target:** November 23, 2026. **Dependencies:** Plan-01 through Plan-12.

- [ ] The full local journey works: profile input -> automatic Steam import ->
      normalized/enriched dataset -> library statistics -> both recommendations
      -> Lets-Plot figures and matching tables.
- [ ] All planned designs and functionality are implemented; no fake values,
      dead buttons, coming-soon pages or hidden demo fallback remain.
- [ ] Frontend lint/tests/build/format checks and Python lint/tests/format checks
      pass; actual commands/results and any unavailable checks are recorded.
- [ ] Validate one bounded live public-account journey when setup permits, with
      actual endpoint/coverage limitations recorded separately from mocked tests.
- [ ] Review the five top-level requirements with evidence. Escalate unresolved
      features before the November 24 deadline rather than silently dropping them.

## Plan-14: Final local testing and November 24 handoff

**Target:** November 24, 2026. **Dependencies:** Plan-13.

- [ ] The complete functional app is ready for local use and final testing.
- [ ] Human checks both recommendations, import, filters/sorts, source labels,
      errors, back/refresh, mobile/wide layout, keyboard and plot/table agreement.
- [ ] Fix regressions, repeat affected checks and record known issues honestly.
      Do not mark human/device or live API tests passed when not performed.
- [ ] Record dataset/schema, two question answers, filter/sort/aggregation
      locations, NumPy scoring, Lets-Plot outputs and test evidence.
- [ ] Verify protected files are unchanged and TIME_LOG.md reflects measured or
      labeled estimated Library Lots work without old-project totals.
- [ ] Hand off exact local setup/run instructions in allowed guidance. No
      deployment, database or deferred-document gate is required for this milestone.

## Plan-15: Deferred review after November 29

**First eligible date:** November 30. **Completion date:** to be agreed with the
human. **Dependencies:** Plan-14 and the date boundary.

- [ ] Only on or after November 30, read SECURE.md and LEGAL.md and determine their
      applicability to the implemented local app.
- [ ] Schedule their review and any resulting work with the human; do not claim
      this documentation reset completed either review.
- [ ] Keep hosting, public release, new services and spending outside the current
      scope unless the human explicitly requests them.

This deferred segment is separate from the November 24 design/functionality
deadline and does not extend it.
