"""
OptInPG Analyst Service — FastAPI + LangGraph skeleton
Reads collected data and triggers Wave 2 evaluation agents.
"""
import os
import json
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="OptInPG Analyst",
    description="Analysis service for Octant public goods evaluation",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGINS", "*")],
    allow_methods=["*"],
    allow_headers=["*"],
)

COUNCIL_OUT = Path(os.getenv("COUNCIL_OUT_DIR", "council-out"))


class AnalyseRequest(BaseModel):
    slug: str


class AnalyseResponse(BaseModel):
    slug: str
    status: str
    eval_files: list[str]
    analysed_at: str


@app.get("/health")
def health():
    return {"status": "ok", "service": "analyst", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.post("/analyse", response_model=AnalyseResponse)
def analyse(req: AnalyseRequest):
    eval_dir = COUNCIL_OUT / req.slug / "eval"

    if not eval_dir.exists():
        raise HTTPException(
            status_code=404,
            detail=f"No evaluation data for slug '{req.slug}'. Run Wave 2 first.",
        )

    eval_files = []
    for f in sorted(eval_dir.iterdir()):
        if f.suffix in (".json", ".md"):
            eval_files.append(f.name)

    return AnalyseResponse(
        slug=req.slug,
        status="analysed",
        eval_files=eval_files,
        analysed_at=datetime.now(timezone.utc).isoformat(),
    )


@app.get("/analyse/{slug}")
def get_analysis(slug: str):
    eval_dir = COUNCIL_OUT / slug / "eval"
    if not eval_dir.exists():
        raise HTTPException(status_code=404, detail=f"No evaluation for slug '{slug}'")

    result = {}
    for f in sorted(eval_dir.iterdir()):
        if f.suffix == ".json":
            try:
                result[f.stem] = json.loads(f.read_text())
            except json.JSONDecodeError:
                result[f.stem] = {"_error": f"Failed to parse {f.name}"}
        elif f.suffix == ".md":
            result[f.stem] = f.read_text()

    return {"slug": slug, "evaluations": result}


@app.get("/analyse/{slug}/ostrom")
def get_ostrom_scores(slug: str):
    ostrom_path = COUNCIL_OUT / slug / "eval" / "ostrom-scores.json"
    if not ostrom_path.exists():
        raise HTTPException(status_code=404, detail=f"No Ostrom scores for slug '{slug}'")

    try:
        return json.loads(ostrom_path.read_text())
    except json.JSONDecodeError:
        raise HTTPException(status_code=422, detail=f"Malformed Ostrom scores JSON for slug '{slug}'")
