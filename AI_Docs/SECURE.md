# Library Lots security review — dormant until November 30, 2026

## Date restriction

The human requested this rewrite now. After the rewrite, **do not read, consult,
apply, implement, or verify against this document in agent work through November
29, 2026 inclusive**. First eligible use: **November 30, 2026**, America/Denver.
It is not an acceptance gate for the November 24 local functional milestone.
Do not copy this checklist into active guidance to bypass the restriction.
Independent AGENTS.md instructions remain in force.

## Scope for the later review

Review the implemented local React/Vite frontend, Python HTTP backend, Steam API
adapter, datasets/caches and Polars/NumPy/Lets-Plot outputs. No database, hosted
service, app-account system or public deployment is currently selected. Do not
provision such systems to satisfy this checklist. Reassess only if scope changes.

This is a future engineering checklist, not certification or a completed audit.
Verify current primary guidance and applicability when the review begins.

## Secrets and repository review

- Trace Steam key handling from local configuration to outbound requests.
  Verify keys never enter browser bundles, VITE_ values, returned errors, request
  logs, screenshots, fixtures or Git.
- Review safe environment examples, ignore coverage and tracked/staged content.
  Cover .venv, Python caches, dependencies, build output, real account snapshots,
  caches, plots with account details, logs and private exports.
- Keep synthetic fixtures, source and dependency locks versioned. Do not hide
  required source with broad data-file exclusions.
- Define exposure handling: stop disclosure, arrange human-led key revocation/
  rotation and review history changes before making destructive modifications.

## Local server and outbound request review

- Verify loopback binding, allowed frontend origins and development-server
  exposure. Do not assume local servers cannot receive hostile browser requests.
- Validate SteamID/profile inputs, fixed outbound Steam hosts, redirects, schemes
  and request construction. Test that arbitrary URLs cannot turn the adapter into
  a proxy or reach private/local network destinations.
- Verify network timeouts, maximum response size, bounded concurrency, retries,
  backoff, cache expiry and rate-limit behavior.
- Treat Steam metadata as untrusted text. Check React escaping, external links
  and image URLs; do not render remote descriptions as raw HTML.
- Review Lets-Plot delivery: generated HTML/JavaScript origins, dependency loading,
  file access and whether plot responses can expose keys or unrelated local files.
- Verify that user input cannot select arbitrary filesystem paths or execute shell,
  Python or template code. Bound analytical input sizes and resource consumption.
- Review error responses and diagnostics without collecting unneeded account data.

## Data handling and analytical integrity

- Inventory temporary datasets and caches, who can access them, retention,
  clearing behavior and account-switch separation.
- Verify missing/hidden data cannot become fabricated zero values or leak prior
  account results through cached responses.
- Check malformed numbers, zero denominators, NaN/infinity, type overflow,
  duplicate AppIDs and currency mixing.
- Keep deterministic automated tests offline with synthetic data; separate actual
  public-account checks from fixtures and private exports.

## Dependencies and later release considerations

- Review supported Python/Node versions, pinned dependencies, vulnerabilities,
  build output and optional external renderer resources. Record findings without
  automatically forcing dependency downgrades or broad upgrades.
- Threat-model the actual app and record applicable controls, test evidence,
  findings, owners and residual risks.
- If hosting is later requested, obtain separate approval and assess identity,
  authorization, transport, headers, rate controls, deployment secrets, monitoring,
  retention, incidents and recovery for that actual design.
- Do not inherit database, administrator, authentication or upload requirements
  for features the app does not have.

## Later review evidence and references

Record review date, application revision, data flows, tested attacks, findings,
fixes and remaining limitations. Do not claim public-release readiness from a
local functional pass.

Recheck primary sources when active:

- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP SSRF prevention guidance](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)
- [Vite environment variables](https://vite.dev/guide/env-and-mode)
- [Steam Web API overview](https://partner.steamgames.com/doc/webapi_overview)
