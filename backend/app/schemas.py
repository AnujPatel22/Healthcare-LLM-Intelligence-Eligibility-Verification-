from datetime import date
from typing import Any

from pydantic import BaseModel, Field


class EligibilityRequest(BaseModel):
    patient_ref: str
    payer: str
    member_ref: str
    service_type: str
    date_of_service: date


class EligibilityResponse(BaseModel):
    patient_ref: str
    payer: str
    coverage_status: str
    plan_type: str
    deductible_remaining: float
    copay: float
    prior_authorization_required: bool
    confidence: float
    recommended_next_step: str


class ClaimSummary(BaseModel):
    claim_id: str
    patient_ref: str
    payer: str
    service_type: str
    icd_codes: list[str]
    cpt_codes: list[str]
    hcpcs_codes: list[str]
    diagnosis: str
    procedure: str
    place_of_service: str
    provider_type: str
    authorization_ref: str | None


class RuleMatch(BaseModel):
    rule_id: str
    payer: str
    title: str
    snippet: str
    score: float
    requires_authorization: bool


class CodebookMatch(BaseModel):
    code: str
    code_type: str
    description: str
    service_type: str
    compatibility: str
    risk_weight: int


class ClaimValidationResponse(BaseModel):
    claim_id: str
    status: str
    risk_score: int
    risk_level: str
    rule_match_accuracy: float
    latency_ms: float
    missing_requirements: list[str]
    matched_rules: list[RuleMatch]
    codebook_matches: list[CodebookMatch]
    recommended_fixes: list[str]
    explanation: str


class RagSearchRequest(BaseModel):
    query: str = Field(min_length=1)
    payer: str | None = None
    code: str | None = None
    service_type: str | None = None
    top_k: int = Field(default=5, ge=1, le=10)


class RagSearchResponse(BaseModel):
    query: str
    matches: list[RuleMatch]
    synthetic_disclaimer: str


class CodebookSearchRequest(BaseModel):
    query: str = Field(min_length=1)
    code_type: str | None = None
    related_code: str | None = None
    top_k: int = Field(default=8, ge=1, le=20)


class CodebookSearchResponse(BaseModel):
    query: str
    matches: list[CodebookMatch]


class BenchmarkSummary(BaseModel):
    queries_per_day_target: int
    p50_latency_ms: float
    p95_latency_ms: float
    cache_hit_rate: float
    rule_match_accuracy: float
    horizontal_replicas: int
    cpu_profile: str
    memory_profile: str
    is_synthetic: bool
    notes: str


class AnalyticsSummary(BaseModel):
    patients: int
    eligibility_records: int
    claims: int
    payer_rules: int
    codebook_entries: int
    benchmark: BenchmarkSummary
    validation_mix: dict[str, Any]
