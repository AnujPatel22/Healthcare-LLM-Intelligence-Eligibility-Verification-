# Testing and QA

Backend tests cover:

- Active and inactive eligibility decisions.
- Prior authorization risk scoring.
- ICD/CPT compatibility matching.
- RAG filtering and retrieval.
- Benchmark target output.

Recommended checks:

```bash
docker compose config
cd backend && pytest
cd frontend && npm install && npm run build
```

Screenshot capture:

```bash
cd frontend
npm run screenshots
```

The screenshot command writes PNG files to `docs/screenshots/` and expects the frontend to be running.
