"""
Consult Kenya Backend Application Entrypoint.
Phase 3 Concrete Executable Backend Implementation (PROG-01 through PROG-08).
"""

import time
import datetime
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.app.core.config import settings
from src.app.core.database import get_db, get_redis_client, init_db

# Import all 8 core backend modules
from src.app.modules.prog01_auth_verification import router as auth_router
from src.app.modules.prog02_studio_parser import router as studio_router
from src.app.modules.prog03_vector_engine import router as discovery_router
from src.app.modules.prog04_slot_lock_manager import router as calendar_router
from src.app.modules.prog05_mpesa_daraja import router as payments_router
from src.app.modules.prog06_escrow_state_machine import router as escrow_router
from src.app.modules.prog07_kra_etims_payout import router as settlement_router
from src.app.modules.prog08_dispute_adjudication import router as disputes_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "Production backend for Consult Kenya: Visual-First Professional Advisory & Authority Network. "
        "Implements Phase 3 Program Design specifications PROG-01 through PROG-08."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Enable CORS for frontend clients (Mobile Web, PWA, Desktop Chrome)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """Initializes persistent database tables on boot."""
    try:
        init_db()
    except Exception as e:
        print(f"[Startup Warning] Could not auto-create tables: {e}")


@app.get("/", tags=["System"])
def root():
    """Root entrypoint returning system metadata and available documentation."""
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "status": "OPERATIONAL",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "documentation": "/docs",
        "modules_implemented": [
            "PROG-01: Auth & Statutory Credentials Verification",
            "PROG-02: Advisory Video & Studio AST Diagram Parser",
            "PROG-03: Two-Pass Vector Recommendation & CAS Ranking Engine",
            "PROG-04: Distributed Calendar Slot Lock Manager",
            "PROG-05: Safaricom M-Pesa Daraja Payment & Callback Coordinator",
            "PROG-06: Statement of Work Escrow Lifecycle State Machine",
            "PROG-07: KRA eTIMS Invoicing & Ledger Settlement Engine",
            "PROG-08: Escrow Dispute Adjudication & Apportionment Engine"
        ]
    }


@app.get("/health", tags=["System"])
def healthcheck(db: Session = Depends(get_db)):
    """Healthcheck endpoint auditing PostgreSQL and Redis connectivity."""
    db_status = "HEALTHY"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"UNHEALTHY: {str(e)}"

    redis_status = "HEALTHY"
    try:
        r = get_redis_client()
        r.set("healthcheck:ping", "pong", ex=10)
        val = r.get("healthcheck:ping")
        if not val:
            redis_status = "DEGRADED"
    except Exception as e:
        redis_status = f"UNHEALTHY: {str(e)}"

    return {
        "status": "PASS" if db_status == "HEALTHY" and "HEALTHY" in redis_status else "WARN",
        "database": db_status,
        "redis_lock_cache": redis_status,
        "system_time": datetime.datetime.utcnow().isoformat(),
        "version": settings.VERSION
    }


# -----------------------------------------------------------------------------
# Module Router Mounting
# -----------------------------------------------------------------------------
api_prefix = settings.API_V1_PREFIX

app.include_router(auth_router, prefix=api_prefix)
app.include_router(studio_router, prefix=api_prefix)
app.include_router(discovery_router, prefix=api_prefix)
app.include_router(calendar_router, prefix=api_prefix)
app.include_router(payments_router, prefix=api_prefix)
app.include_router(escrow_router, prefix=api_prefix)
app.include_router(settlement_router, prefix=api_prefix)
app.include_router(disputes_router, prefix=api_prefix)
