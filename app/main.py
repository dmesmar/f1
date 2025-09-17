from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://dariomesasmarti.com",
        "https://www.dariomesasmarti.com",
        "http://localhost:4200",
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-API-Key"],
    allow_credentials=True,
)

api = APIRouter(prefix="/api")

# 1) Ping /api/ping 
@api.get("/ping", tags=["util"])
async def ping():
    return {"status": "ok"}

app.include_router(api)
