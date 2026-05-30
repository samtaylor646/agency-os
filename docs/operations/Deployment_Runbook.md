# AgencyOS Deployment Runbook

## Overview
This runbook outlines the standard operating procedures for deploying AgencyOS updates to production and staging environments.

## Prerequisites
- Access to the deployment server (SSH/Kubernetes)
- Authorized credentials (AWS/Docker/DB)
- Approved pull request in `main` branch
- QA sign-off from the Evidence Collector agent

## Pre-Deployment Checklist
1. **Verify Environment Variables**: Ensure all secrets and environment variables are properly configured in `.env.production`. **Mandatory**: Perform an explicit verification of the `ENCRYPTION_KEY` to ensure it is valid and accessible.
2. **Database Backup**: Take a snapshot of the current production database.
3. **Review Release Notes**: Confirm `CHANGELOG.md` reflects all changes going into the release.
4. **Notify Stakeholders**: Announce the planned deployment in the relevant communication channels.
5. **Verify Redis Constraints**: Ensure Redis instances are correctly configured with appropriate sizing constraints (e.g., `maxmemory 256mb`) to prevent Out-Of-Memory (OOM) failures.

## Deployment Steps (Docker Compose)
*Note: Ensure you are referencing the correct path for the production compose file, e.g., `deployment/docker-compose.yml` vs root `docker-compose.yml`.*

1. **Pull Latest Changes**:
   ```bash
   git checkout main
   git pull origin main
   ```
2. **Build and Start Containers**:
   ```bash
   docker compose -f deployment/docker-compose.yml up -d --build
   ```
3. **Run Database Migrations**:
   ```bash
   docker compose -f deployment/docker-compose.yml exec server alembic upgrade head
   ```

## Post-Deployment Verification
- Check service health endpoints (e.g., `/health`).
- Verify logs for any immediate errors: `docker compose logs -f server client`.
- **Websocket Monitoring**: Perform verification of websocket event monitoring to ensure real-time connections and events are firing correctly without widespread disconnections.
- Perform a manual UI/UX spot check.

## Rollback Procedure
If critical issues are detected:
1. Revert to the previous stable git tag: `git checkout <previous-tag>`
2. Rebuild and restart: `docker compose -f deployment/docker-compose.yml up -d --build`
3. If necessary, restore the database from the pre-deployment snapshot.
4. Notify stakeholders of the rollback.
