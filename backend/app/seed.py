import json
from pathlib import Path
from typing import Any
from datetime import date

from sqlalchemy.orm import Session

from app.models import BenchmarkResult, Claim, CodebookEntry, EligibilityRecord, Patient, PayerRule
from app.services.embeddings import DeterministicEmbedding

def _data_dir() -> Path:
    here = Path(__file__).resolve()
    candidates = [
        here.parents[2] / "data" / "synthetic",
        here.parents[1] / "data" / "synthetic",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


DATA_DIR = _data_dir()


def _load(name: str) -> list[dict[str, Any]]:
    with (DATA_DIR / name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def seed_database(db: Session) -> None:
    embedder = DeterministicEmbedding()
    if db.query(Patient).count() == 0:
        db.add_all(Patient(**row) for row in _load("patients.json"))
    if db.query(EligibilityRecord).count() == 0:
        rows = []
        for row in _load("eligibility_records.json"):
            row["effective_from"] = date.fromisoformat(row["effective_from"])
            row["effective_to"] = date.fromisoformat(row["effective_to"])
            rows.append(EligibilityRecord(**row))
        db.add_all(rows)
    if db.query(Claim).count() == 0:
        db.add_all(Claim(**row) for row in _load("claims.json"))
    if db.query(PayerRule).count() == 0:
        rules = []
        for row in _load("payer_rules.json"):
            row["embedding"] = embedder.embed(f"{row['title']} {row['content']} {' '.join(row['code_refs'])}")
            rules.append(PayerRule(**row))
        db.add_all(rules)
    if db.query(CodebookEntry).count() == 0:
        entries = []
        for row in _load("codebooks.json"):
            row["embedding"] = embedder.embed(f"{row['code']} {row['description']} {row['service_type']}")
            entries.append(CodebookEntry(**row))
        db.add_all(entries)
    if db.query(BenchmarkResult).count() == 0:
        db.add_all(BenchmarkResult(**row) for row in _load("benchmark_results.json"))
    db.commit()
