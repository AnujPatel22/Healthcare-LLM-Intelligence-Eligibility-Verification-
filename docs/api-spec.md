# API Spec

Base URL: `http://localhost:8000`

- `GET /health`: service status.
- `GET /analytics/summary`: counts, validation mix, benchmark baseline.
- `GET /eligibility/records`: seeded eligibility options.
- `POST /eligibility/verify`: verifies synthetic coverage for a requested service/date.
- `GET /claims`: lists synthetic claims.
- `GET /claims/{claim_id}`: returns one claim.
- `POST /claims/{claim_id}/validate`: validates eligibility, payer rules, code compatibility, and explanation.
- `POST /rag/search`: retrieves synthetic payer rules.
- `POST /codebooks/search`: searches synthetic ICD/CPT/HCPCS entries.
- `GET /benchmarks/summary`: returns synthetic baseline metrics.
- `POST /benchmarks/run-simulation`: returns a synthetic benchmark simulation.
