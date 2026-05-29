# Database Schema Specification

This document details the database schema for AgencyOS. It reflects the structure defined via SQLAlchemy models (`server/models.py`) and Alembic migrations. The database leverages PostgreSQL with the `pgvector` extension for semantic search and embeddings.

## Core Multi-Tenancy (Workspaces)

AgencyOS uses a logical isolation approach. Most tables require a `tenant_id` (or `workspace_id`) to ensure data is strictly segregated per workspace.

### `workspaces`
Represents an isolated tenant environment within the platform.
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PK, Indexed | Unique identifier for the workspace |
| `name` | String(255) | Indexed, Not Null | Human-readable name |
| `created_at` | DateTime(TZ) | Default: now() | Timestamp of creation |
| `settings_json` | JSON | Default: `{}` | Workspace-specific configuration |
| `encrypted_dek` | String(255) | Nullable | Encrypted data encryption key for tenant data |

### `users`
Global users that can be associated with multiple workspaces.
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PK, Indexed | Unique user identifier |
| `email` | String(255) | Unique, Indexed, Not Null | User email address |
| `hashed_password` | String(255) | Not Null | Bcrypt hashed password |
| `created_at` | DateTime(TZ) | Default: now() | Timestamp of creation |
| `tenant_id` | Integer | FK(`workspaces.id`) | Primary/Default workspace context |

### `workspace_members`
Junction table managing users' access and roles within specific workspaces.
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PK, Indexed | Unique membership identifier |
| `workspace_id` | Integer | FK(`workspaces.id`), Not Null | Associated workspace |
| `user_id` | Integer | FK(`users.id`), Not Null | Associated user |
| `role` | String(255) | Default: 'Client Read-Only' | Base RBAC role in this workspace |

## Security & Credentials

### `workspace_api_keys`
API keys issued for programmatic access to a specific workspace.
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PK, Indexed | Key identifier |
| `workspace_id` | Integer | FK(`workspaces.id`), Not Null | Associated workspace |
| `name` | String(255) | Not Null | Key description/label |
| `prefix` | String(255) | Not Null | Unhashed prefix (e.g., `ak_1234`) |
| `hashed_key` | String(255) | Not Null | Securely hashed full API key |
| `created_at` | DateTime(TZ) | Default: now() | Creation timestamp |
| `expires_at` | DateTime(TZ) | Nullable | Expiration timestamp |
| `is_active` | Integer | Default: 1 | 1 for active, 0 for revoked |

### `credentials`
Third-party credentials (e.g., LLM providers) stored securely per tenant.
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PK, Indexed | Credential identifier |
| `tenant_id` | Integer | FK(`workspaces.id`), Not Null | Associated workspace |
| `provider` | String(255) | Not Null | Provider name (e.g., 'openai', 'anthropic') |
| `encrypted_key` | String(255) | Not Null | AES-256-GCM encrypted API key |
| `created_at` | DateTime(TZ) | Default: now() | Creation timestamp |
| `updated_at` | DateTime(TZ) | | Last update timestamp |

## Agents & Pipelines

### `custom_agents`
User-defined or dynamically created specialized agents.
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | String(255) | PK, Indexed | Unique agent identifier (usually UUID) |
| `name` | String(255) | Not Null | Agent display name |
| `role` | String(255) | Not Null | Functional role |
| `filepath` | String(255) | Unique, Not Null | Path to the generated Python file |
| `tenant_id` | Integer | FK(`workspaces.id`), Not Null | Associated workspace |
| `created_at` | DateTime(TZ) | Default: now() | Creation timestamp |

### `workflow_executions` (Pipelines)
Tracks the state and progression of DAG-based multi-agent workflows.
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | String(255) | PK, Indexed | Workflow run identifier (UUID) |
| `tenant_id` | Integer | FK(`workspaces.id`), Not Null | Associated workspace |
| `pipeline_id` | String(255) | Nullable | Template/Pipeline ID |
| `status` | String(50) | Default: 'PENDING' | Execution state (RUNNING, COMPLETED, etc.) |
| `completed_nodes` | JSON | Default: `[]` | List of successfully executed node IDs |
| `failed_nodes` | JSON | Default: `[]` | List of failed node IDs |
| `execution_context` | JSON | Default: `{}` | Shared state and payload data for the DAG |
| `retry_counts` | JSON | Default: `{}` | Tracks retries per node |

## Projects & Chat (Frontend Contexts)

### `projects`
Logical groupings for related chats and workflows.
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PK, Indexed | Project identifier |
| `name` | String(255) | Not Null | Project name |
| `description` | String | Nullable | Project description |
| `tech_stack` | JSON | Default: `[]` | Identified technologies |
| `workspace_id` | Integer | FK(`workspaces.id`), Not Null | Associated workspace |

### `chats`
Interactive conversational sessions.
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PK, Indexed | Chat session identifier |
| `project_id` | Integer | FK(`projects.id`), Nullable | Optional parent project |
| `workspace_id` | Integer | FK(`workspaces.id`), Not Null | Associated workspace |
| `name` | String(255) | Nullable | Session title |

### `chat_messages`
Messages within a chat session.
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PK, Indexed | Message identifier |
| `chat_id` | Integer | FK(`chats.id`), Not Null | Parent chat session |
| `role` | String(50) | Not Null | 'user', 'assistant', 'system' |
| `content` | String | Not Null | Message text/markdown |

## Semantic Memory & Documents (Vector Data)

The system leverages `pgvector` for semantic search across documents and chat memory.

### `documents`
Uploaded or generated documents.
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PK, Indexed | Document identifier |
| `chat_id` | Integer | Indexed, Nullable | Associated context |
| `title` | String(255) | Not Null | Document title |
| `content` | String | Not Null | Full raw content |
| `type` | String(50) | Not Null | MIME/File type |
| `embedding` | Vector(1536) | Nullable | Whole-document semantic embedding |

### `document_chunks`
Vectorized semantic chunks for precise RAG context retrieval.
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Chunk identifier |
| `document_id` | Integer | FK(`documents.id`), Not Null | Parent document |
| `workspace_id` | Integer | Indexed, Not Null | Associated workspace (tenant isolation) |
| `chunk_index` | Integer | Not Null | Ordering index |
| `text_content` | String | Not Null | The chunk text |
| `embedding` | Vector(1536) | Nullable | Vector embedding |

## Audit & Telemetry

### `audit_logs`
Immutable record of system actions for compliance.
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PK, Indexed | Log entry identifier |
| `workspace_id` | Integer | FK(`workspaces.id`), Not Null | Tenant context |
| `user_id` | Integer | FK(`users.id`), Nullable | Actor executing action |
| `action` | String(255) | Not Null | Action verb (e.g., 'CREATE_WORKSPACE') |
| `resource_type` | String(255) | Nullable | Target entity type |
| `resource_id` | String(255) | Nullable | Target entity ID |
| `details` | JSON | Nullable | Extraneous metadata |

### `agent_execution_metrics`
Telemetry for LLM usage and performance.
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PK, Indexed | Metric identifier |
| `workspace_id` | Integer | FK(`workspaces.id`), Not Null | Tenant context |
| `agent_id` | Integer | Nullable | Specific agent ID |
| `agent_name` | String(255) | Not Null | Name of the agent |
| `execution_duration_ms` | Integer | Not Null | Time to complete task |
| `tokens_used` | Integer | Default: 0 | API token consumption |
| `status` | String(255) | Not Null | SUCCESS / FAILED |
| `error_message` | String(255) | Nullable | Stack trace / Error |
