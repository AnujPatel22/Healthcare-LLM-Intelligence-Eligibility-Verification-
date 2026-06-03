import time
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.models import Claim, CodebookEntry, EligibilityRecord, PayerRule, ValidationResult
from app.schemas import ClaimSummary, ClaimValidationResponse
from app.services.claim_validator import ClaimValidator
from app.services.codebook_matcher import CodebookMatcher
from app.services.eligibility_engine import EligibilityEngine
from app.services.llm_client import get_llm_client
from app.services.rag_engine import RagEngine

router = APIRouter(prefix="/claims", tags=["claims"])


def _summary(row: Claim) -> dict:
    return {
        "claim_id": row.claim_id,
        "patient_ref": row.patient_ref,
        "payer": row.payer,
        "member_ref": row.member_ref,
        "service_type": row.service_type,
        "icd_codes": row.icd_codes,
        "cpt_codes": row.cpt_codes,
        "hcpcs_codes": row.hcpcs_codes,
        "diagnosis": row.diagnosis,
        "procedure": row.procedure,
        "place_of_service": row.place_of_service,
        "provider_type": row.provider_type,
        "authorization_ref": row.authorization_ref,
    }


@router.get("", response_model=list[ClaimSummary])
def list_claims(db: Session = Depends(get_db)) -> list[dict]:
    return [_summary(row) for row in db.query(Claim).order_by(Claim.claim_id).all()]


@router.get("/{claim_id}", response_model=ClaimSummary)
def get_claim(claim_id: str, db: Session = Depends(get_db)) -> dict:
    row = db.query(Claim).filter(Claim.claim_id == claim_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Claim not found")
    return _summary(row)


@router.post("/{claim_id}/validate", response_model=ClaimValidationResponse)
def validate_claim(claim_id: str, db: Session = Depends(get_db)) -> dict:
    started_at = time.perf_counter()
    claim = db.query(Claim).filter(Claim.claim_id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    eligibility_records = db.query(EligibilityRecord).all()
    eligibility = EligibilityEngine().verify(
        eligibility_records,
        claim.patient_ref,
        claim.payer,
        claim.member_ref,
        claim.service_type,
        date_of_service=date(2026, 6, 1),
    )
    query = f"{claim.payer} {claim.service_type} {' '.join(claim.icd_codes + claim.cpt_codes + claim.hcpcs_codes)} {claim.diagnosis} {claim.procedure}"
    rules = db.query(PayerRule).all()
    matched_rules = RagEngine().search(rules, query, payer=claim.payer, service_type=claim.service_type, top_k=4)
    codebook_entries = db.query(CodebookEntry).all()
    codebook_matches = CodebookMatcher().validate_compatibility(codebook_entries, claim)
    preliminary = ClaimValidator().validate(claim, eligibility, matched_rules, codebook_matches, "", started_at)
    settings = get_settings()
    explanation = get_llm_client(settings.llm_provider, settings.llm_api_key).explain_claim(
        claim,
        preliminary["status"],
        preliminary["missing_requirements"],
        matched_rules,
        codebook_matches,
    )
    result = ClaimValidator().validate(claim, eligibility, matched_rules, codebook_matches, explanation, started_at)
    db.add(
        ValidationResult(
            claim_id=claim.claim_id,
            status=result["status"],
            risk_score=result["risk_score"],
            risk_level=result["risk_level"],
            latency_ms=result["latency_ms"],
            result_payload=result,
        )
    )
    db.commit()
    return result
