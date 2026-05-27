# GDPR Compliance & Data Retention Policies

## 1. Environment Data Segregation Policy

### Overview
To comply with GDPR principles of data minimization and storage limitation, AgencyOS enforces strict environment data segregation. Customer data must be isolated on a per-tenant basis, ensuring that data crossing tenant boundaries is strictly prohibited. 

### Core Tenets
- **Logical Segregation:** All database records must contain a `tenant_id`. Application queries MUST filter by `tenant_id` at the lowest possible layer (e.g., ORM or DB views).
- **Physical Segregation Requirements:** Where possible, blob storage and file uploads must be partitioned into tenant-specific buckets or directories. 
- **Environment Isolation:** Production, Staging, and Development environments must use separate databases and infrastructure. Production customer data MUST NOT be copied to Development or Staging environments without explicit, documented anonymization.
- **Fail-Fast Tenancy:** API requests lacking a valid, authorized `X-Tenant-ID` header must fail immediately with a `403 Forbidden` or `401 Unauthorized`. Fallbacks to hardcoded tenant IDs (e.g., `tenant '1'`) are strictly forbidden.

---

## 2. Log Retention & Purge Policy

### Overview
This policy outlines the storage limitation principles applied to application and system logs, ensuring compliance with GDPR Article 5(1)(e) which mandates that personal data be kept for no longer than is necessary.

### Retention Period (TTL)
- **Standard Application Logs:** All application logs, including validation errors and system events, are subject to a strict **30-day Time-To-Live (TTL)**. 
- **Audit Logs:** Security and audit logs related to user access and administrative actions may be retained up to **90 days** for incident investigation, after which they must be securely purged.
- **Data Deletion Mechanism:** An automated cron job or managed logging service configuration must enforce the 30-day TTL, permanently purging logs older than 30 days.

### Log Redaction & Masking
- No Personally Identifiable Information (PII) or secrets should be logged in plaintext. 
- All logs emitting request bodies, parameters, or errors must pass through the `redact_pii` utility.
- Masked Data Types include but are not limited to:
  - Emails, Phone Numbers, SSNs, and Credit Card numbers.
  - Passwords, API Keys (e.g., `sk-...`), Bearer Tokens, and other authorization secrets.

### Review and Enforcement
Violations of these policies (such as discovering plaintext PII in logs or non-segregated cross-tenant queries) must be treated as critical severity incidents and remediated within 24 hours. Regular audits of log storage and database constraints will be conducted quarterly.