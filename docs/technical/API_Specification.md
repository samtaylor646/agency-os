# API Specification

## 1. Overview
The AgencyOS API is a RESTful and WebSocket-based API built with FastAPI.
* **Base URL (Local):** `http://localhost:8000/api/v1`
* **Content-Type:** `application/json`
* **Versioning:** Major versioning in the URL (`/v1/`).

## 2. Authentication & Authorization
* **Method:** JWT (JSON Web Tokens) passed in the `Authorization` header (`Bearer <token>`).
* **RBAC:** Roles include `admin`, `workspace_owner`, and `member`. Endpoints enforce role checks at the route level via FastAPI dependencies.

## 3. Endpoints

### 3.1. Workspaces
#### `GET /workspaces`
* **Description:** Retrieves all workspaces the authenticated user has access to.
* **Responses:**
  * `200 OK`: `{"data": [{"id": "uuid", "name": "Workspace A", "role": "admin"}]}`

#### `POST /workspaces`
* **Description:** Create a new workspace.
* **Request Body:**
  ```json
  {
    "name": "Acme Corp Workspace",
    "description": "Internal marketing AI pod"
  }
  ```
* **Responses:**
  * `201 Created`: Returns the created workspace object.

### 3.2. Agents & Pods
#### `GET /workspaces/{workspace_id}/agents`
* **Description:** List all custom and system agents available in the workspace.
* **Responses:**
  * `200 OK`: `{"data": [{"id": "uuid", "name": "Product Manager", "model": "gpt-4o"}]}`

#### `POST /workspaces/{workspace_id}/pods`
* **Description:** Provision a new Agent Pod (a team of agents working together).
* **Request Body:**
  ```json
  {
    "name": "Launch Team",
    "agents": ["agent_uuid_1", "agent_uuid_2"]
  }
  ```
* **Responses:**
  * `201 Created`: Returns the provisioned Pod.

### 3.3. Execution & Chat
#### `POST /pods/{pod_id}/messages`
* **Description:** Send a message to an active Agent Pod.
* **Request Body:**
  ```json
  {
    "content": "Start the market research analysis for Product X",
    "attachments": []
  }
  ```
* **Responses:**
  * `202 Accepted`: Message queued for agent processing.

#### `WS /ws/pods/{pod_id}`
* **Description:** WebSocket connection for real-time streaming of agent responses, thoughts, tool invocations, and sandbox logs.

## 4. Error Handling
Standardized JSON error format:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The provided agent ID is invalid.",
    "details": [...]
  }
}
```
* **Common Codes:** `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `422 Unprocessable Entity` (FastAPI Validation), `500 Internal Server Error`.