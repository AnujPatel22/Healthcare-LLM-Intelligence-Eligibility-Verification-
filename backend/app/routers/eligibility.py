from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import EligibilityRecord
from app.schemas import EligibilityRequest, EligibilityResponse
from app.services.eligibility_engine import EligibilityEngine

router = APIRouter(prefix="/eligibility", tags=["eligibility"])


@router.get("/records")
def records(db: Session = Depends(get_db)) -> list[dict]:
    return [
        {
            "patient_ref": row.patient_ref,
            "payer": row.payer,
            "member_ref": row.member_ref,
            "service_type": row.service_type,
            "coverage_status": row.coverage_status,
        }
        for row in db.query(EligibilityRecord).order_by(EligibilityRecord.patient_ref).all()
    ]


@router.post("/verify", response_model=EligibilityResponse)
def verify(payload: EligibilityRequest, db: Session = Depends(get_db)) -> dict:
    rows = db.query(EligibilityRecord).all()
    return EligibilityEngine().verify(rows, **payload.model_dump())
