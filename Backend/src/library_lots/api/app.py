"""FastAPI application for local frontend development."""

import threading

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from library_lots.analysis.dataset import normalize
from library_lots.steam.importer import ImportErrorState, import_library

app = FastAPI(title="Library Lots API", version="0.1.0")
import_lock = threading.Lock()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, str]:
    """Return a non-sensitive service readiness response."""

    return {"status": "ok", "service": "library-lots-backend"}


class ImportRequest(BaseModel):
    profile: str = Field(max_length=256)


@app.post("/api/library/import")
def load_library(body: ImportRequest) -> dict:
    if not import_lock.acquire(blocking=False):
        raise HTTPException(status_code=429, detail="rate_limited")
    try:
        result = import_library(body.profile)
        dataset, partial = normalize(result["games"], result["imported_at"], result["partial"])
        result["games"] = dataset.to_dicts()
        result["partial"] = partial
        return result
    except ImportErrorState as exc:
        statuses = {
            "invalid_input": 400,
            "not_found": 404,
            "hidden": 403,
            "rate_limited": 429,
            "configuration": 503,
            "unavailable": 502,
        }
        raise HTTPException(status_code=statuses[exc.code], detail=exc.code) from None
    finally:
        import_lock.release()
