# Sprint 4.1 Backend Architecture: Message Broker & Semantic Storage

## 1. Message Broker (Redis Pub/Sub)
- **Component**: Redis
- **Purpose**: Enable asynchronous, event-driven communication between agents within a Pod.
- **Integration Point**: Refactor `server/services/queue_manager.py` or introduce `server/services/message_broker.py` to wrap Redis Pub/Sub functionality.
- **Data Flow**: Agents publish messages to a Pod-specific channel (`pod:{pod_id}:messages`). Subscribed agents receive messages asynchronously.

## 2. Semantic Storage (pgvector)
- **Component**: PostgreSQL with `pgvector` extension.
- **Purpose**: Long-term semantic memory storage for agents.
- **Integration Point**: 
  - Migrate local DB from SQLite to PostgreSQL in development/production.
  - Update SQLAlchemy models in `server/models.py` to include vector columns (e.g., `Vector(1536)` for OpenAI embeddings).
  - Add Alembic migration for `pgvector` extension and new vector columns.
- **Data Flow**: Text inputs -> Embedding generation (via `llm_runner.py` or new service) -> Stored in pgvector -> Vector similarity search for context retrieval.

## 3. DevOps Handoff Requirements
- Update `docker-compose.yml` to include a Redis container.
- Update `docker-compose.yml` to replace SQLite/default DB with a `pgvector`-enabled PostgreSQL container (e.g., `ankane/pgvector`).
- Update `deployment/kubernetes/configmap.yaml` and related manifests for Redis and PostgreSQL.
