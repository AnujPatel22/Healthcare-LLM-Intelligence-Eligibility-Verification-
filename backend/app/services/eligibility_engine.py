from datetime import date
from decimal import Decimal
from typing import Any


def value(obj: Any, key: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


class EligibilityEngine:
    def verify(
        self,
        records: list[Any],
        patient_ref: str,
        payer: str,
        member_ref: str,
        service_type: str,
        date_of_service: date,
    ) -> dict[str, Any]:
        exact = [
            record
            for record in records
            if value(record, "patient_ref") == patient_ref
            and value(record, "payer") == payer
            and value(record, "member_ref") == member_ref
            and value(record, "service_type") == service_type
        ]
        fallback = [
            record
            for record in records
            if value(record, "patient_ref") == patient_ref
            and value(record, "payer") == payer
            and value(record, "member_ref") == member_ref
        ]
        record = exact[0] if exact else (fallback[0] if fallback else None)

        if not record:
            return {
                "patient_ref": patient_ref,
                "payer": payer,
                "coverage_status": "not_found",
                "plan_type": "Unknown",
                "deductible_remaining": 0.0,
                "copay": 0.0,
                "prior_authorization_required": False,
                "confidence": 0.52,
                "recommended_next_step": "Confirm member reference and payer before claim submission.",
            }

        in_window = value(record, "effective_from") <= date_of_service <= value(record, "effective_to")
        status = value(record, "coverage_status") if in_window else "inactive"
        requires_auth = bool(value(record, "prior_authorization_required"))

        if status == "active" and requires_auth:
            next_step = "Confirm prior authorization before claim submission."
        elif status == "active":
            next_step = "Coverage is active for the requested service; proceed with claim readiness checks."
        else:
            next_step = "Coverage is inactive for the date of service; verify payer eligibility response."

        confidence = 0.94 if exact and in_window else 0.78 if fallback else 0.52
        return {
            "patient_ref": patient_ref,
            "payer": payer,
            "coverage_status": status,
            "plan_type": value(record, "plan_type"),
            "deductible_remaining": float(value(record, "deductible_remaining") or Decimal("0")),
            "copay": float(value(record, "copay") or Decimal("0")),
            "prior_authorization_required": requires_auth,
            "confidence": confidence,
            "recommended_next_step": next_step,
        }
