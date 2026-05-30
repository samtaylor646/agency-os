# Engineering Specification: Build vs. Run Sandbox Environment

## 1. Executive Summary
As part of the isolated Twin.so research and analysis project, this document specifies the technical architecture for a "Build vs. Run" Sandbox Environment. This environment enables developers and users to iteratively draft, test, and debug agent prompts in a secure, isolated, and highly cost-effective manner before promoting them to live production execution.

## 2. Architectural Paradigm

The architecture enforces a strict boundary between two execution contexts:

### 2.1. Build Environment (The Sandbox)
*   **Purpose:** Rapid iteration, prompt engineering, logic validation, and debugging.
*   **State:** Ephemeral. Memory and contextual states are localized to the active session and wiped upon exit unless explicitly saved as test cases.
*   **Access:** Zero-trust network access. External API calls are intercepted and routed to a mocking engine.
*   **Compute:** Lightweight, shared execution threads.

### 2.2. Run Environment (Production)
*   **Purpose:** Live execution, real-world data processing, and user-facing operations.
*   **State:** Persistent. Interacts directly with the primary transactional database and long-term vector storage.
*   **Access:** Full external API access using decrypted user/organization credentials.
*   **Compute:** Dedicated, prioritized worker queues.

## 3. Cost-Saving Mechanisms

To dramatically reduce the financial overhead of prompt engineering, the following mechanisms are enforced at the API Gateway layer:

### 3.1. Automatic Model Routing (Degradation)
When an agent is executed within the `Build` context, the LLM routing proxy intercepts the request. Unless specifically overridden for a high-fidelity test, requests for premium models are automatically downgraded:
*   `gpt-4o` → `gpt-3.5-turbo` or `gpt-4o-mini`
*   `claude-3-opus` → `claude-3-haiku`
*   `gemini-1.5-pro` → `gemini-1.5-flash`

### 3.2. Semantic Caching
The Sandbox environment employs an aggressive semantic caching layer. Repeated iterations of similar prompts (e.g., fixing a typo in the system prompt) will serve cached responses for unmodified sections of the conversation tree, minimizing token usage.

### 3.3. Hard Token Caps
All sandbox completions are injected with strict `max_tokens` limits. Furthermore, infinite-loop detection is tightened, terminating agent execution after a maximum of 3 cyclic reasoning steps.

## 4. Backend Isolation Strategy

Preventing sandbox leakage into production data is paramount.

### 4.1. Data and Secret Isolation
*   **Credential Masking:** The secrets manager will completely block the retrieval of production API keys if the execution context flag is set to `BUILD`.
*   **Mock Storage:** Database write operations (e.g., `save_document`, `update_memory`) are redirected to an in-memory SQLite instance or a temporary Redis namespace tied exclusively to the sandbox session ID.

### 4.2. Compute Isolation
To prevent malicious code execution during agent tool testing, Sandbox Python/Node execution environments are spun up inside ephemeral, network-isolated Firecracker microVMs or strictly bounded Docker containers without external network interfaces.

## 5. Transition: Promotion to Run
A clear "Promote to Production" pipeline must be established. Once a user is satisfied with the agent's performance in the Sandbox, the system creates an immutable snapshot of the agent's prompts, tool configurations, and settings. This snapshot is tagged with a version number and deployed to the `Run` environment, at which point the model routing reverts to the requested premium models.