from datetime import date, datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import Boolean, Date, DateTime, Float, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_ref: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(120))
    age_band: Mapped[str] = mapped_column(String(32))
    region: Mapped[str] = mapped_column(String(80))
    synthetic_note: Mapped[str] = mapped_column(Text)


class EligibilityRecord(Base):
    __tablename__ = "eligibility_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_ref: Mapped[str] = mapped_column(String(64), index=True)
    payer: Mapped[str] = mapped_column(String(120), index=True)
    member_ref: Mapped[str] = mapped_column(String(64), index=True)
    plan_type: Mapped[str] = mapped_column(String(80))
    coverage_status: Mapped[str] = mapped_column(String(32), index=True)
    service_type: Mapped[str] = mapped_column(String(80), index=True)
    deductible_remaining: Mapped[float] = mapped_column(Numeric(10, 2))
    copay: Mapped[float] = mapped_column(Numeric(10, 2))
    prior_authorization_required: Mapped[bool] = mapped_column(Boolean)
    effective_from: Mapped[date] = mapped_column(Date)
    effective_to: Mapped[date] = mapped_column(Date)


class Claim(Base):
    __tablename__ = "claims"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    claim_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    patient_ref: Mapped[str] = mapped_column(String(64), index=True)
    payer: Mapped[str] = mapped_column(String(120), index=True)
    member_ref: Mapped[str] = mapped_column(String(64), index=True)
    service_type: Mapped[str] = mapped_column(String(80), index=True)
    icd_codes: Mapped[list[str]] = mapped_column(JSONB)
    cpt_codes: Mapped[list[str]] = mapped_column(JSONB)
    hcpcs_codes: Mapped[list[str]] = mapped_column(JSONB)
    diagnosis: Mapped[str] = mapped_column(Text)
    procedure: Mapped[str] = mapped_column(Text)
    place_of_service: Mapped[str] = mapped_column(String(80))
    provider_type: Mapped[str] = mapped_column(String(80))
    authorization_ref: Mapped[str | None] = mapped_column(String(80), nullable=True)


class PayerRule(Base):
    __tablename__ = "payer_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rule_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    payer: Mapped[str] = mapped_column(String(120), index=True)
    service_type: Mapped[str] = mapped_column(String(80), index=True)
    rule_type: Mapped[str] = mapped_column(String(80))
    code_refs: Mapped[list[str]] = mapped_column(JSONB)
    title: Mapped[str] = mapped_column(String(180))
    content: Mapped[str] = mapped_column(Text)
    denial_reason: Mapped[str] = mapped_column(String(180))
    requires_authorization: Mapped[bool] = mapped_column(Boolean)
    embedding: Mapped[list[float]] = mapped_column(Vector(16))


class CodebookEntry(Base):
    __tablename__ = "codebook_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    code_type: Mapped[str] = mapped_column(String(16), index=True)
    description: Mapped[str] = mapped_column(Text)
    service_type: Mapped[str] = mapped_column(String(80), index=True)
    compatible_codes: Mapped[list[str]] = mapped_column(JSONB)
    incompatible_codes: Mapped[list[str]] = mapped_column(JSONB)
    risk_weight: Mapped[int] = mapped_column(Integer)
    embedding: Mapped[list[float]] = mapped_column(Vector(16))


class ValidationResult(Base):
    __tablename__ = "validation_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    claim_id: Mapped[str] = mapped_column(String(64), index=True)
    status: Mapped[str] = mapped_column(String(32))
    risk_score: Mapped[int] = mapped_column(Integer)
    risk_level: Mapped[str] = mapped_column(String(32))
    latency_ms: Mapped[float] = mapped_column(Float)
    result_payload: Mapped[dict] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class BenchmarkResult(Base):
    __tablename__ = "benchmark_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    queries_per_day_target: Mapped[int] = mapped_column(Integer)
    p50_latency_ms: Mapped[float] = mapped_column(Float)
    p95_latency_ms: Mapped[float] = mapped_column(Float)
    cache_hit_rate: Mapped[float] = mapped_column(Float)
    rule_match_accuracy: Mapped[float] = mapped_column(Float)
    horizontal_replicas: Mapped[int] = mapped_column(Integer)
    cpu_profile: Mapped[str] = mapped_column(String(120))
    memory_profile: Mapped[str] = mapped_column(String(120))
    is_synthetic: Mapped[bool] = mapped_column(Boolean, default=True)
    notes: Mapped[str] = mapped_column(Text)
