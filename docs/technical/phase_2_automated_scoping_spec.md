# Technical Specification: Phase 2 - Automated Scoping & Document Generation

## 1. Overview
This specification outlines the architecture and implementation details for Phase 2: Automated Scoping & Document Generation in AgencyOS. The goal is to generate formal project documents (PRDs, Engineering Specs, Task Lists) directly from chat context and manage document ingestion (parsing PDF and Markdown files).

## 2. Core Components

### 2.1 Document Ingestion Engine
- **Purpose:** Allow users to upload external context (PDFs, Markdown files) into the chat scope.
- **Parsing Strategy:**
  - **PDF:** Use PyMuPDF or pdfplumber to extract text and structure.
  - **Markdown:** Native parsing, extracting frontmatter and headings.
- **Data Flow:** Upload -> Parse -> Chunk (if necessary) -> Store in Vector DB or direct context attachment.

### 2.2 Document Generators
- **Purpose:** Transform chat context and parsed inputs into structured outputs.
- **Generators:**
  - `PRDGenerator`: Outputs Markdown PRDs.
  - `EngineeringSpecGenerator`: Outputs Technical Specifications.
  - `TaskListGenerator`: Outputs JSON/Markdown actionable tasks.
- **Mechanism:** Prompt chains leveraging the existing LLM runner, passing accumulated conversation history + parsed document contents.

### 2.3 Split-Screen Viewer UI
- **Purpose:** Allow users to view generated documents side-by-side with the chat interface.
- **Component:** A resizable split-pane layout in `ChatScopeInterface.jsx`.
- **Features:** Render markdown, copy to clipboard, save to `docs/` or download.

## 3. Data Models (Backend)
- Add `Document` model (id, chat_id, title, content, type, created_at)
- Endpoints:
  - `POST /api/chat/{id}/documents/upload`
  - `POST /api/chat/{id}/generate/{doc_type}`

## 4. Next Steps for Implementation
1. **Backend Architect:** Implement upload/parsing endpoints and document generation services.
2. **Frontend Developer:** Implement upload UI, generation triggers, and the Split-Screen Document Viewer.
