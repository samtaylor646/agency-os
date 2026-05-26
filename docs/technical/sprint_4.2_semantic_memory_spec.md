# Technical Specification: Sprint 4.2 - Semantic Memory Layer

## 1. Overview

This specification details the implementation plan for the Semantic Memory Layer in AgencyOS. Based on the architectural evaluation, we are utilizing **pgvector** as our vector storage foundation directly within our existing PostgreSQL infrastructure. We will adopt a **pluggable embedding architecture**, beginning with OpenAI's `text-embedding-3-small`, and implement a **hybrid relational-vector schema** for both document knowledge retrieval (RAG) and long-term agent conversational memory.

## 2. Database Schema & Alembic Migration Plan

### 2.1 Schema Design

We will introduce two primary domains: Document Storage (for RAG) and Conversation Storage (for agent memory).

#### Document Storage
*   **`documents`**: Metadata for uploaded files.
*   **`document_chunks`**: Segmented text chunks with their associated vector embeddings. Includes denormalized `workspace_id` for fast tenant filtering.

#### Conversation Storage
*   **`agent_sessions`**: Parent record for a specific agent interaction thread.
*   **`session_messages`**: Individual messages (user, assistant, system) with vector embeddings for semantic recall of past conversations.

### 2.2 Alembic Migration Strategy

The migration must be handled carefully to ensure the `pgvector` extension is enabled safely and indexes are created optimally.

**Migration Steps (Alembic Revision):**

1.  **Enable Extension**: Execute `CREATE EXTENSION IF NOT EXISTS vector;` (requires superuser or appropriate privileges).
2.  **Create Tables**: Define the relational schema using SQLAlchemy ORM mapping to `UUID`, `String`, `DateTime`, and the specialized `Vector` type from `pgvector-python`.
3.  **Index Creation**: Use HNSW indexes for fast cosine similarity search.
    *   *Note on Production Migrations*: For future data-heavy migrations, use `CREATE INDEX CONCURRENTLY` to avoid table locks. For this initial creation on empty tables, standard index creation is acceptable.

**SQLAlchemy Models Example:**
```python
from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from database import Base

class DocumentChunk(Base):
    __tablename__ = 'document_chunks'
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    document_id = Column(UUID(as_uuid=True), ForeignKey('documents.id', ondelete='CASCADE'))
    workspace_id = Column(UUID(as_uuid=True), index=True)
    chunk_index = Column(Integer)
    text_content = Column(Text)
    embedding = Column(Vector(1536)) # Dimension for text-embedding-3-small
```

## 3. FastAPI Embedding Service Interface

To support future local/open-source models, the embedding layer must be heavily abstracted.

### 3.1 Interface Definition

```python
from abc import ABC, abstractmethod
from typing import List

class EmbeddingProvider(ABC):
    @abstractmethod
    async def get_embedding(self, text: str) -> List[float]:
        """Returns a single vector embedding for a given string."""
        pass

    @abstractmethod
    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Returns a list of vector embeddings for batch processing."""
        pass
```

### 3.2 Phase 1 Implementation: OpenAI Provider

```python
import openai
from .provider_interface import EmbeddingProvider

class OpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(self, api_key: str, model: str = "text-embedding-3-small"):
        self.client = openai.AsyncClient(api_key=api_key)
        self.model = model

    async def get_embedding(self, text: str) -> List[float]:
        response = await self.client.embeddings.create(input=[text], model=self.model)
        return response.data[0].embedding

    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        response = await self.client.embeddings.create(input=texts, model=self.model)
        return [data.embedding for data in response.data]
```

*Dependency Injection*: The FastAPI app will bind the `EmbeddingProvider` interface to the `OpenAIEmbeddingProvider` via a factory function configurable via environment variables (`EMBEDDING_PROVIDER_TYPE=openai`).

## 4. RAG Ingestion and Retrieval Flow

### 4.1 Ingestion Pipeline
1.  **Upload Endpoint**: FastAPI endpoint receives file and `workspace_id`.
2.  **Parsing**: Extract raw text (e.g., using `PyPDF2` or `unstructured`).
3.  **Chunking**: Split text into overlapping segments (e.g., 500 tokens, 50 token overlap).
4.  **Embedding Generation**: Call `EmbeddingProvider.get_embeddings()` on the chunks.
5.  **Storage**: Transactionally insert the parent `Document` and multiple `DocumentChunk` records.

