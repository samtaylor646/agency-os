# User Journey Flows: Epic 1 (Multi-Tenant Workspace)

## Overview
This document outlines the core user journeys for the foundation of AgencyOS: establishing secure, isolated client workspaces.

---

## Flow 1: Agency Admin Onboarding & Workspace Creation

**Persona:** Agency Operator (Admin)
**Goal:** Setup the agency account and create the first isolated client environment.

1. **Signup/Login:** Admin authenticates into the main AgencyOS dashboard.
2. **Empty State:** Dashboard recognizes no active workspaces and prompts "Create Your First Client Workspace."
3. **Workspace Configuration:**
   - Admin enters Client Name (e.g., "Acme Corp").
   - Admin configures initial settings (which agents are assigned to this workspace).
4. **Provisioning:**
   - Backend generates a unique `tenant_id`.
   - Backend creates isolated data partitions for Acme Corp.
5. **Success & Redirection:** Admin is redirected to the Acme Corp workspace dashboard. The global context switcher at the top now displays "Acme Corp".

---

## Flow 2: Client Invitation & Access

**Persona:** Agency Operator (Admin) & Agency Client (End-User)
**Goal:** Grant a client secure access to their specific workspace portal.

1. **Invitation Generation:**
   - Admin navigates to "Users & Access" within the Acme Corp workspace.
   - Admin enters the Client's email address and selects role ("Approver" or "Read-Only").
2. **Email Dispatch:** AgencyOS sends a branded invitation email to the Client.
3. **Client Authentication:**
   - Client clicks the link and completes account setup (password creation).
4. **Restricted Portal Access:**
   - Client logs in.
   - RBAC strictly enforces that the Client *only* sees the Acme Corp workspace.
   - Client views a simplified dashboard showing active agent pipelines and deliverables, with no access to system-level settings.

---

## Flow 3: Admin Context Switching

**Persona:** Agency Operator (Admin)
**Goal:** Manage multiple clients without logging out.

1. **Active Session:** Admin is currently viewing the "Acme Corp" dashboard.
2. **Trigger Switch:** Admin clicks the Workspace Dropdown in the top navigation bar.
3. **Selection:** Admin selects "Globex Corp" from their list of managed workspaces.
4. **State Update:**
   - Frontend updates the global `active_tenant_id` context.
   - All dashboard widgets, agent pipelines, and file views immediately refetch data filtered strictly to the "Globex Corp" `tenant_id`.