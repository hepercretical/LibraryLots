# Library Lots legal review — dormant until November 30, 2026

## Date restriction

The human requested this rewrite now. After the rewrite, **do not read, consult,
apply, implement, or verify against this document in agent work through November
29, 2026 inclusive**. First eligible use: **November 30, 2026**, America/Denver.
It is not an acceptance gate for the November 24 local functional milestone.
Do not copy its checklist into active requirements to bypass the restriction.

This is a future review inventory, not legal advice or a compliance determination.
The scheduling decision does not change external obligations. Verify current
primary sources and actual applicability when this document becomes active.

## Product and data scope

Library Lots runs locally with React/Vite and a Python backend. It imports public
Steam account/library information and free public Steam game metadata to produce
statistics, current-price cost/hour and similar-unplayed-game recommendations.
No hosting, payments, app accounts, advertisements or tracking provider is selected.

The later review must reflect actual data flows rather than an inherited policy
for a different product. Do not add services, age gates, contracts or public-facing
pages solely because a previous project had them.

## Steam source terms and permitted use

- Review current Steam Web API terms and documentation for keys, permitted access,
  request limits, caching, derived results, display, redistribution and retention.
- Identify every supplemental Steam Store endpoint used. Distinguish documented
  Web API contracts from public Steam-operated endpoints whose supported contract
  has not been verified. Availability alone is not proof of permitted reuse.
- Review attribution, Valve/Steam branding, links, names, artwork and other metadata
  rights. Avoid implying sponsorship, endorsement or affiliation.
- Do not bypass visibility controls, authentication or access restrictions.
- Record sources, versions/dates and outstanding questions. Ask the human to
  resolve material uncertainty rather than claiming terms permit unverified use.

## Price and recommendation claims

- Explain current store price, region/currency, discounts and retrieval date.
  Do not call it the user's purchase cost, spending, savings or resale value.
- Explain that hours reflect Steam's available record and may omit activity or
  reflect idle time; cost/hour does not measure enjoyment.
- Label recommendations as an explainable similarity estimate using available
  genres/themes and playtime. Do not promise preference accuracy or enjoyment.
- Keep zero-hour and missing-price cases clear and avoid unsupported conclusions
  about a person's finances, habits or identity.
- Describe known metadata gaps, regional prices, unavailable/delisted games and
  the effect of changing prices on rankings.

## Privacy and distribution assessment

- Inventory SteamIDs, profile names/URLs, avatars, owned games, playtime, derived
  preferences, local caches, logs and exported plots. Public visibility does not
  automatically resolve every use, retention or redistribution question.
- Describe which processing is local, what requests go to Steam, and any external
  resources used by plots/images. Review retention and clearing behavior.
- Determine applicable privacy/data-protection obligations for the actual operator,
  intended audience, jurisdiction and distribution. Do not invent a U.S.-only
  audience or assume every statute applies.
- If public distribution is later proposed, assess accurate notices, operator
  contacts, user requests, accessibility, any youth-related applicability and
  third-party processing with appropriate qualified review.
- Cookies, analytics, marketing, payments, community submissions and app-account
  terms are conditional on later approved scope; they are not required additions
  to the local milestone.

## Code, dataset and asset licensing

- Inventory licenses for Python/JavaScript packages, fonts, icons, images and
  datasets. Keep notices required by actual licenses.
- Keep synthetic test data clearly separate from real account data. Review rights
  before redistributing an account snapshot or Steam metadata dataset.
- Do not invent an existing project license or change licensing without the
  human's explicit instruction.
- Never publish fabricated contact details or copied policies describing
  unimplemented systems.

## Later review evidence and references

Record actual applicability, source/date, operator decisions, unresolved items and
review evidence. Any public deployment remains separately requested and approved;
this document does not select hosting or authorize spending.

Starting points to verify when active:

- [Steam Web API terms](https://steamcommunity.com/dev/apiterms)
- [Steam Web API overview](https://partner.steamgames.com/doc/webapi_overview)
- [Steamworks branding guidelines](https://partner.steamgames.com/doc/marketing/branding)
- [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/)
