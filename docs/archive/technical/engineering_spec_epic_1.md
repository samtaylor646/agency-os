# Engineering Specifications: Epic 1 (Multi-Tenant Workspace)

## 1. Overview
This specification details the technical requirements for building the Foundation phase of AgencyOS: Multi-Tenant Workspaces & Client Portals. This must be implemented *before* the core agent engine to ensure all agent executions are securely bound to specific client environments.

## 2. Core Architecture Decisions

### 2.1 Database & Multi-Tenancy Approach
- **Pattern:** Logical Isolation (Row-Level Security/Partitioning) within a shared database.
- **Implementation:** Every core entity table (Users, Agents, Pipelines, Files) MUST include a `tenant_id` foreign key referencing the `Workspaces` table.
- **Query Guardrails:** The backend ORM/Data access layer must automatically inject `WHERE tenant_id = ?` based on the authenticated user's active session context.

### 2.2 Authentication & RBAC (Role-Based Access Control)
- **Roles:**
  - `Super Admin` (System owner - manages the SaaS platform)
  - `Agency Admin` (Agency Operator - full access across all their client workspaces)
  - `Client Approver` (End-user - read/approve access to a single workspace)
  - `Client Read-Only` (End-user - view-only access to a single workspace)
- **Token Claims:** JWTs must encode the user's role and their authorized `tenant_ids`.

## 3. Backend Implementation Tasks (API)

- [ ] **Task 1: Database Migration - Workspaces**
  - Create `workspaces` table (`id`, `name`, `created_at`, `settings_json`).
  - Update existing foundational tables (users, etc.) to include `tenant_id`.
- [ ] **Task 2: Auth Layer & RBAC Middleware**
  - Implement JWT validation middleware.
  - Implement role-checking middleware to block unauthorized endpoints.
  - Implement tenant-context middleware to parse `X-Tenant-ID` from headers and validate the user has access.
- [ ] **Task 3: Workspace CRUD API**
  - `POST /api/v1/workspaces` (Create new client workspace).
  - `GET /api/v1/workspaces` (List workspaces user has access to).
- [ ] **Task 4: User Invitation API**
  - `POST /api/v1/workspaces/:id/invites` (Send email invite with role).

## 4. Frontend Implementation Tasks (UI)

- [ ] **Task 5: Global Context Provider**
  - Implement React/Vue Context (or Redux/Zustand store) to manage `activeWorkspaceId`.
  - Ensure all outbound API requests attach `X-Tenant-ID: activeWorkspaceId`.
- [ ] **Task 6: Context Switcher Component**
  - Build the dropdown in the main navigation.
  - On change, update the global context and force a refetch of dashboard data.
- [ ] **Task 7: Workspace Management UI (Admin)**
  - Build the form to create a new client workspace.
  - Build the settings page to manage users/invites for that workspace.
- [ ] **Task 8: Client Portal View**
  - Implement the restricted dashboard layout for `Client Approver` roles (hiding agency settings, billing, etc.).

## 5. Security & Validation Loop
- All API endpoints must be audited to ensure no endpoint allows IDOR (Insecure Direct Object Reference) across tenants.
- Validation script required to test that a Client token cannot access Agency Admin routes.