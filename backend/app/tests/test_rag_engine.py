from app.services.rag_engine import RagEngine


RULES = [
    {
        "rule_id": "RULE-APEX-IMG-001",
        "payer": "Apex Health Plan",
        "service_type": "MRI Imaging",
        "title": "MRI prior authorization",
        "content": "MRI imaging requires prior authorization and documentation of medical necessity.",
        "code_refs": ["70553"],
        "requires_authorization": True,
    },
    {
        "rule_id": "RULE-NOVA-PT-001",
        "payer": "NovaCare Advantage",
        "service_type": "Physical Therapy",
        "title": "Therapy visit limit",
        "content": "Physical therapy requires progress notes after 12 visits.",
        "code_refs": ["97110"],
        "requires_authorization": False,
    },
]


def test_rag_search_filters_by_payer_and_code() -> None:
    matches = RagEngine().search(RULES, "MRI authorization 70553", payer="Apex Health Plan", code="70553")
    assert matches[0]["rule_id"] == "RULE-APEX-IMG-001"
    assert matches[0]["requires_authorization"] is True
