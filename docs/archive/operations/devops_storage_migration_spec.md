# DevOps Deployment Specification: Storage Migration (Phase 3)

## 1. Overview
This document outlines the deployment strategy, environment configuration, and infrastructure changes required to support the Phase 3 Rebuild of AgencyOS. It specifically addresses the transition from local file-based storage for Custom Agents to a resilient, multi-tenant DB-backed and S3-compatible cloud storage architecture.

## 2. Infrastructure Requirements

### 2.1 Database Updates
*   **PostgreSQL:** Ensure the PostgreSQL instance has sufficient capacity to handle the new `workflow_executions` table, which will store granular state and JSONB data (potentially large payloads).
*   **Migrations:** Database migrations must be run as an init-container or pre-deployment hook to create `workflow_executions` and update `custom_agents` before the application pods start.

### 2.2 S3-Compatible Storage
*   **Bucket Provisioning:** Create a dedicated S3 bucket (e.g., `agency-os-agent-storage-prod`) for storing generated markdown persona files.
*   **IAM Policies (AWS/Cloud):** Create restricted IAM roles/policies granting the backend application `s3:PutObject`, `s3:GetObject`, and `s3:DeleteObject` strictly scoped to this bucket. 
*   **Path Structure:** Ensure IAM policies allow operations on the `tenants/*` path prefix.

## 3. Environment Variables Configuration

The following environment variables must be injected into the backend application environment (Docker/Kubernetes).

| Variable Name | Description | Default / Example |
| :--- | :--- | :--- |
| `STORAGE_BACKEND` | Defines the storage strategy (`s3` or `local`). | `s3` (Prod) / `local` (Dev) |
| `S3_BUCKET_NAME` | The target S3 bucket for storing custom agents. | `agency-os-agent-storage-prod` |
| `AWS_REGION` | The region of the S3 bucket. | `us-east-1` |
| `AWS_ACCESS_KEY_ID` | (Optional if using K8s IRSA) IAM Access Key. | `AKIA...` |
| `AWS_SECRET_ACCESS_KEY` | (Optional if using K8s IRSA) IAM Secret. | `...` |
| `LOCAL_STORAGE_PATH` | Base path for local fallback storage. | `agents/custom/` |
| `DATABASE_URL` | PostgreSQL connection string. | `postgresql://user:pass@db:5432/agencyos` |

## 4. Docker Compose Implementation (Local/Testing)

For `docker-compose.yml`, the strategy involves configuring the fallback local environment and simulating the DB.

*   **Local Fallback Mount:** Ensure the `LOCAL_STORAGE_PATH` is mounted as a volume so that tenant-isolated local files persist across container restarts in dev.
    ```yaml
    volumes:
      - ./agents/custom:/app/agents/custom
    ```
*   **Environment Injection:** Pass `STORAGE_BACKEND=local` by default in the standard compose file, but provide a `.env.example` that demonstrates switching to `s3` with credentials for local S3 testing (e.g., MinIO).

## 5. Kubernetes (K8s) Implementation (Production)

### 5.1 Storage & State
*   Since `s3` is the primary storage backend, pods can remain entirely stateless regarding agent configurations.
*   No PersistentVolumeClaims (PVCs) are required for the `agents/custom/` directory in production, increasing horizontal scalability and reducing stateful set complexity.

### 5.2 Security & Secrets
*   **IAM Roles for Service Accounts (IRSA):** Preferred over static AWS Access Keys. Bind an IAM role with S3 permissions to the Kubernetes ServiceAccount running the backend pod.
*   **ConfigMaps/Secrets:** Store `S3_BUCKET_NAME` and `STORAGE_BACKEND` in a ConfigMap. Store database credentials in K8s Secrets.

### 5.3 Deployment Strategies
*   **Init Containers:** Use an init container to run `alembic upgrade head` (or equivalent migration command) to ensure the `workflow_executions` table is present before the app starts.
*   **Rolling Updates:** Since state checkpointing will now be persisted in the DB, rolling updates of the DAG orchestrator (`central_runner`) will be safer. Ensure graceful shutdown (`SIGTERM`) is configured so running DAG nodes can checkpoint their state before pod termination.

## 6. Pre-Flight Deployment Checklist

- [ ] S3 Bucket is provisioned with appropriate encryption and versioning (optional, based on audit needs).
- [ ] IAM Role/Policy is created and restricted to the specific S3 Bucket.
- [ ] K8s ServiceAccount is annotated with the IAM Role (if using IRSA).
- [ ] K8s Secrets/ConfigMaps are updated with the new S3 and DB connection env vars.
- [ ] Database migration scripts for `workflow_executions` are tested and included in the deployment pipeline.
- [ ] Docker Compose updated to handle volume mounts for `STORAGE_BACKEND=local`.
- [ ] CI/CD pipeline configured to run integration tests against both `local` and `s3` storage implementations.
- [ ] Staging deployment completed and verified using a test tenant and dummy custom agent creation.

## 7. Rollback Plan

If the storage migration fails in production:
1.  **Code Rollback:** Revert the container image to the pre-migration tag.
2.  **Storage:** Since the legacy approach used local disk (which in Kubernetes without PVCs means ephemeral pod storage), no "data migration" rollback from S3 to disk is explicitly required, as previous pods were writing locally. However, any agents created in S3 during the failed window will be lost unless manually ported.
3.  **Database:** Assess if a down-migration of the `workflow_executions` table is necessary (usually additive schema changes can remain harmlessly).