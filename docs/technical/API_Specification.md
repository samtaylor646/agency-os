# API Specification

This document details the RESTful API for AgencyOS. The API is built using FastAPI and follows standard conventions, utilizing JWT-based authentication and strict tenant-level isolation.

## Global Concepts

### Base URL
All API endpoints are mounted under the `/api/v1` prefix.
```
http://<host>:<port>/api/v1
```

### Authentication & Authorization
AgencyOS uses OAuth2 Password Flow with Bearer Tokens (JWT).
- **Header:** `Authorization: Bearer <access_token>`
- **Tenant Context:** Multi-tenancy is enforced using the `X-Tenant-ID` HTTP header. For almost all requests, `X-Tenant-ID` is required to ensure data is strictly scoped.

### Validation & Errors
All validation errors return `422 Unprocessable Entity` formatted according to Pydantic/FastAPI defaults. PII (Personally Identifiable Information) in validation error responses is automatically redacted by the global middleware (e.g., `[REDACTED_EMAIL]`, `[REDACTED_API_KEY]`).

---

## 1. Authentication (`/token`)

### Generate Access Token
`POST /api/v1/token`

Exchange user credentials for a JWT access token.
- **Content-Type:** `application/x-www-form-urlencoded`
- **Body:**
  - `username` (string, email address)
  - `password` (string)
- **Response `200 OK`:**
  ```json
  {
    "access_token": "eyJhbG...",
    "token_type": "bearer"
  }
  ```

---

## 2. Workspaces (`/workspaces`)

### List Workspaces
`GET /api/v1/workspaces`

Returns a list of workspaces the authenticated user has access to. Super Admins receive all workspaces.
- **Response `200 OK`:**
  ```json
  [
    {
      "id": 1,
      "name": "Acme Agency",
      "settings_json": {},
      "created_at": "2026-05-29T10:00:00Z"
    }
  ]
  ```

### Create Workspace
`POST /api/v1/workspaces`

Creates a new workspace and automatically assigns the creator as an `Agency Admin`.
- **Body:**
  ```json
  {
    "name": "New Agency",
    "settings_json": {}
  }
  ```
- **Response `201 Created`:** Workspace object.

### Invite User
`POST /api/v1/workspaces/{workspace_id}/invites`

Invite a user to a workspace.
- **Headers:** `X-Tenant-ID: {workspace_id}`
- **Body:**
  ```json
  {
    "email": "user@example.com",
    "role": "Client Read-Only"
  }
  ```

---

## 3. Workflows & Pipelines

### Execute DAG Workflow
`POST /api/v1/workflows/run`

Triggers the execution of a multi-agent Directed Acyclic Graph (DAG) workflow.
- **Headers:** `X-Tenant-ID: <id>`
- **Body:**
  ```json
  {
    "nodes": [
      {
        "node_id": "step_1",
        "agent_name": "researcher",
        "task": "Find market trends",
        "required_inputs": []
      }
    ],
    "edges": [
      {
        "from_node": "step_1",
        "to_node": "step_2"
      }
    ]
  }
  ```
- **Response `200 OK`:**
  ```json
  {
    "status": "success",
    "results": { ... }
  }
  ```

---

## 4. Custom Agents (`/custom_agents`)
Standard CRUD endpoints for dynamically compiled specialized agents.
- `GET /api/v1/custom_agents`: List agents.
- `POST /api/v1/custom_agents`: Generate a new agent and deploy `.py` file to `/agents`.
- `GET /api/v1/custom_agents/{id}`: Retrieve agent details.
- `DELETE /api/v1/custom_agents/{id}`: Archive/delete agent.

## 5. Memory & Documents (`/documents`)
Endpoints for RAG (Retrieval-Augmented Generation) ingestion.
- `POST /api/v1/documents`: Upload file (PDF, TXT, MD). Triggers semantic chunking and `pgvector` indexing.
- `GET /api/v1/documents`: List available workspace documents.
- `GET /api/v1/documents/search`: Execute similarity search against vector store.

## 6. Projects & Chat Contexts (`/projects`, `/chat`)
- `GET /api/v1/projects`: List projects within the tenant.
- `POST /api/v1/projects`: Create project.
- `GET /api/v1/chat`: List chat sessions.
- `POST /api/v1/chat/{chat_id}/messages`: Append user message to thread and trigger LLM streaming response.

## 7. Configuration & Security
- **Credentials (`/credentials`)**: Manage encrypted LLM API Keys (OpenAI, Anthropic).
- **API Keys (`/api_keys`)**: Issue platform programmatic access tokens.
- **Webhooks (`/webhooks`)**: Register and manage outbound event hooks.
- **RBAC (`/rbac`)**: Manage granular roles and permissions (Admin, Approver, Read-Only).
- **Audit (`/audit`)**: Retrieve immutable audit log trails for compliance reporting.
