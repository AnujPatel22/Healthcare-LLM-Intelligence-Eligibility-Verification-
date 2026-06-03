from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import SessionLocal, init_database
from app.routers import analytics, benchmarks, claims, codebooks, eligibility, health, rag
from app.seed import seed_database

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Synthetic healthcare eligibility, claim validation, and RAG rule retrieval service.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(analytics.router)
app.include_router(eligibility.router)
app.include_router(claims.router)
app.include_router(rag.router)
app.include_router(codebooks.router)
app.include_router(benchmarks.router)


@app.on_event("startup")
def startup() -> None:
    init_database()
    if settings.seed_on_startup:
        db = SessionLocal()
        try:
            seed_database(db)
        finally:
            db.close()