### 4.2 Retrieval Flow (Semantic Search)
1.  **Query Processing**: Agent receives user prompt.
2.  **Query Embedding**: Call `EmbeddingProvider.get_embedding(prompt)`.
3.  **Vector Search**: Execute SQL similarity search pre-filtered by `workspace_id`.
    ```sql
    SELECT text_content, document_id, 1 - (embedding <=> :query_embedding) as similarity
    FROM document_chunks
    WHERE workspace_id = :workspace_id
    ORDER BY embedding <=> :query_embedding
    LIMIT :top_k;
    ```
4.  **Context Injection**: Retrieve the `text_content` from the top results and inject them into the system prompt context window for the LLM.

## 5. DevOps Implementation Tasks

To support `pgvector`, the underlying infrastructure must be updated.

### 5.1 Docker Compose Updates
Update `docker-compose.yml` (and any local dev overrides) to use the official pgvector image.
*   **Action**: Change PostgreSQL image to `pgvector/pgvector:pg16`.

### 5.2 Kubernetes Production Manifests
Update `deployment/kubernetes/postgres.yaml`.
*   **Action**: Change the image to the pgvector equivalent.
*   **Action**: Increase `resources.requests.memory` and `resources.limits.memory` to handle HNSW index generation and vector search loads. 

### 5.3 CI/CD Adjustments
*   **Action**: Ensure the CI pipeline uses the `pgvector/pgvector:pg16` image for integration tests, allowing SQLAlchemy tests to successfully execute vector queries.
*   **Action**: Implement secure secret management for `OPENAI_API_KEY` and any future embedding provider keys across all environments (Local dev, CI/CD, and Prod).

## 6. Sprint Execution / Todo Plan

**Database & DevOps (Backend/DevOps Role)**
- [x] Update `docker-compose.yml` with `pgvector/pgvector:pg16`.
- [x] Update `deployment/kubernetes/postgres.yaml` image and resource limits.
- [x] Configure CI environment to support `pgvector`.
- [x] Write Alembic migration to enable `pgvector` extension.
- [x] Write Alembic migration for `documents`, `document_chunks`, `agent_sessions`, and `session_messages` tables with HNSW indexes.
- [x] Validate environment variable injection for embedding secrets in CI/CD.

**Services & Abstractions (Backend Role)**
- [x] Create `EmbeddingProvider` abstract base class.
- [x] Implement `OpenAIEmbeddingProvider` using `text-embedding-3-small`.
- [x] Set up FastAPI Dependency Injection for the provider.

**Ingestion & Retrieval APIs (Backend Role)**
- [x] Implement document parsing and chunking logic.
- [x] Build FastAPI `POST /api/documents/ingest` endpoint.
- [x] Build vector similarity search function in the repository layer.
- [x] Integrate semantic search into the Agent execution pipeline (Context Injection).

**Security (Security Role)**
- [x] Implement API layer RBAC checks to verify the authenticated user has explicit read/write access to the requested `workspace_id` prior to executing ingestion or vector retrieval.
- [x] Define rate-limiting and payload size limits for document ingestion to prevent denial-of-wallet (DoW) attacks via OpenAI API exhaustion.
- [x] Document data poisoning prevention strategies and sanitation logic for text chunking prior to embedding generation.

**Quality Assurance (Evidence Collector Role)**
- [x] Write integration tests for vector insertion and retrieval.
- [x] Verify multi-tenant isolation (`workspace_id` filtering) works correctly during retrieval.
- [x] Conduct performance testing on ingestion throughput and search latency.
- [x] Test edge cases (e.g., malformed documents, extremely large payloads, and empty strings).
- [x] Validate CI pipeline successfully spins up `pgvector` and executes SQLAlchemy vector queries.

## 7. Cross-Functional Review Board Sign-off

| Role | Sign-off Status | Reviewer Notes |
| :--- | :--- | :--- |
| **Backend Architect** | [x] Approved | Architecture aligns with pgvector evaluation and ensures scalable abstraction for future local LLM integration. |
| **DevOps Engineer** | [x] Approved | CI/CD and Kubernetes resource adjustments are clearly scoped. Local dev parity is maintained. |
| **Security Analyst** | [x] Approved | RBAC isolation explicitly documented for both vector storage filtering and API request validation. Rate limiting and sanitization added to tasks. |
| **QA (Evidence Collector)** | [x] Approved | Test plans adequately cover CI pipeline validation, performance benchmarks, boundary testing, and isolation guarantees. |
