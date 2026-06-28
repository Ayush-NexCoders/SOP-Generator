"""
FastAPI Main Application
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from database.db import init_db
from models import SOPCreate, SOPUpdate, GenerateRequest
from modules.sop_service import (
    get_all_sops,
    get_sop_by_name,
    create_sop,
    update_sop,
    delete_sop,
)
from modules.prompt_builder import build_analysis_prompt, build_sop_prompt
from modules.ai_generator import generate_context, generate_sop
from modules.parser import parse_sop, parse_context

app = FastAPI(title="AI SOP Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/", include_in_schema=False)
def serve_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/library", include_in_schema=False)
def serve_library():
    return FileResponse(os.path.join(FRONTEND_DIR, "library.html"))

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/sops")
def list_sops():
    sops = get_all_sops()
    return {"sops": sops, "count": len(sops)}

@app.get("/sops/{process_name}")
def get_sop(process_name: str):
    sop = get_sop_by_name(process_name)
    if not sop:
        raise HTTPException(status_code=404, detail=f"SOP not found.")
    return sop

@app.post("/sops", status_code=201)
def create_new_sop(payload: SOPCreate):
    try:
        return create_sop(payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@app.put("/sops/{process_name}")
def update_existing_sop(process_name: str, payload: SOPUpdate):
    updated = update_sop(process_name, payload.model_dump(exclude_none=True))
    if updated is None:
        raise HTTPException(status_code=404, detail="SOP not found.")
    return updated

@app.delete("/sops/{process_name}")
def delete_existing_sop(process_name: str):
    deleted = delete_sop(process_name)
    if not deleted:
        raise HTTPException(status_code=404, detail="SOP not found.")
    return {"message": "Deleted"}

@app.post("/generate")
def generate_sop_endpoint(payload: GenerateRequest):
    process_name = payload.process_name.strip()
    if not process_name:
        raise HTTPException(status_code=400, detail="process_name cannot be empty.")

    existing = get_sop_by_name(process_name)
    if existing:
        return {"status": "exact_match", "sop": existing}

    try:
        analysis_prompt = build_analysis_prompt(process_name)
        raw_context = generate_context(analysis_prompt)
        context_data = parse_context(raw_context)

        sop_prompt = build_sop_prompt(process_name, context_data["full_context"])
        raw_sop = generate_sop(sop_prompt)

        parsed = parse_sop(raw_sop)
        parsed["process_name"] = process_name
        parsed["department"] = context_data.get("department", "General")

        return {"status": "generated", "sop": parsed}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
