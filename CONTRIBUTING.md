# Contributing

This is a portfolio MVP, but contributions should follow production-style discipline.

## Local Checks

```bash
cd backend
pytest
```

```bash
cd frontend
npm install
npm run build
```

## Data Safety

- Do not add real PHI.
- Do not add real payer contracts.
- Do not add real member IDs.
- Keep all patients, claims, payer rules, and codebooks synthetic.

## Pull Request Quality Bar

- Keep changes scoped.
- Add or update tests for backend logic changes.
- Update docs when public API behavior changes.
- Keep screenshots current when frontend views change.
