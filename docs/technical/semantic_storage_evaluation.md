# Semantic Storage Foundation Evaluation (Sprint 4.2)

## Executive Summary
This document evaluates the architectural options for implementing the Semantic Storage Foundation in AgencyOS. Given our current Dockerized FastAPI and React stack, the goal is to choose a vector storage solution and embedding strategy that balances operational simplicity, performance, scalability, and cost.

**Primary Recommendation:** Utilize **pgvector** as an extension to our existing PostgreSQL database, adopt a **pluggable embedding architecture** (starting with OpenAI's `text-embedding-3-small` for speed to market, with a clear path to local Open Source models), and implement a **hybrid relational-vector schema** for storing documents and conversations.

---

## 1. Database Choice: pgvector vs. Dedicated Vector DBs

We need a database to store and query high-dimensional vectors representing our documents and agent conversations.

### Option A: pgvector (PostgreSQL Extension)
Since we already utilize PostgreSQL in our Dockerized environment, `pgvector` adds vector similarity search capabilities directly to our existing database.

**Pros:**
*   **Operational Simplicity:** No new infrastructure to manage. It fits perfectly into our existing `docker-compose.yml` and Kubernetes manifests.
*   **ACID Compliance:** Transactions span both relational metadata (e.g., RBAC, Workspace IDs) and vector data, preventing orphan records.
*   **Simplified Filtering:** Pre-filtering vectors by tenant/workspace is trivial using standard SQL `WHERE` clauses alongside `ORDER BY vector <-> query`.
*   **Reduced Cost:** No additional SaaS subscriptions or separate database clusters to provision.

**Cons:**
*   **Scale Limits:** While algorithms like HNSW have improved pgvector's performance, it may become a bottleneck if we scale to billions of vectors compared to specialized distributed systems.
*   **Resource Contention:** Heavy vector searches share CPU and memory with standard transactional queries.

### Option B: Dedicated Vector Databases (Pinecone, Weaviate, Milvus, Qdrant)
These are purpose-built systems for managing vector embeddings at massive scale.

**Pros:**
*   **Extreme Scale & Speed:** Built specifically for low-latency similarity search across billions of records.
*   **Advanced Features:** Often include built-in document chunking, hybrid search (keyword + vector), and automatic embedding generation (e.g., Weaviate).
*   **Isolation:** Vector workloads do not impact relational database performance.

**Cons:**
*   **Operational Overhead:** Requires managing a new distributed system in Docker/Kubernetes (e.g., Milvus/Weaviate) or relying on a managed SaaS (Pinecone), which complicates local development and adds network latency.
*   **Data Synchronization:** Requires maintaining consistency between the primary database (PostgreSQL) and the vector database.
*   **Complex Multi-tenancy:** Enforcing strict workspace isolation across two separate data stores requires careful engineering.

### **Recommendation: pgvector**
For our current scale and Dockerized FastAPI architecture, **pgvector** is the clear winner. The operational simplicity of having a single source of truth for both relational metadata and embeddings far outweighs the potential extreme-scale benefits of a dedicated vector database at this stage. It guarantees data consistency and simplifies our deployment footprint.

---

## 2. Embedding Model: OpenAI vs. Open Source

Embeddings convert text into the vector representations required for semantic search.

### Option A: OpenAI API (`text-embedding-3-small` / `text-embedding-3-large`)
**Pros:**
*   **Ease of Use:** Simple API call from FastAPI. No infrastructure to manage.
*   **High Quality:** State-of-the-art performance on retrieval benchmarks (MTEB).
*   **Multilingual:** Excellent support out-of-the-box.
*   **Dimension Flexibility:** `text-embedding-3` allows truncating dimensions to save storage space without significant quality loss.

**Cons:**
*   **Cost:** API usage costs scale with volume.
*   **Privacy/Security:** Sensitive agency data must be sent to a third party (OpenAI).
*   **Latency:** Network call required for every ingestion and search.

### Option B: Open Source Local Models (e.g., BGE-m3, Nomic-Embed-Text via Ollama or HuggingFace)
**Pros:**
*   **Privacy First:** Data never leaves the Docker network. Ideal for strict compliance requirements.
*   **No Recurring Cost:** Free to run, bounded only by our own infrastructure.
*   **Control:** Absolute control over latency and model versioning.

**Cons:**
*   **Infrastructure Overhead:** Requires adding an inference service (like Ollama or a custom Python worker) to our Docker stack.
*   **Resource Intensive:** Requires significant RAM and ideally GPU acceleration for fast ingestion of large documents.

### **Recommendation: Pluggable Architecture (Start OpenAI, Fast Follow Open Source)**
We should implement a generic `EmbeddingProvider` interface in FastAPI. 
1.  **Phase 1 (Sprint 4.2 MVP):** Implement the OpenAI provider using `text-embedding-3-small`. It is extremely cheap ($0.02 / 1M tokens), fast, and requires zero Docker infrastructure changes, allowing us to focus on building the RAG pipeline and DB schema.
2.  **Phase 2:** Implement a local provider using an Open Source model hosted in a new Docker container (e.g., an Ollama service in `docker-compose.yml`), offering a "Privacy Mode" for sensitive workspaces.

---

## 3. Architecture for Storing Agent Conversations and Documents

To effectively use pgvector in our FastAPI stack, we will use a hybrid relational-vector schema.

### Database Schema Design (PostgreSQL + pgvector)

We will structure our tables to separate the parent object from the vectorized chunks, ensuring efficient metadata filtering.

```sql
-- Enable the extension
CREATE EXTENSION IF NOT EXISTS vector;

-- 1. Document Storage
CREATE TABLE documents (
    id UUID PRIMARY KEY,
    workspace_id UUID REFERENCES workspaces(id),
    filename VARCHAR(255),
    content_type VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE document_chunks (
    id UUID PRIMARY KEY,
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    workspace_id UUID REFERENCES workspaces(id), -- Denormalized for fast filtering
    chunk_index INTEGER,
    text_content TEXT,
    embedding vector(1536) -- Size matches OpenAI text-embedding-3-small
);

-- Index for fast vector search (HNSW)
CREATE INDEX ON document_chunks USING hnsw (embedding vector_cosine_ops);
CREATE INDEX ON document_chunks (workspace_id);

-- 2. Conversation Storage (Memory)
CREATE TABLE agent_sessions (
    id UUID PRIMARY KEY,
    workspace_id UUID REFERENCES workspaces(id),
    agent_id UUID,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE session_messages (
    id UUID PRIMARY KEY,
    session_id UUID REFERENCES agent_sessions(id) ON DELETE CASCADE,
    workspace_id UUID REFERENCES workspaces(id),
    role VARCHAR(50), -- 'user', 'assistant', 'system'
    content TEXT,
    embedding vector(1536),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX ON session_messages USING hnsw (embedding vector_cosine_ops);
CREATE INDEX ON session_messages (workspace_id, session_id);
```

### FastAPI Ingestion & Retrieval Flow

1.  **Ingestion Pipeline (FastAPI Background Tasks / Celery):**
    *   File uploaded via React UI -> FastAPI endpoint.
    *   `DocumentParserService` extracts raw text.
    *   `ChunkingService` splits text into logical segments (e.g., 500 tokens with 50-token overlap).
    *   `EmbeddingService` calls OpenAI to get vectors for each chunk.
    *   `StorageService` inserts rows into `documents` and `document_chunks`.

2.  **Retrieval Augmented Generation (RAG) Flow:**
    *   Agent receives a user prompt.
    *   `EmbeddingService` vectorizes the user prompt.
    *   SQL query executes: `SELECT text_content FROM document_chunks WHERE workspace_id = $1 ORDER BY embedding <-> $2 LIMIT 5`.
    *   Retrieved chunks are injected into the LLM context window.

---

## 4. DevOps & Infrastructure Review

### Review Notes & Approvals
**Status: Approved with Recommendations**

From an infrastructure and operational standpoint, the proposed `pgvector` and pluggable embedding architecture aligns well with our current operational maturity and deployment capabilities. 

### Infrastructure & Deployment Implications

#### 1. Dockerized Environment (Local/Dev)
*   **PostgreSQL Image:** We must update our local `docker-compose.yml` to use an official `pgvector` image (e.g., `pgvector/pgvector:pg16` or building a custom image derived from our current Postgres base). This avoids compiling the extension from source during local container startup, ensuring fast and consistent dev environments.
*   **Pluggable Architecture Strategy:** Starting with OpenAI for Phase 1 minimizes the immediate footprint of our local Docker stack. When we move to Phase 2 (Local Open Source Models via Ollama/HuggingFace), we will need to introduce hardware-conditional profiles in `docker-compose.yml` (e.g., `--profile gpu` or `--profile cpu`) because adding a heavy inference container will severely impact developers running on resource-constrained machines.

#### 2. Kubernetes Manifests (Production)
*   **StatefulSets & Storage:** `pgvector` introduces new I/O profiles. While vector indices (like HNSW) are RAM-heavy during generation and querying, the persistent storage tier requires high IOPS. Our current PostgreSQL `StatefulSet` and PersistentVolumeClaims (PVCs) need to be reviewed to ensure we are provisioning appropriately high-throughput storage classes in Kubernetes.
*   **Resource Requests/Limits:** Vector searches, particularly building HNSW indexes, can cause CPU and memory spikes. The `resources.requests` and `resources.limits` in our `deployment/kubernetes/postgres.yaml` will need an immediate bump. We must establish robust monitoring to track PostgreSQL memory usage to prevent Kubernetes OOMKills.
*   **Database Migrations:** Integrating the `CREATE EXTENSION IF NOT EXISTS vector;` step into our automated database migration strategy (e.g., Alembic for FastAPI) is critical. The DB user executing migrations must have the required privileges to create extensions in the target environment.

#### 3. CI/CD Pipelines
*   **Testing:** CI pipelines must be updated to use the `pgvector`-enabled database image for integration and automated tests. Relying on mocks for vector search is insufficient; we need actual `pgvector` instances running in our pipeline.
*   **Automated Deployments:** No significant changes to the CD pipeline itself, as this is fundamentally a database schema and application code update. However, the initial migration that creates the vector extension and indexes should be treated as a high-risk deployment due to the potential locks and resource consumption on large tables. We recommend applying the index creation concurrently (`CREATE INDEX CONCURRENTLY ...`) if implemented on a live database with existing data.

### Required DevOps Actions for Sprint 4.2
1.  **[ ]** Update `docker-compose.yml` (root and `deployment/`) to use a dedicated `pgvector` image.
2.  **[ ]** Update `deployment/kubernetes/postgres.yaml` to ensure the correct image is used and adjust memory/CPU resource limits.
3.  **[ ]** Update CI test service definitions to spin up the `pgvector`-enabled Postgres container for the test suite.

---

### Conclusion
By leveraging `pgvector` alongside a well-structured FastAPI service layer that abstracts the embedding provider, we maintain the operational simplicity of our Dockerized stack while building a robust, production-ready semantic memory foundation.