# Engineering Specification: Epic 4 - Standardized API & Integrations

## 1. Overview
This specification details the technical implementation of Epic 4, focusing on the API Gateway, Webhook system, and the Secure Credential Vault for AgencyOS.

## 2. Architecture

### 2.1 API Gateway
- **Framework:** FastAPI (Python) running within the existing `server` container.
- **Authentication:** 
  - JWT for UI-based requests.
  - Long-lived API Keys for external system integrations. Keys hashed in DB (bcrypt/argon2).
- **Rate Limiting:** Redis-backed token bucket algorithm per tenant/API key.

### 2.2 Secure Credential Vault (LLM Keys)
- **Encryption Strategy:**
  - AES-256-GCM for encrypting keys at rest.
  - Data Encryption Key (DEK) unique per tenant.
  - Key Encryption Key (KEK) managed via AWS KMS or HashiCorp Vault (or a secure environment variable for MVP).
- **Database Schema (`credentials` table):**
  - `id` (UUID)
  - `tenant_id` (UUID, FK)
  - `provider` (Enum: 'openai', 'anthropic', etc.)
  - `encrypted_key` (Bytea)
  - `created_at` / `updated_at`

### 2.3 Webhook Infrastructure
- **Inbound Webhooks:**
  - Dedicated endpoint: `POST /api/v1/webhooks/{tenant_id}/{webhook_id}`
  - Signature verification support for known providers (e.g., verifying HubSpot HMAC).
  - Enqueue payloads to a message broker (RabbitMQ/Redis) for asynchronous processing by the NEXUS pipeline.
- **Outbound Webhooks:**
  - Agent runner triggers HTTP requests using `httpx` or `requests`.
  - Retry mechanism with exponential backoff (Celery/RQ) for failed deliveries.

## 3. Security Considerations
- Never log raw API keys or webhook payloads containing PII.
- All endpoints must enforce tenant isolation (validating API key -> tenant mapping).
- Strict validation of inbound JSON payloads using Pydantic schemas.

## 4. Rollout Plan
1. Implement and test Cryptography utility for the Vault.
2. Build CRUD API & UI for managing LLM credentials.
3. Expose core API endpoints and API Key generation.
4. Implement Inbound/Outbound Webhook engine.
