# Architecture

The application is a Dockerized monorepo with a React frontend, FastAPI backend, and PostgreSQL database using pgvector.

```text
Browser
  -> React/Vite frontend
  -> FastAPI JSON API
  -> SQLAlchemy models and service layer
  -> PostgreSQL tables with pgvector rule/code embeddings
```

Core design choices:

- Business logic lives in service classes so it can be tested without a database.
- Database startup enables `vector` and seeds synthetic data automatically.
- RAG retrieval uses deterministic embeddings for offline operation and LangChain document objects where practical.
- Mock LLM output is grounded in retrieved rules and codebook matches.
