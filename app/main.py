import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router as api_router

app = FastAPI(title="BeeBot AI Context Service - Async")

# CORS Configuration
# NOTE: allow_origins=["*"] + allow_credentials=True is ILLEGAL per the CORS spec.
# Browsers (and FastAPI itself) reject this combination.
# This AI service is called server-to-server by the Node.js backend, so we
# lock it down to the backend's origin only for security.
_raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5000,http://127.0.0.1:5000")
ALLOWED_ORIGINS = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
def health_check():
    return {"status": "ok", "service": "BeeBot AI context processing - Celery Engine"}
