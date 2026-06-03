# Backend Spec

The backend exposes FastAPI endpoints grouped by health, analytics, eligibility, claims, RAG, codebooks, and benchmarks.

Service modules own business behavior:

- `EligibilityEngine`: coverage and authorization decisions.
- `ClaimValidator`: missing requirements, risk score, and fixes.
- `RagEngine`: synthetic payer rule retrieval.
- `CodebookMatcher`: code search and compatibility.
- `MockLLMClient`: deterministic grounded explanation.
- `BenchmarkEngine`: synthetic scaling metrics.
