# Scaling Strategy

## Horizontal Scaling

- Run multiple stateless FastAPI containers.
- Place replicas behind AWS ECS, App Runner, or an ALB-backed service.
- Scale on CPU, memory, request count, and p95 latency.
- Keep persistent state in PostgreSQL.
- Add Redis for shared cache in a future version.
- Add a queue for async explanation generation when real LLM calls are used.

## Vertical Scaling

- Increase PostgreSQL CPU and memory.
- Add pgvector HNSW or IVFFlat indexes for larger corpora.
- Tune connection pooling and Uvicorn workers.
- Batch embedding ingestion.
- Cache frequent eligibility and rule retrieval results.
- Tune top-k retrieval and embedding dimensions for latency.
