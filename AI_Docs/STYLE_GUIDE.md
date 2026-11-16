# Library Lots style guide

## Purpose and boundaries

Make a game library easy to inspect and a recommendation easy to understand.
Use with [DESIGN.md](DESIGN.md), [HUMAN.md](HUMAN.md), [PLAN.md](PLAN.md) and
[../AGENTS.md](../AGENTS.md). Read the human's EXPECTATIONS.md without editing it.
No previous-project screenshots, palette approvals or themes carry over.

SECURE.md and LEGAL.md must not be read or used in agent work through November 29,
2026 inclusive. First eligible use is November 30. This guide does not activate
their deferred requirements.

## Visual direction

Use clear typography, restrained surfaces, compact readable game rows and one
obvious primary action per context. Let Steam game names/artwork provide character.
Avoid generic decorative dashboards, excessive pills, unrelated gradients,
oversized empty cards and charts that do not answer a question.

Build a single consistent theme first. Dark/light switching, custom accents,
animation systems and new icon packages are not required for this sprint.
Review the initial palette and layout with the human in Plan-03.

## Design tokens and CSS

Define semantic tokens in Frontend/src/styles/ for background, surface, text,
muted text, border, primary action, focus, error and chart colors. Include spacing,
type sizes/line heights, radii, shadows, content widths and control heights.
Select concrete values during design; no inherited palette is preapproved.

Use tokens throughout component styles. Add named values for new visual roles
rather than scattered literals. Keep tokens/reset/global typography separate from
page layout and colocated component CSS. Prefer simple classes, Grid and Flexbox;
avoid deeply nested selectors, unexplained magic numbers and routine !important.

## Layout and accessibility

- Start with a narrow single column; expand only when content has room. Use
  content-driven breakpoints and a maximum content width.
- Use semantic header/nav/main landmarks, one main page heading and logical
  heading order. Buttons perform actions; links navigate.
- Give fields visible labels, instructions and associated persistent errors.
  Placeholders do not replace labels.
- Keep visible keyboard focus, sensible focus order and dialogs with focus
  management. Announce loading/results/errors without excessive interruptions.
- Use at least 44px touch targets as a project convention. Check keyboard,
  200% zoom, reduced motion and reflow on narrow screens.
- Target WCAG 2.2 AA contrast and interaction quality as an engineering standard;
  do not claim compliance solely from automated tests.
- Do not hide the main result, source basis, units or error recovery on mobile.
  Long names wrap. Tables may have an intentionally labeled scroll region if
  needed, with the primary recommendation readable outside the wide table.
- Avoid sticky elements that obscure fields, mobile keyboards, focus or notices.

## Data presentation

- Show hours with units; preserve backend precision and round consistently only
  for display. Show currency codes when a symbol could be ambiguous.
- Label prices **Current Steam price** and cost/hour **Current-price cost/hour**.
  Include region/currency and retrieval time. Keep estimate wording beside results.
- Use **Unplayed** only for known zero recorded hours. Use **Unavailable** for
  missing values. Unknown price is not free and missing playtime is not zero.
- Align numerical columns; explain sort direction and selected filters.
- Provide clear match reasons. Use neutral labels rather than shaming a person
  for their library or claiming a score proves enjoyment.
- Display all analytical charts from Python/Lets-Plot results. Include titles,
  axis units, readable labels and equivalent tables/text. Color never carries
  the only meaning; chart values must agree with tabular results.

## States and copy

Use consistent names: Load library, Library, Statistics and Pick a game.
Choose specific actions such as Load library, Refresh, Reset filters and Try again.
Do not ship framework titles, lorem ipsum, fake activity, dead links or
Coming Soon destinations.

Show loading, partial enrichment, validation, empty library, no matching games,
hidden/unavailable details, request failure and success as appropriate.
Explain what happened and the next useful action. Keep important errors visible;
a toast can supplement a field or retry region, never replace it.
Preserve valid input and view state during recoverable errors.

## Verification

Test each custom component using accessible roles/labels and userEvent. Check
important output, controls, pending/disabled behavior and relevant data states.
Review narrow/wide layouts, long game names, large values, focus, zoom and figure
legibility. Run frontend format/lint/tests/build after implementation changes.
Record human review separately from automated checks. This documentation update
is not a palette, layout or application test pass.
