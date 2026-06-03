# Security Policy

## Synthetic Data Only

This repository is designed for public portfolio review and must contain only synthetic data.

Never commit:

- Real PHI.
- Real patient records.
- Real insurance member data.
- Real payer contracts.
- Real API keys or secrets.

## Secrets

Use `.env` for local secrets. `.env` is ignored by git.

Use `.env.example` only for safe placeholder values.

## Production Gap

This project is not production-ready for healthcare use. A real deployment would require HIPAA review, authentication, authorization, audit logging, encryption, BAAs, key management, and compliance approval.
