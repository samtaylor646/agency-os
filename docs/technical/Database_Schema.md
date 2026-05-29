# Database Schema

## 1. Overview
AgencyOS utilizes **PostgreSQL** as its primary relational database for persistent state. It leverages SQLAlchemy as the ORM, with UUIDs as primary keys for all core entities to ensure globally unique identification and security against enumeration.

## 2. Entity Relationship Diagram (ERD)
* **Users** (1:N) **WorkspaceMembers** (N:1) **Workspaces**
* **Workspaces** (1:N) **Agents**
* **Workspaces** (1:N) **Pods**
* **Pods** (1:N) **Messages**
* **Agents** (M:N) **Pods** (via `pod_agents` join table)

## 3. Tables

### 3.1. `users`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PRIMARY KEY | Unique identifier for the user. |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | User's email address. |
| `hashed_password` | VARCHAR | NOT NULL | Bcrypt hashed password. |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Record creation timestamp. |

### 3.2. `workspaces`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PRIMARY KEY | Workspace identifier. |
| `name` | VARCHAR(255) | NOT NULL | Display name of the workspace. |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Record creation timestamp. |

### 3.3. `workspace_members`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `user_id` | UUID | FOREIGN KEY (users) | Reference to the user. |
| `workspace_id` | UUID | FOREIGN KEY (workspaces) | Reference to the workspace. |
| `role` | VARCHAR(50) | NOT NULL | e.g., 'owner', 'admin', 'member' |

### 3.4. `agents`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PRIMARY KEY | Agent configuration identifier. |
| `workspace_id` | UUID | FOREIGN KEY (workspaces) | The workspace this agent belongs to. |
| `name` | VARCHAR(255) | NOT NULL | Agent display name. |
| `system_prompt` | TEXT | NOT NULL | The base instruction set for the LLM. |
| `model_slug` | VARCHAR(100) | NOT NULL | e.g., 'gpt-4o', 'claude-3-5-sonnet'. |
| `tools` | JSONB | DEFAULT '{}' | Array of permitted MCP tools/skills. |

### 3.5. `pods`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PRIMARY KEY | Pod identifier. |
| `workspace_id` | UUID | FOREIGN KEY (workspaces) | The workspace this pod belongs to. |
| `name` | VARCHAR(255) | NOT NULL | Session / team name. |
| `status` | VARCHAR(50) | DEFAULT 'active' | active, paused, archived. |

### 3.6. `messages`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PRIMARY KEY | Message identifier. |
| `pod_id` | UUID | FOREIGN KEY (pods) | The pod thread this message belongs to. |
| `sender_type` | VARCHAR(50) | NOT NULL | 'user', 'agent', 'system'. |
| `sender_id` | UUID | NULLABLE | Refers to user.id or agent.id. |
| `content` | TEXT | NOT NULL | The actual message content. |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Message timestamp. |

## 4. Migrations & Versioning
* Migrations are managed using **Alembic**.
* All schema changes must be accompanied by an Alembic revision file generated via `alembic revision --autogenerate -m "description"`.
* Migrations are automatically applied during deployment pipelines via the standard kickoff protocol.