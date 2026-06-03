# Database Schema

Tables:

- `patients`: synthetic patient references and non-PHI profile labels.
- `eligibility_records`: payer/member/service/date coverage state.
- `claims`: synthetic claim facts, code lists, service type, and authorization reference.
- `payer_rules`: synthetic payer policies with pgvector embeddings.
- `codebook_entries`: synthetic ICD/CPT/HCPCS entries with pgvector embeddings.
- `validation_results`: saved validation payloads.
- `benchmark_results`: synthetic performance baseline.

No table should store real PHI or real insurance data.
