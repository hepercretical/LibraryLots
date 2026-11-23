# Local development

Plan-02 uses Node/npm, React 19.3.1 and Vite 8.3.8, plus Python 3.13
(verified with 3.13.15), FastAPI 0.115.6 and Uvicorn 0.34.0.
Frontend versions are pinned in package.json/package-lock.json. Python direct
dependencies are pinned in pyproject.toml and all resolved dependencies in
requirements.lock. This is a Windows/Python 3.13 lock. No Steam calls are made
by the health check or automated tests.

## Backend

Run from Backend/ using the available uv installer:

```powershell
uv venv .venv --python 3.13
uv pip sync --python .venv\Scripts\python.exe requirements.lock
uv pip install --python .venv\Scripts\python.exe --no-deps -e .
.venv\Scripts\python.exe -m uvicorn library_lots.api.app:app --host 127.0.0.1 --port 8000 --reload
```

Keep that terminal running. To check and format Python, from Backend/:

```powershell
.venv\Scripts\python.exe -m pytest
.venv\Scripts\python.exe -m ruff check src tests
.venv\Scripts\python.exe -m black --check src tests
.venv\Scripts\python.exe -m black src tests
```

Python has no compilation/build step for local use; editable installation is
the local package setup. FastAPI serves /api/health. No credentials are needed
for it. Backend/.env.example contains placeholders for later Steam integration;
Backend/.env is ignored and is never sent to the frontend. Health scaffolding
does not load or use Steam credentials.

## Frontend

In a second terminal, run from Frontend/:

```powershell
npm ci
npm run dev
```

Open http://127.0.0.1:5173 and use Load library. Vite binds to
loopback, requires port 5173, and forwards /api to http://127.0.0.1:8000.
Run the following checks from Frontend/:

```powershell
npm run lint
npm test
npm run build
npm run format
npx prettier --check .
```

The build outputs Frontend/dist. It is a build check, not a separately configured
production server. The development proxy requires the Python process. Stop both
development processes with Ctrl+C. Tests mock network responses and cover pending,
keyboard activation, success, HTTP/network errors, invalid responses and retry.

## Dependency maintenance

After approved Python dependency changes, regenerate the lock with
`uv pip compile pyproject.toml --extra dev -o requirements.lock`, then sync and
reinstall the local package using the commands above. Ruff is the Python linter;
Black is the formatter. Vitest/Testing Library test the React components;
ESLint checks JavaScript and Prettier formats frontend files only.

## Public library import and dataset

The Load library form sends an explicit request to the local Python service.
Configure `STEAM_WEB_API_KEY` in the ignored Backend/.env file as described in
Backend/.env.example. The backend makes HTTPS requests only to fixed Steam Web
API methods, with a ten-second timeout, no redirects or automatic retries, one
active import per process, and a 1,000-call per-process daily ceiling. A restart
resets that ceiling, so it is not a global limit across processes or machines;
the operator remains responsible for Steam's overall daily limit. Credentials
are not sent to the frontend or persisted in account snapshots. Cancellation
prevents a stale response from appearing, though a Steam request already in
flight may finish on the backend.

The Polars v1 dataset uses one row per valid AppID, with minutes and nullable
recent playtime, import source and time, and nullable fields for future price and
genre/theme enrichment. Duplicate AppIDs keep the first valid row; duplicates,
malformed rows, invalid identifiers and missing lifetime playtime mark the
import partial. Unknown minutes remain null. Store enrichment is not implemented
in Plan-05; all such fields are unavailable until Plan-06. The synthetic fixture
in Data/fixtures is separate from live imports and remains safe to track.

On November 18, 2026, the authorized public profile was checked with the
implemented importer. Steam's GetPlayerSummaries and GetOwnedGames endpoints
returned 131 owned-game rows, with matching reported count. This check did not
retrieve store prices, so region, currency and price coverage are not applicable;
it did not establish metadata enrichment. The sandboxed attempt could not reach
Steam; the approved unrestricted retry succeeded at 17:33:49 UTC. The live
Steam Web API Terms and method documentation were reviewed on November 18.

## Plan-02 verification, November 16, 2026

Verified the separate local Vite/Uvicorn processes with a real GET through
http://127.0.0.1:5173/api/health: status ok, service library-lots-backend.
Clean `npm ci`, Prettier check, frontend lint, production build and all six tests
in three files passed. npm reported zero vulnerabilities during the clean install.
Python pytest passed (one test), Ruff passed and Black check passed.
Polars, NumPy and Lets-Plot imports passed in the Python 3.13 environment.
The test run used `pytest -p no:cacheprovider` because sandbox permissions
prevented pytest cache creation. The remaining warning is an upstream
Starlette/AnyIO deprecated alias; it does not affect the health result.
Vitest required execution outside the sandbox because worker spawning was denied.
Git ignore checks confirmed exclusion of Backend/.env, .venv, node_modules and
dist. Protected tracked files have no differences from Git HEAD.
Plan-02 criteria are satisfied by this scaffold and verification. All six
acceptance checkboxes were marked complete with human authorization.
