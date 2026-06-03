from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import BenchmarkResult
from app.schemas import BenchmarkSummary
from app.services.benchmark_engine import BenchmarkEngine

router = APIRouter(prefix="/benchmarks", tags=["benchmarks"])


@router.get("/summary", response_model=BenchmarkSummary)
def summary(db: Session = Depends(get_db)) -> dict:
    row = db.query(BenchmarkResult).order_by(BenchmarkResult.id).first()
    return BenchmarkEngine().baseline(row)


@router.post("/run-simulation", response_model=BenchmarkSummary)
def run_simulation() -> dict:
    return BenchmarkEngine().run_simulation(20000)
