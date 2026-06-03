from typing import Any


class LLMClient:
    def explain_claim(
        self,
        claim: Any,
        status: str,
        missing_requirements: list[str],
        matched_rules: list[dict[str, Any]],
        codebook_matches: list[dict[str, Any]],
    ) -> str:
        raise NotImplementedError


class MockLLMClient(LLMClient):
    def explain_claim(
        self,
        claim: Any,
        status: str,
        missing_requirements: list[str],
        matched_rules: list[dict[str, Any]],
        codebook_matches: list[dict[str, Any]],
    ) -> str:
        rule_ids = ", ".join(rule["rule_id"] for rule in matched_rules[:3]) or "no payer rules"
        risky_codes = [match["code"] for match in codebook_matches if match["compatibility"] in {"incompatible", "needs_support"}]
        blockers = "; ".join(missing_requirements) if missing_requirements else "no blocking requirements"
        code_note = ", ".join(risky_codes) if risky_codes else "all matched synthetic codes are compatible or neutral"
        return (
            f"Mock grounded explanation: claim {getattr(claim, 'claim_id', None) or claim.get('claim_id')} is {status}. "
            f"The decision is grounded in synthetic payer rule matches {rule_ids}. "
            f"Current blockers: {blockers}. Codebook review: {code_note}. "
            "This explanation is generated from synthetic data and is not medical, billing, or legal advice."
        )


def get_llm_client(provider: str = "mock", api_key: str | None = None) -> LLMClient:
    return MockLLMClient()
