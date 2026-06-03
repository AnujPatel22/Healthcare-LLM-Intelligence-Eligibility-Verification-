from typing import Any

from app.services.eligibility_engine import value
from app.services.embeddings import DeterministicEmbedding, cosine_similarity


class CodebookMatcher:
    def __init__(self, embedder: DeterministicEmbedding | None = None) -> None:
        self.embedder = embedder or DeterministicEmbedding()

    def search(
        self,
        entries: list[Any],
        query: str,
        code_type: str | None = None,
        related_code: str | None = None,
        top_k: int = 8,
    ) -> list[dict[str, Any]]:
        query_embedding = self.embedder.embed(query)
        scored: list[tuple[float, Any]] = []
        query_lower = query.lower()
        for entry in entries:
            if code_type and value(entry, "code_type") != code_type:
                continue
            text = f"{value(entry, 'code')} {value(entry, 'description')} {value(entry, 'service_type')}"
            embedding = value(entry, "embedding", None)
            entry_embedding = list(embedding) if embedding is not None else self.embedder.embed(text)
            score = cosine_similarity(query_embedding, entry_embedding)
            if value(entry, "code").lower() in query_lower:
                score += 0.7
            if any(part.lower() in text.lower() for part in query.split()):
                score += 0.15
            compatibility = "neutral"
            compatible = value(entry, "compatible_codes", []) or []
            incompatible = value(entry, "incompatible_codes", []) or []
            if related_code:
                if related_code in compatible:
                    compatibility = "compatible"
                    score += 0.5
                elif related_code in incompatible:
                    compatibility = "incompatible"
                    score += 0.5
            scored.append((score, entry))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [self._to_match(entry, related_code) for _, entry in scored[:top_k]]

    def validate_compatibility(self, entries: list[Any], claim: Any) -> list[dict[str, Any]]:
        codes = (value(claim, "icd_codes", []) or []) + (value(claim, "cpt_codes", []) or []) + (value(claim, "hcpcs_codes", []) or [])
        lookup = {value(entry, "code"): entry for entry in entries}
        matches: list[dict[str, Any]] = []
        for code in codes:
            entry = lookup.get(code)
            if not entry:
                continue
            compatibility = "compatible"
            incompatible = set(value(entry, "incompatible_codes", []) or [])
            compatible = set(value(entry, "compatible_codes", []) or [])
            if any(other in incompatible for other in codes):
                compatibility = "incompatible"
            elif compatible and not any(other in compatible for other in codes if other != code):
                compatibility = "needs_support"
            matches.append(self._to_match(entry, None, compatibility))
        return matches

    def _to_match(self, entry: Any, related_code: str | None, compatibility_override: str | None = None) -> dict[str, Any]:
        compatibility = compatibility_override or "neutral"
        if related_code:
            if related_code in (value(entry, "compatible_codes", []) or []):
                compatibility = "compatible"
            elif related_code in (value(entry, "incompatible_codes", []) or []):
                compatibility = "incompatible"
        return {
            "code": value(entry, "code"),
            "code_type": value(entry, "code_type"),
            "description": value(entry, "description"),
            "service_type": value(entry, "service_type"),
            "compatibility": compatibility,
            "risk_weight": int(value(entry, "risk_weight", 0)),
        }
