# Library Lots human-quality guidance

## Purpose

Keep the application useful, deliberate and understandable to the human using it.
This replaces inherited product-specific reviews and completion claims.
Read [DESIGN.md](DESIGN.md), [STYLE_GUIDE.md](STYLE_GUIDE.md), [PLAN.md](PLAN.md)
and [../AGENTS.md](../AGENTS.md), plus the human-maintained EXPECTATIONS.md.
Do not change EXPECTATIONS.md.

Do not read or use SECURE.md or LEGAL.md in agent work through November 29, 2026
inclusive. First eligible use is November 30. The current requested rewrite
does not constitute review or implementation of their future requirements.

## Product clarity

- Make the next action obvious: load a public library, inspect it, or pick a game.
- Explain the public game-detail requirement without telling people their account
  must be empty when information is hidden.
- Use current Steam price as a visible estimate basis, not claimed purchase cost.
  Do not describe playtime as proof of enjoyment or unplayed games as wasted money.
- Explain recommendations through matching genres/themes and actual playtime
  evidence. Do not invent reviews, ratings, testimonials or account activity.
- Say when metadata, prices or playtime are missing. A no-result explanation is
  better than a fabricated answer.
- State that local live imports require internet and backend configuration.
  Do not imply the Steam API eliminates the Python server.
- No decorative compliance banners, fake contacts, marketing analytics, cookie
  widgets, social features or extra settings are required for this local tool.

## Interaction quality

- Prevent duplicate loads and confusing repeated clicks. Make pending status clear
  and handle old responses when switching accounts.
- Preserve useful inputs and filters during recoverable errors and navigation.
- Provide persistent field errors and page-load recovery; avoid raw tracebacks
  and disappearing-only error toasts.
- Every visible control must work. Do not leave placeholder routes or disabled
  examples in the finished journey.
- Keep keyboard focus visible, controls labeled, touch targets usable and figures
  understandable without relying on color.
- Check long game names, large libraries, zero hours, fractional hours, zero
  price, unavailable price, missing genres and regional/currency differences.
- Use meaningful page titles, a language attribute, accessible headings and a
  Library Lots identity instead of Vite/React defaults. Public SEO infrastructure,
  social previews, sitemap/structured data and tracking are not required for local
  testing. Do not invent a canonical hosted domain.

## Human review by November 24

Ask the human to try the local app on narrow and wide viewports. Record actual
browser/device, tasks, observations and follow-up issues. Review:

1. SteamID and both profile URL forms, invalid values and unresolved vanity names.
2. Import/enrichment progress, refresh, profile switching and back navigation.
3. A confirmed empty library versus hidden/unavailable game details.
4. Library filters and sorts and agreement with Python-computed statistics.
5. Current-price value recommendations, price context and separate unplayed group.
6. Similar unplayed recommendations and understandable matching reasons.
7. Lets-Plot figures and matching tables, keyboard navigation and zoom.
8. Request failure, retry, missing metadata, no eligible rows and no matches.

A generated screenshot, mock test or written plan does not establish human review.
Do not claim a live Steam import passed unless the live journey was performed.
The completed local milestone is due November 24; no public release is requested.
