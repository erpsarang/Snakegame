"""Run the Dire Straits identity sentence generation service."""

from __future__ import annotations

from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.lyrics_service.service import DireStraitsIdentityService

app = FastAPI(title="Dire Straits Identity Forge")
service = DireStraitsIdentityService()


class IngestRequest(BaseModel):
    directory: str


class GenerateRequest(BaseModel):
    count: int = 1
    seed: int | None = None


class GenerateResponse(BaseModel):
    sentences: List[str]
    songs: List[str]


@app.post("/ingest")
def ingest(request: IngestRequest) -> dict[str, str]:
    try:
        service.ingest(Path(request.directory))
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=f"Directory not found: {exc}")
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=400, detail=str(exc))
    return {"status": "ok"}


@app.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest) -> GenerateResponse:
    if not service.ready():
        raise HTTPException(status_code=409, detail="Service not ready. Call /ingest first.")

    try:
        sentences = service.generate(count=request.count, seed=request.seed)
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=400, detail=str(exc))

    songs = service.corpus.songs if service.corpus else []
    return GenerateResponse(sentences=sentences, songs=songs)


__all__ = ["app", "service"]
