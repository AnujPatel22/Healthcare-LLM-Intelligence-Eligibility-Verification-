from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import CodebookEntry
from app.schemas import CodebookSearchRequest, CodebookSearchResponse
from app.services.codebook_matcher import CodebookMatcher

router = APIRouter(prefix="/codebooks", tags=["codebooks"])


@router.post("/search", response_model=CodebookSearchResponse)
def search(payload: CodebookSearchRequest, db: Session = Depends(get_db)) -> dict:
    entries = db.query(CodebookEntry).all()
    matches = CodebookMatcher().search(entries, payload.query, payload.code_type, payload.related_code, payload.top_k)
    return {"query": payload.query, "matches": matches}
