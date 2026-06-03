from typing import Any

try:
    from langchain_core.documents import Document
except Exception:  # pragma: no cover - fallback only if langchain packaging changes
    Document = None  # type: ignore

from app.services.eligibility_engine import value
from app.services.embeddings import DeterministicEmbedding, cosine_similarity


class RagEngine:
    def __init__(self, embedder: DeterministicEmbedding | None = None) -> None:
        self.embedder = embedder or DeterministicEmbedding()

    def search(
        self,
        rules: list[Any],
        query: str,
        payer: str | None = None,
        code: str | None = None,
        service_type: str | None = None,
        top_k: int = 5,
    ) -> list[dict[str, Any]]:
        query_embedding = self.embedder.embed(query)
        scored: list[tuple[float, Any]] = []
        query_lower = query.lower()
        for rule in rules:
            if payer and value(rule, "payer") != payer:
                continue
            if service_type and value(rule, "service_type") != service_type:
                continue
            code_refs = value(rule, "code_refs", []) or []
            if code and code not in code_refs:
                continue
            content = f"{value(rule, 'title')} {value(rule, 'content')} {' '.join(code_refs)}"
            embedding = value(rule, "embedding", None)
            rule_embedding = list(embedding) if embedding is not None else self.embedder.embed(content)
            score = cosine_similarity(query_embedding, rule_embedding)
            if any(token.lower() in content.lower() for token in query.split()):
                score += 0.2
            if value(rule, "payer", "").lower() in query_lower:
                score += 0.2
            if code and code in code_refs:
                score += 0.4
            scored.append((score, rule))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [self._to_match(rule, score) for score, rule in scored[:top_k]]

    def as_documents(self, matches: list[dict[str, Any]]) -> list[Any]:
        if Document is None:
            return matches
        return [
            Document(
                page_content=match["snippet"],
                metadata={"rule_id": match["rule_id"], "payer": match["payer"], "score": match["score"]},
            )
            for match in matches
        ]

    def _to_match(self, rule: Any, score: float) -> dict[str, Any]:
        content = value(rule, "content")
        return {
            "rule_id": value(rule, "rule_id"),
            "payer": value(rule, "payer"),
            "title": value(rule, "title"),
            "snippet": content[:240],
            "score": round(float(score), 3),
            "requires_authorization": bool(value(rule, "requires_authorization")),
        }
