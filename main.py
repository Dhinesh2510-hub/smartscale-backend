
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from time import time

app = FastAPI(title="Retail AI SmartScale API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://retail-ai-smartscale.vercel.app",
        "https://retail-ai-smartscale-3o5j1c8q0-sddhinesh977-4144s-projects.vercel.app",
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

class WeightReading(BaseModel):
    weight_g: float = Field(ge=0, le=100000)
    raw_adc: int
    hx711_ready: bool
    calibrated: bool

latest = {
    "weight_g": 0.0,
    "raw_adc": 0,
    "hx711_ready": False,
    "calibrated": False,
    "updated_at": None,
}

@app.get("/")
def health():
    return {"status": "online", "service": "SmartScale API"}

@app.post("/api/hardware/weight")
def receive_weight(data: WeightReading):
    latest.update(data.model_dump())
    latest["updated_at"] = time()
    return {"ok": True, "reading": latest}

@app.get("/api/hardware/weight")
def get_weight():
    return latest
