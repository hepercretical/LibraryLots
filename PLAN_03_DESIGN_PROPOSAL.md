# Plan-03 design proposal for human review

This proposal describes the intended local application; it is not an implemented
screen or evidence of human review. Steam imports require internet and a
backend-configured Web API key. The application does not ask for a password.

## Journey and navigation

The header shows **Library Lots**, navigation to **Load library**, **Library**,
**Statistics**, and **Pick a game**, and the selected profile and import time
when available. Before an import, the other views explain that a public library
must be loaded and link back to the form. Browser back returns to the previous
view; useful search and filter selections survive navigation and recoverable
errors. No routing dependency is needed.

Load library has a visible SteamID64 or profile URL label, short examples, a
visibility explanation, and a **Load library** button. During a request, an
announced progress message and **Cancel** appear, and duplicate submissions
are disabled. Validation errors stay next to the field. Unresolved identity,
hidden game details, unavailable responses, rate limits and network errors have
distinct explanations and a useful retry action. A confirmed visible empty
library is explicitly identified. Refresh retains the current identity and
shows progress; switching profiles immediately removes old results from the
new profile's view. Cancellation and request identity checks prevent late
responses from replacing newer results. Metadata enrichment is shown separately
from import and can be partial.

Library presents a search field, played/unplayed and genre filters, sort control,
and **Reset filters**, followed by compact rows with name, recorded hours,
current Steam price and available genres. Missing values say **Unavailable**;
known zero playtime says **Unplayed**. Empty library, no matches, loading,
partial metadata and failure each have distinct messages. Filters and sorting
are performed by Python.

Statistics shows available game count, played/unplayed counts, recorded hours,
and genre/theme playtime with a Python-generated figure and equivalent table.
Coverage and multi-label allocation are explained. Empty, unavailable and partial
data do not imply zero; source and import time remain visible.

Pick a game offers two clearly labeled sections. Current-price cost/hour shows
the leading played game and alternatives with recorded hours, current price,
currency, region and retrieval time. It explains that the figure is based on
the retrieved store price, not the amount paid. Unplayed games are separate;
missing price or hours and no eligible result are explained. Similar unplayed
games show a leading suggestion, alternatives, shared attributes and played-game
examples. Missing metadata, no played games, no unplayed games and no positive
matches each receive an explanation without a fabricated result. Figures have
matching tables; scores do not claim enjoyment.

## Layout and visual direction

Use the existing scaffold's restrained light palette as a proposal: background
`#f5f7f8`, surface `#ffffff`, text `#1f2933`, muted text `#52616b`, border
`#d5dde3`, primary action `#176b87`, and focus `#d45b2a`. System sans
serif typography, 1.5 body line height, a 72rem maximum content width, 44px
minimum controls, modest 0.45rem control radius and an 8px spacing scale keep
the interface compact. Primary actions are visually prominent; secondary
actions use a bordered surface. All controls have visible focus and labels.

On narrow screens the header, form, filters and results stack in one column;
game names wrap. On wider screens filters can sit beside or above results and
explanations can share a row with the main result. Tables have a labeled
horizontal scroll region when necessary, while the main recommendation and
its context remain readable outside it. Charts include titles, units, source,
time and a text/table equivalent. Layout must reflow at 200% zoom, respect
reduced motion and retain keyboard access.

## View states and recovery

These are design specifications for later implementation. Each result view
shows the active profile and import time, and never presents an earlier profile's
results as the newly selected one. Loading and result changes use a polite
status announcement; field errors remain associated with the field. Retain
valid inputs and filters on recoverable failures.

| View | Loading or validation | Empty or unavailable | Error and recovery | Partial | Success |
| --- | --- | --- | --- | --- | --- |
| Load library | Disable duplicate loads; announce profile and library progress; offer Cancel. Reject invalid input beside the field. | Distinguish an explicitly confirmed empty library from hidden game details and an unresolved profile. | Explain connection, configuration and rate-limit failures; preserve the input and offer Try again. | Show returned games with a partial-import notice and missing-data explanation. | Show the selected profile, import time and a route to Library; Refresh starts a new import. |
| Library | Announce loading and retain valid filter selections. Give malformed filter input a persistent field message. | Explain a confirmed empty library separately from no filter matches; offer Reset filters for the latter. If game details are hidden, direct the user to visibility guidance. | Keep filters and offer Try again; explain when the library cannot be retrieved. | Show available rows, missing fields as Unavailable and coverage; offer metadata retry when available. | Show compact rows, Python-applied filters and sort direction, source and import time. |
| Statistics | Announce calculation progress; prevent duplicate requests. If an input filter is invalid, identify it and retain its value. | Explain when there are no games or insufficient known playtime or metadata; do not show unknown totals as zero. | Preserve filters and offer Try again when statistics cannot be loaded. | Show available totals and grouped results with denominators and missing-data coverage. | Show Python totals and genre/theme figure with an equivalent table and allocation explanation. |
| Current-price value | Announce ranking progress; identify invalid comparison or filter selections. | Explain no eligible priced, played games; list unplayed separately without cost/hour. | Preserve the comparison and offer Try again if ranking or price retrieval fails. | Rank eligible rows only; show excluded counts, missing prices and region/currency/time context. | Show the leading game and ranked alternatives with price, hours, cost/hour, source and estimate wording. |
| Similar unplayed games | Announce ranking progress; identify invalid filters without discarding them. | Explain no played games, no known unplayed games, missing metadata or no positive matches. | Preserve filters and offer Try again when recommendations cannot be calculated. | Show available matches with metadata coverage and limitations; never invent reasons. | Show the leading suggestion and alternatives with shared attributes, played examples and relative-score explanation. |

## Semantic design tokens and shared controls

The proposed palette retains the human-approved direction. Use the following
tokens consistently; verify actual rendered contrast during implementation,
including focus indicators and chart marks. These values are a design decision,
not evidence of a browser or accessibility test.

| Role | Value |
| --- | --- |
| Background / surface | `#f5f7f8` / `#ffffff` |
| Text / muted text / border | `#1f2933` / `#52616b` / `#d5dde3` |
| Primary background / primary text | `#176b87` / `#ffffff` |
| Focus outline | `#d45b2a`, 3px with 3px offset |
| Error text / error surface / error border | `#9b1c1c` / `#fff1f0` / `#b42318` |
| Chart primary / secondary / grid | `#176b87` / `#70421b` / `#d5dde3` |
| Spacing | 4px, 8px, 16px, 24px, 32px, 48px |
| Body / small / heading type | 16px/1.5, 14px/1.4, 24px/1.2; page heading 32px/1.15 |
| Control height / content width | at least 44px / at most 72rem |
| Control radius / surface radius / shadow | 0.45rem / 0.75rem / `0 2px 8px rgba(31, 41, 51, 0.08)` |

Labels sit above inputs; buttons use consistent primary and bordered secondary
styles. Status and error regions use text and icons or labels in addition to
color. Filters use labeled native controls and a Reset filters button. On
narrow screens, result rows stack the game name above labeled values; on wider
screens tables align numeric columns and allow long names to wrap. If a table
still exceeds the viewport, place it in a keyboard-accessible, labeled scroll
region. Both Lets-Plot figures have an adjacent table from the same backend
results, with matching values, units, source, timestamps and readable labels.
No chart or table alone carries the primary recommendation.

## Review requested

Please review the journey, profile-switching behavior, palette and responsive
layout. Record actual feedback and any changes before Plan-04 begins. Automated
tests, screenshots and this proposal do not constitute human review.
