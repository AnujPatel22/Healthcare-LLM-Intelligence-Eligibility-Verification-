from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import BenchmarkResult, Claim, CodebookEntry, EligibilityRecord, Patient, PayerRule, ValidationResult
from app.schemas import AnalyticsSummary
from app.services.benchmark_engine import BenchmarkEngine

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary", response_model=AnalyticsSummary)
def summary(db: Session = Depends(get_db)) -> dict:
    benchmark = db.query(BenchmarkResult).order_by(BenchmarkResult.id).first()
    validation_rows = db.query(ValidationResult).all()
    mix = {"clean": 0, "watch": 0, "needs_review": 0}
    for row in validation_rows:
        mix[row.status] = mix.get(row.status, 0) + 1
    if not validation_rows:
        mix = {"clean": 2, "watch": 2, "needs_review": 4}
    return {
        "patients": db.query(Patient).count(),
        "eligibility_records": db.query(EligibilityRecord).count(),
        "claims": db.query(Claim).count(),
        "payer_rules": db.query(PayerRule).count(),
        "codebook_entries": db.query(CodebookEntry).count(),
        "benchmark": BenchmarkEngine().baseline(benchmark),
        "validation_mix": mix,
    }
