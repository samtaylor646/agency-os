# Data Poisoning Prevention Strategies

This document outlines the strategies employed to prevent data poisoning and denial-of-wallet (DoW) attacks in our ingestion pipelines, particularly concerning embedding generation and LLM context usage.

## Threat Model
Data poisoning occurs when an attacker uploads maliciously crafted documents containing prompts or specific tokens designed to:
1. Skew semantic search results by packing keywords or adversarial text.
2. Exploit LLM vulnerabilities via prompt injection (e.g., overriding system prompts when the document is retrieved in a RAG pipeline).
3. Cause Denial-of-Wallet (DoW) by exhausting API rate limits or budget via excessively large inputs.

## Prevention Strategies

### 1. Data Sanitation & Normalization
Prior to embedding, all extracted text must pass through a strict sanitation layer (`server/services/document_parser.py:sanitize_text`).
- **Null Byte and Control Character Stripping:** Removes non-printable characters that might confuse the tokenizer or underlying embedding models.
- **Special Token Removal:** Strips recognized LLM control tokens (e.g., `<|endoftext|>`, `<|fim_prefix|>`) that attackers might use to prematurely terminate prompts or manipulate model context windows.
- **Whitespace Normalization:** Collapses excessive spaces and newlines to prevent token bloat and maintain chunking consistency.

### 2. Payload Size Limits & Rate Limiting
To prevent DoW attacks:
- **Max File Size Enforcement:** We enforce a strict payload limit (e.g., 5MB) at the API layer for document uploads.
- **Rate Limiting:** IP-based and user/tenant-based rate limiting on the ingestion endpoint (`POST /api/documents/ingest`) limits the number of ingestion requests per minute.

### 3. Role-Based Access Control (RBAC) Isolation
- All ingested documents are strictly bound to a `workspace_id`.
- The API explicitly verifies that the authenticated user has explicit read/write access to the `workspace_id` before allowing ingestion or retrieval. This prevents cross-tenant poisoning where an attacker attempts to inject malicious context into another workspace's vector space.
