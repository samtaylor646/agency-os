# AgencyOS Deployment Runbook

## Overview
This runbook outlines the standard operating procedures for deploying AgencyOS updates to production and staging environments.

## Prerequisites
- Access to the deployment server (SSH/Kubernetes)
- Authorized credentials (AWS/Docker/DB)
- Approved pull request in `main` branch
- QA sign-off from the Evidence Collector agent

## Pre-Deployment Checklist
1. **Verify Environment Variables**: Ensure all secrets and environment variables are properly configured in `.env.production`.
2. **Database Backup**: Take a snapshot of the current production database.
3. **Review Release Notes**: Confirm `CHANGELOG.md` reflects all changes going into the release.
4. **Notify Stakeholders**: Announce the planned deployment in the relevant communication channels.

## Deployment Steps (Docker Compose)
1. **Pull Latest Changes**:
   ```bash
   git checkout main
   git pull origin main
   ```
2. **Build and Start Containers**:
   ```bash
   docker compose -f docker-compose.prod.yml up -d --build
   ```
3. **Run Database Migrations**:
   ```bash
   docker compose -f docker-compose.prod.yml exec server alembic upgrade head
   ```

## Post-Deployment Verification
- Check service health endpoints (e.g., `/health`).
- Verify logs for any immediate errors: `docker compose logs -f server client`.
- Perform a manual UI/UX spot check.

## Rollback Procedure
If critical issues are detected:
1. Revert to the previous stable git tag: `git checkout <previous-tag>`
2. Rebuild and restart: `docker compose -f docker-compose.prod.yml up -d --build`
3. If necessary, restore the database from the pre-deployment snapshot.
4. Notify stakeholders of the rollback.
