from datetime import date

from app.services.eligibility_engine import EligibilityEngine


RECORDS = [
    {
        "patient_ref": "SYN-PAT-1001",
        "payer": "Apex Health Plan",
        "member_ref": "SYN-MEM-9001",
        "plan_type": "Commercial PPO",
        "coverage_status": "active",
        "service_type": "MRI Imaging",
        "deductible_remaining": 450,
        "copay": 35,
        "prior_authorization_required": True,
        "effective_from": date(2026, 1, 1),
        "effective_to": date(2026, 12, 31),
    }
]


def test_active_eligibility_requires_authorization() -> None:
    result = EligibilityEngine().verify(RECORDS, "SYN-PAT-1001", "Apex Health Plan", "SYN-MEM-9001", "MRI Imaging", date(2026, 6, 1))
    assert result["coverage_status"] == "active"
    assert result["prior_authorization_required"] is True
    assert result["confidence"] == 0.94


def test_out_of_window_is_inactive() -> None:
    result = EligibilityEngine().verify(RECORDS, "SYN-PAT-1001", "Apex Health Plan", "SYN-MEM-9001", "MRI Imaging", date(2027, 1, 1))
    assert result["coverage_status"] == "inactive"
