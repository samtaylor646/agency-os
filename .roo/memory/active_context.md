# Active Context

## Current Objective
Epic: Custom Agent Remediation - Phase 2 complete.
- Validated and human-approved Data Adapter & Strict Schema Enforcement.
- Fixed 401 Unauthorized errors during custom agent creation by configuring Vite's API proxy fallback to `http://localhost:8000`.
- Verified strict backend schema rejection of flat payloads (returns 422).
- Proved atomic transaction rollback mechanism in `server/routers/custom_agents.py`.

## Next Steps
- Epic is fully complete and ready for final review or closure.

## Active Epic
Custom Agent Remediation

## State
- Phase 1 (Security Hotfixes) complete.
- Phase 2 (Data Integrity & Schema Mapping) complete and QA verified.
- Phase 3 (Maintainability & Policy) complete. Updated Vite and Docker configs to use `VITE_API_URL` instead of hardcoded ports, and drafted the Data Governance Policy for GDPR compliance.
