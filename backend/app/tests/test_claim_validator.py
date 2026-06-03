from app.services.claim_validator import ClaimValidator


def test_claim_validator_scores_prior_auth_risk() -> None:
    claim = {
        "claim_id": "CLM-7001",
        "patient_ref": "SYN-PAT-1001",
        "payer": "Apex Health Plan",
        "member_ref": "SYN-MEM-9001",
        "service_type": "MRI Imaging",
        "diagnosis": "Headache",
        "procedure": "MRI brain",
        "place_of_service": "Outpatient hospital",
        "provider_type": "Radiology group",
        "authorization_ref": None,
    }
    eligibility = {"coverage_status": "active", "prior_authorization_required": True}
    rules = [{"rule_id": "RULE-APEX-IMG-001", "requires_authorization": True}]
    codes = [{"code": "70553", "compatibility": "needs_support", "risk_weight": 18}]
    result = ClaimValidator().validate(claim, eligibility, rules, codes, "explanation")
    assert result["status"] in {"watch", "needs_review"}
    assert "Prior authorization confirmation" in result["missing_requirements"]
