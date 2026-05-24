# Multi-Agent Git Workflow Rules

This document outlines the standard Git workflow for all autonomous agents operating within the AgencyOS project.

## 1. Core Principles

- **No Direct Commits to Main:** Agents are strictly prohibited from pushing directly to `main` or `develop` branches.
- **Atomic Commits:** Each commit must accomplish a single, logical change and be independently verifiable.
- **Conventional Commits:** All commit messages must follow the Conventional Commits specification (`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`).
- **Agent Identity:** Agents must configure their Git identity before making commits.

## 2. Agent Git Identity

To ensure traceability, agents must set their Git config at the repository level (`--local`) before committing.
Example:
```bash
git config user.name "AgencyOS - Frontend Agent"
git config user.email "frontend-agent@agencyos.local"
```

## 3. Branching Strategy

We use a modified Trunk-Based development approach designed for agentic concurrency.

### Naming Convention
Branches created by agents must follow this format:
`agent/{agent-slug}/{task-or-feature}`

Examples:
- `agent/ux-architect/redesign-dashboard`
- `agent/senior-developer/api-auth-fix`

### Workflow Steps

1. **Checkout & Update:** 
   Always start by fetching and branching from the latest `main` or the designated epic branch.
   ```bash
   git fetch origin
   git checkout -b agent/my-slug/my-task origin/main
   ```

2. **Develop & Commit:** 
   Make incremental, atomic commits using the configured agent identity.

3. **Rebase Before PR:** 
   Before requesting a review, fetch the latest `main` and rebase to resolve potential conflicts locally.
   ```bash
   git fetch origin
   git rebase origin/main
   ```

4. **Push:**
   Push the branch to the remote repository.
   ```bash
   git push -u origin agent/my-slug/my-task
   ```

## 4. Conflict Resolution & Merging

- If an agent encounters a merge conflict during a rebase that it cannot confidently resolve programmatically, it must pause and hand over the task to the **Git Workflow Master** agent (`git-workflow-master`).
- Merging to `main` is handled exclusively via Pull Requests. 
- A designated Reviewer Agent (or Human) will review the PR, verify CI/CD checks, and perform a squash-merge.

## 5. Handoffs

When a task requires multiple specialists sequentially (e.g., UX Architect -> Senior Developer -> Evidence Collector), agents should pass the branch name in their handoff payload. The subsequent agent will check out the existing branch instead of creating a new one.