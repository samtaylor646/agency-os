# Phase 0 Discovery: Legal Dependency Audit Report

I have completed a review of the primary dependencies listed in your frontend and backend configuration files. The purpose of this audit was to identify any restrictive copyleft licenses (such as GPL or AGPL) that could impose "viral" open-source requirements, thereby complicating your ability to take the project private or monetize it as a proprietary product.

### 1. Frontend Dependencies (`client/package.json`)
All frontend dependencies utilize highly permissive licenses that are fully compatible with proprietary and commercial software:
*   **MIT License:** `react`, `react-dom`, `tailwindcss`, `postcss`, `autoprefixer`, `vite`, `@vitejs/plugin-react`
*   **ISC License:** `lucide-react`

**Frontend Risk Assessment:** **Low / Safe.** There are no restrictive copyleft obligations here.

### 2. Backend Dependencies (`server/requirements.txt`)
The Python backend dependencies also consist primarily of permissive licenses (MIT, Apache 2.0, and BSD). 
*   **MIT License:** `fastapi`, `pydantic`, `langchain`, `sqlalchemy`, `alembic`, `python-jose`, `python-docx`, `redis`, `openai`, `anthropic`, `mcp`, `pyyaml`
*   **Apache License 2.0:** `bcrypt`, `python-multipart`, `tenacity`, `boto3`
*   **BSD 3-Clause:** `uvicorn`, `passlib`, `PyPDF2`
*   **Unlicense:** `email-validator`
*   **PostgreSQL License:** `pgvector`
*   **LGPL (with exception):** `psycopg2-binary`

*Note on `psycopg2-binary`:* While `psycopg2` is licensed under the LGPL (which is copyleft), it includes an explicit linking exception that allows it to be used in proprietary applications without requiring you to open-source your own codebase. Furthermore, for a SaaS or backend application not distributed directly to end users, the LGPL does not require source disclosure (unlike the AGPL).

**Backend Risk Assessment:** **Low / Safe.** 

### Conclusion & Recommendation
**No highly restrictive copyleft licenses (such as GPL or AGPL) were found in your top-level dependencies.** 

From a legal and compliance perspective regarding the primary dependencies reviewed, there are no immediate open-source license blockers to taking this project private or monetizing it as a proprietary product. 

*Recommendation:* As you move closer to launch or a formal distribution, I recommend implementing an automated dependency scanning tool (such as Snyk or FOSSA) into your CI/CD pipeline to catch any restrictive transitive dependencies that might be pulled in indirectly.