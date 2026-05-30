# AgencyOS Structural and Workflow Recommendations

Based on the findings in `build_workflow_analysis.md`, the following recommendations outline concrete improvements for the project setup, structure, and build pipelines.

## 1. CI/CD Pipeline Alignment

**Implement Full-Stack Testing in CI:**
*   Add Node.js setup and `npm run test` execution to `ci-tests.yml` to ensure client-side changes do not break the application.
*   Incorporate End-to-End testing (e.g., Playwright) running against a temporary staging build within the GitHub Action.

**Optimize Build Speeds:**
*   Implement dependency caching for `pip` and `npm` in `ci-tests.yml`.
*   Introduce Docker layer caching (`cache-from` and `cache-to`) in `deploy.yml` to avoid redundant builds on every commit.

**Secure and Resilient Pipelines:**
*   Remove direct dependencies on real API keys in standard PR tests to support fork contributions. Implement VCR.py or custom mock agents for LLM integration testing.
*   Complete the `deploy.yml` pipeline by adding semantic versioning or SHA tagging, and connect it to a real deployment endpoint (e.g., AWS ECS, Kubernetes).

## 2. Structural & Rule Improvements

**Consolidate Rules:**
*   Merge duplicate mandates between `config/settings.md` and `.clinerules`. Ideally, `.clinerules` should act as the AI context boundary, while `config/settings.md` should be the human-readable operational source of truth.

**Protect Core Documentation:**
*   Update `.github/workflows/doc-integrity-check.yml` to explicitly include `docs/core/` in its protection regex. Currently, it only checks `qa`, `technical`, and `operations`.

**Enhance Local Developer Experience (DX):**
*   Update `docker-compose.yml` to utilize a `.env` file rather than hardcoded dummy values (e.g., `SECRET_KEY`).
*   Implement `pre-commit` hooks (or Husky for Node) to run `scripts/validate_agent_metadata.py` and `scripts/validation_layer.py` locally before a developer pushes code, reducing CI failure cycles.

## 3. Agent Ecosystem Governance

**Agent Validation Workflow:**
*   Require any modifications to the `/agents` directories to run through a specific validation pipeline in GitHub Actions, ensuring that the `agent_base.yaml` constraints and metadata properties are intact.
*   Enforce that newly discovered workflows and runbooks are automatically templated into `agents/teams/` or `agents/strategy/runbooks/` as part of the Phase Gate handoff process.
