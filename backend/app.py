"""TrustScope backend: serves precomputed results and the frontend.

Run from the backend folder:
    uvicorn app:app --reload
Then open http://127.0.0.1:8000
"""
import csv
import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FRONTEND = ROOT / "frontend"

app = FastAPI(title="TrustScope")


@app.get("/api/results")
def results():
    """AUROC per signal: pooled (all pairs), within (same question), between (different questions)."""
    rows = []
    with open(DATA / "results_auroc.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append({
                "signal": r["signal"],
                "pooled": float(r["pooled"]),
                "within": float(r["within"]),
                "between": float(r["between"]),
            })
    return {"results": rows}


@app.get("/api/examples")
def examples():
    """Confidently wrong answers (model agrees with itself but is wrong). Empty until the file is added."""
    path = DATA / "confidently_wrong.json"
    if not path.exists():
        return {"examples": []}
    return {"examples": json.loads(path.read_text(encoding="utf-8"))}


@app.get("/")
def index():
    return FileResponse(FRONTEND / "index.html")


app.mount("/", StaticFiles(directory=FRONTEND), name="frontend")
