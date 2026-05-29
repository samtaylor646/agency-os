# Technical Debt and Refactoring Plan

## Overview
This document outlines the top technical debt items within the AgencyOS architecture that require addressing before the system can be considered robust for production. As the system has rapidly scaled to include specialized agents, complex DAG workflows, and dynamic environments, several architectural shortcuts have emerged.

## Major Technical Debt Items

### 1. Monolithic Orchestration in `central_runner.py`
**Description:** The `central_runner.py` script currently handles too much responsibility, acting as a monolithic orchestrator for pipelines, validation, and agent execution. It tightly couples task routing with execution logic.
**Impact:** 
- Hard to scale horizontally as pipeline execution is bound to this single process bottleneck.
- Testing is complex due to deep dependencies on external systems (LLMs, databases) within the core runner loop.
- Difficult to implement proper dead-letter queues, task retries, and distributed tracing.
**Refactoring Plan:**
- **Decompose the Runner:** Split `central_runner.py` into smaller, event-driven micro-workers utilizing a robust message broker (e.g., RabbitMQ or Redis Streams).
- **Introduce a State Machine:** Replace the linear/DAG execution logic with a durable workflow engine (like Temporal or Celery) to handle retries, timeouts, and state persistence natively.

### 2. Sandbox Isolation and Lifecycle Management
**Description:** Docker sandbox execution (e.g., for Python code execution via `server/routers/sandbox.py`) lacks rigorous lifecycle constraints, resource quotas (CPU/Memory limits), and concurrent scaling strategies.
**Impact:** 
- Security vulnerabilities from potentially escaping sandboxes or consuming host resources (noisy neighbor problem).
- Zombie containers can accumulate if execution fails or times out improperly, leading to storage and memory exhaustion.
**Refactoring Plan:**
- **Resource Quotas:** Enforce strict Docker resource limits (CPU, memory, network isolation) in the sandbox instantiation logic.
- **Ephemeral Firecracker MicroVMs:** Transition from standard Docker containers to Firecracker microVMs or gVisor for enhanced security and faster startup times for untrusted code execution.
- **Reaper Service:** Implement a background cron or daemon to prune orphaned sandboxes aggressively.

### 3. Synchronous Database & pgvector Operations
**Description:** Some FastAPI endpoints and backend operations perform synchronous or unoptimized vector similarity searches against `pgvector` and standard relational tables.
**Impact:** 
- High latency during vector searches blocks the ASGI event loop, decreasing the overall throughput of the API.
- Connection pool exhaustion under high concurrent load during agent ingestion or complex contextual memory retrieval.
**Refactoring Plan:**
- **Asynchronous DB Drivers:** Ensure 100% usage of async database drivers (e.g., `asyncpg` with SQLAlchemy 2.0 async sessions) across all endpoints.
- **Index Optimization:** Review and implement HNSW (Hierarchical Navigable Small World) indices on all `pgvector` embeddings columns to drastically reduce search latency compared to flat exact nearest neighbor searches.
- **Caching Layer:** Introduce a Redis caching layer for frequently accessed context and exact-match semantic queries.

### 4. WebSocket State Management and Connection Dropping
**Description:** The real-time messaging and WebSocket infrastructure (`server/routers/websockets.py`) relies on in-memory state for connection management, lacking a distributed pub/sub backend.
**Impact:** 
- The system cannot be horizontally scaled (multiple API instances) because WebSocket messages intended for a client connected to Server A cannot be published by Server B.
- Connections are easily dropped and lose state during deployments or network blips without built-in recovery protocols.
**Refactoring Plan:**
- **Redis Pub/Sub Integration:** Decouple WebSocket connection state from the application memory by integrating Redis Pub/Sub. When a message is generated, it is published to a channel, and the specific node holding the client connection pushes it via WS.
- **Connection Resiliency:** Implement ping/pong heartbeats and client-side reconnection logic with message playback (last-event-id tracking) to recover lost messages during brief disconnects.
