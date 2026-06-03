# Codex Master Plan

## Goal

Build a full-stack healthcare LLM intelligence platform that runs locally and demonstrates eligibility verification, claim validation, RAG payer rule retrieval, ICD/CPT/HCPCS search, mock LLM claim explanation, and benchmark/scaling readiness.

## Phases

1. Repository foundation: monorepo structure, README, Docker Compose, docs, data, CI.
2. Database and seed data: PostgreSQL, pgvector extension, synthetic seed records.
3. FastAPI backend: health, analytics, eligibility, claims, RAG, codebook, and benchmark endpoints.
4. RAG and codebook intelligence: deterministic embeddings, vector-ready storage, payer rule retrieval, code compatibility.
5. Frontend: dashboard, eligibility, claim validation, rule explorer, codebooks, and scaling pages.
6. Tests and final polish: pytest, TypeScript build, Docker checks, synthetic-data safety.
