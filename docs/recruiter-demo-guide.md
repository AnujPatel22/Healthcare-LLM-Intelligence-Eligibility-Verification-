# Recruiter Demo Guide

This guide gives a fast, concrete review path for the Healthcare LLM Intelligence & Eligibility Verification Service.

## What This Proves

- Full-stack delivery: React, TypeScript, FastAPI, PostgreSQL, Docker.
- Healthcare workflow understanding: eligibility, claim readiness, prior auth, code compatibility.
- AI/RAG architecture: payer rules and codebooks retrieved with cited matches.
- Production thinking: tests, CI, seed data, scaling docs, security/compliance notes.

## Run Locally

```bash
cp .env.example .env
docker compose up --build
```

Open:

- App: `http://localhost:5173`
- API docs: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`

If local ports are busy:

```bash
POSTGRES_PORT=55432 BACKEND_PORT=8001 FRONTEND_PORT=5174 BACKEND_PUBLIC_URL=http://localhost:8001 docker compose up --build
```

## API Proof

Health:

```bash
curl http://localhost:8000/health
```

Eligibility:

```bash
curl -X POST http://localhost:8000/eligibility/verify \
  -H "Content-Type: application/json" \
  -d '{"patient_ref":"SYN-PAT-1001","payer":"Apex Health Plan","member_ref":"SYN-MEM-9001","service_type":"MRI Imaging","date_of_service":"2026-06-01"}'
```

Claim validation:

```bash
curl -X POST http://localhost:8000/claims/CLM-7001/validate
```

RAG rule search:

```bash
curl -X POST http://localhost:8000/rag/search \
  -H "Content-Type: application/json" \
  -d '{"query":"MRI prior authorization 70553","payer":"Apex Health Plan","top_k":5}'
```

## Expected Highlights

- `coverage_status`: `active`
- `prior_authorization_required`: `true`
- `risk_score`: around `45`
- `matched_rules`: includes `RULE-APEX-IMG-001`
- `rule_match_accuracy`: `0.94`
- `queries_per_day_target`: `20000`

All data is synthetic and safe for public GitHub review.
