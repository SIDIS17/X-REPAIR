from __future__ import annotations
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional

from backend.modules import vibe, acoustic, thermal, power, circuit, core

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT/"frontend"

app = FastAPI(
    title="X-Repair 17A API",
    version="1.0.0",
    description="API multimodale: Vibe, Circuit, Acoustic, Thermal, Power et Core."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

class SignalRequest(BaseModel):
    samples: list[float]
    fs: float = Field(gt=0)
    rpm: float = Field(default=1500, gt=0)

class AcousticRequest(BaseModel):
    samples: list[float]
    fs: float = Field(gt=0)

class ThermalRequest(BaseModel):
    temperatures_c: list[float]
    ambient_c: float = 25.0
    limit_c: float = 80.0

class PowerRequest(BaseModel):
    voltage: list[float]
    current: list[float]
    nominal_voltage: Optional[float] = None

class CircuitRequest(BaseModel):
    netlist: str
    run_spice: bool = False

class FusionRequest(BaseModel):
    results: dict[str, dict]

@app.get("/api/health")
def health():
    return {
        "service":"X-Repair 17A",
        "status":"ok",
        "modules":["vibe","circuit","acoustic","thermal","power","core"]
    }

@app.post("/api/vibe/analyze")
def vibe_analyze(req: SignalRequest):
    try:
        return vibe.analyze(req.samples, req.fs, req.rpm)
    except Exception as e:
        raise HTTPException(400, str(e))

@app.post("/api/acoustic/analyze")
def acoustic_analyze(req: AcousticRequest):
    try:
        return acoustic.analyze(req.samples, req.fs)
    except Exception as e:
        raise HTTPException(400, str(e))

@app.post("/api/thermal/analyze")
def thermal_analyze(req: ThermalRequest):
    try:
        return thermal.analyze(req.temperatures_c, req.ambient_c, req.limit_c)
    except Exception as e:
        raise HTTPException(400, str(e))

@app.post("/api/power/analyze")
def power_analyze(req: PowerRequest):
    try:
        return power.analyze(req.voltage, req.current, req.nominal_voltage)
    except Exception as e:
        raise HTTPException(400, str(e))

@app.post("/api/circuit/analyze")
def circuit_analyze(req: CircuitRequest):
    try:
        return circuit.analyze(req.netlist, req.run_spice)
    except Exception as e:
        raise HTTPException(400, str(e))

@app.post("/api/core/fuse")
def core_fuse(req: FusionRequest):
    return core.fuse(req.results)

@app.get("/")
def index():
    return FileResponse(FRONTEND/"index.html")

@app.get("/assets/{path:path}")
def assets(path: str):
    target = ROOT/"assets"/path
    if not target.exists():
        raise HTTPException(404, "Asset introuvable")
    return FileResponse(target)
