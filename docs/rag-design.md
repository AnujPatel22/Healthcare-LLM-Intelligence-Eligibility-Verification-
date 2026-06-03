# RAG Design

The RAG flow embeds synthetic payer rule text and codebook text with deterministic local embeddings. Payer rules are stored in PostgreSQL using pgvector-compatible columns.

Retrieval steps:

1. Build a query from payer, service type, diagnosis, procedure, and code references.
2. Filter by payer/service/code when provided.
3. Score candidates using cosine similarity plus exact token/code boosts.
4. Return cited snippets and rule IDs.
5. Feed rule matches and codebook matches into the mock explanation client.

The project imports LangChain document primitives where practical, but does not require an external LLM or embedding API.
