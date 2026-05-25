# API Architecture Options for AgencyOS Discovery Engine

To support the interactive Discovery Engine—where a user submits a prompt, agents think and ask clarifying questions, and artifacts are generated—we need a way for the Python backend to communicate with the React frontend. 

Here are the three main architectural options for this communication, along with their pros and cons.

---

## Option 1: REST API with Long-Polling
**How it works:** The frontend sends a request (e.g., `POST /init-discovery`). The backend starts processing but doesn't close the connection until it has a response (e.g., the agent finishes generating questions). If the connection times out, the frontend asks again (`GET /discovery-status`).

**Pros:**
- Simplest to implement initially.
- Uses standard HTTP verbs and requires no special libraries on the frontend or backend.
- Easy to load balance and scale (stateless).

**Cons:**
- **No real-time token streaming:** The user stares at a spinner until the entire block of text (questions or artifacts) is generated. This can feel very slow for LLM interactions.
- High overhead if standard short-polling (pinging every 1 second) is used instead of long-polling.

---

## Option 2: REST + Server-Sent Events (SSE) (Recommended)
**How it works:** The frontend uses standard REST for discrete actions (e.g., `POST /submit-prompt`). The backend immediately returns a `session_id`. The frontend then opens a unidirectional SSE connection (`GET /stream/{session_id}`) to listen for real-time updates. The backend streams tokens and status updates as they happen.

**Pros:**
- **Excellent for LLMs:** Built-in support for streaming text generation token-by-token (typewriter effect).
- Uses standard HTTP protocols (works seamlessly over HTTP/1.1 and HTTP/2).
- Native browser support via the `EventSource` API (no complex libraries needed).
- Keeps architecture clean: REST for *commands* (doing things), SSE for *queries/listening* (observing things).

**Cons:**
- Unidirectional only (server to client). The client must still make separate POST requests to send answers back to the server.
- Connection limits in HTTP/1.1 (browsers max out at ~6 open SSE connections per domain), though not an issue for MVP.

---

## Option 3: Full WebSockets
**How it works:** The frontend and backend open a persistent, bi-directional connection. All communication (submitting prompts, streaming tokens, sending answers) happens over this single connection using a custom event schema.

**Pros:**
- **Lowest latency:** Bi-directional real-time communication.
- Highly scalable for massive multiplayer or highly concurrent real-time apps.

**Cons:**
- **High Complexity:** You must manually manage connection state, drops, reconnections, and message acknowledgments.
- Requires specific WebSocket libraries on both ends (e.g., `socket.io` or `fastapi.websockets`).
- Stateful by nature, making deployment and load balancing slightly more complicated.
- Often overkill for LLM applications where the user sends a message and waits for a stream of text.

---

### Recommendation for MVP
**Option 2 (REST + SSE)** is the industry standard for LLM applications like ChatGPT and Claude. It provides the UX benefits of real-time streaming without the complex state management overhead of WebSockets. 