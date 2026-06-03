from app.services.codebook_matcher import CodebookMatcher


ENTRIES = [
    {
        "code": "M54.50",
        "code_type": "ICD",
        "description": "Low back pain",
        "service_type": "Physical Therapy",
        "compatible_codes": ["97110"],
        "incompatible_codes": ["70553"],
        "risk_weight": 8,
    },
    {
        "code": "70553",
        "code_type": "CPT",
        "description": "MRI brain with contrast",
        "service_type": "MRI Imaging",
        "compatible_codes": ["G44.1"],
        "incompatible_codes": ["M54.50"],
        "risk_weight": 18,
    },
]


def test_search_finds_related_code() -> None:
    matches = CodebookMatcher().search(ENTRIES, "MRI brain", code_type="CPT", top_k=1)
    assert matches[0]["code"] == "70553"


def test_validate_flags_incompatible_pair() -> None:
    claim = {"icd_codes": ["M54.50"], "cpt_codes": ["70553"], "hcpcs_codes": []}
    matches = CodebookMatcher().validate_compatibility(ENTRIES, claim)
    assert any(match["compatibility"] == "incompatible" for match in matches)
