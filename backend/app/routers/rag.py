from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import PayerRule
from app.schemas import RagSearchRequest, RagSearchResponse
from app.services.rag_engine import RagEngine

router = APIRouter(prefix="/rag", tags=["rag"])


@router.post("/search", response_model=RagSearchResponse)
def search(payload: RagSearchRequest, db: Session = Depends(get_db)) -> dict:
    rules = db.query(PayerRule).all()
    matches = RagEngine().search(rules, payload.query, payload.payer, payload.code, payload.service_type, payload.top_k)
    return {
        "query": payload.query,
        "matches": matches,
        "synthetic_disclaimer": "Matches are retrieved from synthetic payer policy data for demo use only.",
    }
