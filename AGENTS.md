# AGENTS.md

## Project Identity

This repository is a Healthcare LLM Intelligence & Eligibility Verification Service. It simulates a healthcare AI platform that verifies patient eligibility, validates claim readiness, retrieves payer-specific billing rules, searches synthetic ICD/CPT/HCPCS codebooks, and generates LLM-assisted validation explanations.

The system must remain GitHub-ready, recruiter-friendly, demo-ready, and technically credible.

## Core Stack

- Backend: Python, FastAPI
- RAG: LangChain-compatible orchestration with deterministic fallback embeddings
- Vector database: PostgreSQL with pgvector
- Frontend: React, TypeScript, Vite
- Local runtime: Docker Compose
- LLM integration: mock fallback by default
- Testing: pytest for backend, TypeScript build for frontend

## Non-Negotiable Rules

1. Never use real PHI.
2. Never use real patient records.
3. Never use real insurance member data.
4. Never include real payer contracts.
5. All data must be synthetic.
6. The app must run locally with Docker Compose.
7. The app must work without a real LLM API key.
8. Use deterministic mock LLM output when no API key exists.
9. Use PostgreSQL with pgvector.
10. Include practical tests.
11. Include benchmark simulation.
12. Keep benchmark claims honest and clearly synthetic unless real load tests are run.

## Demo Flow

1. Open dashboard.
2. Review eligibility, claim, rule, codebook, and benchmark metrics.
3. Verify a synthetic patient eligibility record.
4. Validate a synthetic claim.
5. Review payer rule matches and codebook compatibility.
6. Read the grounded mock LLM explanation.
7. Search payer rules through RAG.
8. Search synthetic ICD/CPT/HCPCS codebooks.
9. Review scaling benchmark readiness.
