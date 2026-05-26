# Project Tracking & Dependencies

This document tracks the execution status across all phases of the AgencyOS lifecycle and maps critical dependencies to ensure proper sequencing of work.

## Team Assembly
The following core team is actively assembled for the current operations (Phase 3 Rebuild & Orchestration):
* **Agents Orchestrator:** Manages the Dev↔QA Loop
* **Backend Architect:** Leads orchestration resilience, database changes, and custom agent storage endpoints
* **DevOps Automator:** Handles CI/CD, Docker Compose fallback, and S3 infrastructure provisioning
* **Evidence Collector:** Leads the QA gates, transactional tests, and isolation validation
* **Product Manager:** Manages project roadmap and dependency tracking

---

## 1. High-Level Phase Tracking

- [x] **Phase 0: Intelligence & Discovery**
  - Opportunity validated, requirements scoped.
- [x] **Phase 1: Strategy & Architecture**
  - Architecture approved, sprint backlog created.
- [x] **Phase 2: Foundation & Scaffolding**
  - Infrastructure deployed, CI/CD operational.
- [~] **Phase 3: Build & Iterate (Current Phase)**
  - *Note: We are actively executing the Phase 3 Rebuild Epic focused on DAG orchestration and Custom Agent storage.*
- [ ] **Phase 4: Quality & Hardening**
  - Dependency: Requires 100% completion of Phase 3 features and Dev↔QA sign-offs.
- [ ] **Phase 5: Launch & Growth**
  - Dependency: Requires Reality Checker "READY" verdict from Phase 4.
- [ ] **Phase 6: Operate & Evolve**
  - Dependency: Requires stable production deployment and active growth channels from Phase 5.

---

## 2. Phase 3 Rebuild: Task Tracking & Dependencies

### Epic A: Orchestration Hardening & Resilience
| Status | Task ID | Description | Agent | Dependencies |
|:---:|---|---|---|---|
| [ ] | A1-1 | DB migration for `workflow_executions` table | Backend Architect | Phase 2 DB Foundation |
| [ ] | A1-2 | Implement workflow state saving in `central_runner.py` | Backend Architect | A1-1 |
| [ ] | A2-1 | Replace mock `execute_node` with actual logic | Backend Architect | A1-2 |
| [x] | A3-1 | Implement retry mechanism with exponential backoff | Backend Architect | A2-1 |
| [x] | A3-2 | Handle disconnected graphs & crashes | Backend Architect | A3-1 |
| [ ] | A4-1 | Pydantic models for DAG inputs/outputs | Backend Architect | A1-1 |
| [ ] | A4-2 | Strict schema validation between nodes | Backend Architect | A4-1 |
| [ ] | QA-A | Integration and resilience test scenarios | Evidence Collector | A1-2, A2-1, A3-2, A4-2 |

### Epic B: Custom Agent Storage & Lifecycle Management
| Status | Task ID | Description | Agent | Dependencies |
|:---:|---|---|---|---|
| [ ] | B4-1 | Refactor markdown generation into `agent_config_service.py` | Backend Architect | None |
| [ ] | B1-1 | Storage Abstraction Layer (S3 & Local Fallback) | Backend Architect | D1-1 |
| [ ] | B1-2 | Strict tenant isolation in storage paths | Backend Architect | B1-1 |
| [ ] | B2-1 | `PUT /api/custom-agents/{agent_id}` endpoint | Backend Architect | B4-1, B1-2 |
| [ ] | B2-2 | `DELETE /api/custom-agents/{agent_id}` endpoint | Backend Architect | B1-2 |
| [ ] | B3-1 | DB transactional rollbacks on storage failure | Backend Architect | B2-1, B2-2 |
| [ ] | QA-B | Transactional and isolation test scenarios | Evidence Collector | B3-1 |

### DevOps & Infrastructure
| Status | Task ID | Description | Agent | Dependencies |
|:---:|---|---|---|---|
| [ ] | D1-1 | Provision S3 bucket and IAM Roles/Policies | DevOps Engineer | Phase 2 AWS Setup |
| [ ] | D1-2 | Update Kubernetes configs with env vars | DevOps Engineer | D1-1 |
| [ ] | D1-3 | Update `docker-compose.yml` for local testing | DevOps Engineer | D1-1 |
| [ ] | D1-4 | Configure CI/CD pipeline for `s3` integration tests | DevOps Engineer | D1-3, QA-A, QA-B |

---

## 3. Workflow Dependencies (The Dev↔QA Loop)
Every task in Phase 3 is subject to the following dependency cycle before being marked complete:
1. **Implementation** (Dev Agent) -> Blocks QA
2. **Automated Testing** (Dev Agent) -> Blocks Handoff
3. **QA Validation** (Evidence Collector) -> Blocks Merge
4. **Sign-off & Merge** (Orchestrator) -> Unblocks dependent tasks