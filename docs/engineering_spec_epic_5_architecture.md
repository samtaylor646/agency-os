# Engineering Specification: Epic 5 Architecture Review

## 1. Overview
As we transition from Epic 4 to Epic 5, the architectural focus shifts toward data governance, advanced agent orchestration, reporting, and a foundational marketplace. This document outlines the required architectural evolutions to support Epic 5, ensuring multi-tenant isolation, security, and scalability.

## 2. Advanced Analytics & Reporting Pipeline

### Current State
In Epic 4, webhooks and events rely on an in-memory `webhook_queue` within `server/routers/webhooks.py`. While sufficient for MVP validation, this will not scale for durable event tracking, billing metrics, or analytics.

### Epic 5 Requirements
- **Message Broker Integration:** Replace the in-memory queue with a durable message broker (e.g., Redis or RabbitMQ) for reliable asynchronous task processing and event routing.
- **Analytics Data Store:** Introduce a structured way to store time-series data (e.g., PostgreSQL with TimescaleDB or partitioned event tables) to track API usage, agent execution duration, token consumption, and success/failure rates per `tenant_id`.
- **Worker Processes:** Decouple event processing from the main FastAPI server by implementing background workers (e.g., using Celery or an asyncio-based worker polling the broker) to aggregate analytics without blocking the web thread.

## 3. Enhanced RBAC & Data Governance

### Current State
Role-Based Access Control is currently managed via a static `RoleEnum` (Super Admin, Agency Admin, Client Approver, Client Read-Only) in `server/models.py`.

### Epic 5 Requirements
- **Granular Permissions System:** Migrate from a static enum to dynamic Role and Permission relational tables.
  - `Permission` table: Defines specific actions (e.g., `view:analytics`, `execute:agent`, `manage:billing`).
  - `Role` table: Defines named roles that group multiple permissions.
  - `WorkspaceMemberRole` mapping: Maps users to roles within a specific workspace context.
- **Audit Logging:** Implement a middleware or decorator to automatically log significant state changes (CRUD operations, agent invocations) to a secure `audit_logs` table, ensuring compliance and traceability per workspace.

## 4. Marketplace & Templates Architecture

### Current State
Agents and workflows are primarily defined in static Markdown (`.md`) files in the `agents/` directory, which is parsed by the NEXUS pipeline.

### Epic 5 Requirements
- **Template Registry:** Establish a database schema for storing generic "Template" definitions (Agents, DAG Workflows) so that agencies can install or clone templates into their specific workspace context.
- **Workspace-Specific Overrides:** Allow agencies to fork a base Markdown agent template and apply custom system prompts or tools. This requires storing modified agent states in the database or a tenant-isolated storage partition (e.g., S3 bucket with tenant prefixes).
- **Versioning:** Introduce version control for marketplace assets to ensure updates do not break existing agency workflows.

## 5. Next Steps
1. **Database Migrations:** Engineering to draft Alembic migrations for Analytics tables, new RBAC models, and Audit Logs.
2. **Infrastructure:** DevOps to provision a Redis instance (or alternative message broker) in the staging and production environments.
3. **PRD Alignment:** Cross-reference this technical spec with `prd_epic_5.md` once finalized by the Product Manager.
