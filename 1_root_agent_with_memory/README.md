# 1. Root Agent with Memory (Google ADK)

This project demonstrates how to build and run a foundational agent using the **Google Agent Development Kit (ADK)** with **Google Search tool grounding** and **conversational memory** across multi-turn interactions.

---

## Directory Overview

```
1_root_agent_with_memory/
├── agents/
│   └── root_agent/
│       ├── .env                # Environment configuration (API keys / Project IDs)
│       ├── agent.py            # ADK Agent definition with Google Search tool
│       └── main.py             # FastAPI server with ADK session management
├── frontend/                   # Optional Node.js/Express web chat interface
│   ├── public/                 # Static chat UI assets
│   ├── server.js               # Proxy server for FastAPI backend
│   └── package.json
├── tests/
│   └── root_agent/
│       └── test.py             # Integration tests for single-turn and multi-turn flows
├── utils/
│   ├── logging.py              # Colored and structured logging configuration
│   └── utils.py                # Environment variable helper utilities
└── requirements.txt            # Python dependencies
```

---

## Core Components

### 1. Root Agent with Google Search (`agents/root_agent/agent.py`)

The agent is defined using `google.adk.agents.llm_agent.Agent` and equipped with real-time web search capabilities:

* **Model**: Powered by `gemini-2.5-flash`.
* **Tools**: Integrated with `google.adk.tools.google_search` to fetch up-to-date facts and web results.
* **Role & Instructions**: Acts as a helpful assistant that answers user queries and automatically triggers Google Search when factual or recent information is required.

```python
from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge, use google search whenever you need to find recent information or facts.',
    tools=[google_search]
)
```

---

### 2. Multi-Turn Session & Memory Design (`agents/root_agent/main.py`)

`main.py` wraps the ADK agent inside a **FastAPI** application to provide a REST API while maintaining conversational state across multiple turns.

#### How Memory & Sessions are Designed:

1. **Shared Session Service (`InMemorySessionService`)**:
   - An instance of `InMemorySessionService` is created at the application level.
   - It stores the conversation state, message history, and context in memory keyed by `(app_name, user_id, session_id)`.

2. **Session Lifecycle (`setup_session_and_runner`)**:
   - **New Session**: When a request arrives without a `session_id` (`session_id=None`), the service creates a new session using `await service.create_session(app_name=root_agent.name, user_id=user_id)` and generates a unique `session_id`.
   - **Existing Session (Multi-turn)**: When a request includes an existing `session_id`, the function reuses that session, allowing the agent to access previous turns and maintain conversational context.
   - An ADK `Runner` is instantiated with the `root_agent`, `app_name`, and the shared `session_service`.

3. **Execution & Event Processing (`execute_agent_run`)**:
   - Executes `runner.run_async` with the target `session_id` and the user query encapsulated in `types.Content(parts=[types.Part(text=query)], role="user")`.
   - Iterates through the streaming response events, aggregating the generated text chunks into a final response.
   - Returns both the active `session_id` and the `final_response`.

4. **FastAPI Endpoint (`POST /run-root-agent`)**:
   - Accepts `query` (string) and optional `session_id` (string).
   - Returns a structured JSON payload:
     ```json
     {
       "status": "success",
       "results": {
         "session_id": "<session-uuid>",
         "response": "<agent-response-text>"
       }
     }
     ```
   - Callers can save the returned `session_id` and supply it in subsequent requests to maintain the conversation context.

---

### 3. Integration Testing (`tests/root_agent/test.py`)

`test.py` validates the backend API using FastAPI's `TestClient`, covering both stateless single-turn interactions and stateful multi-turn memory:

1. **Health Check (`GET /`)**:
   - Verifies that the API service is up and running.

2. **Single-Turn Queries**:
   - Executes independent queries (e.g., *"What is the capital of France?"*, *"Who wrote Hamlet?"*) without passing a `session_id`.
   - Verifies successful execution and response structure.

3. **Multi-Turn Queries (Memory & Context Persistence)**:
   - **Turn 1**: Sends a piece of information to remember (*"Remember this: my secret code name is Antigravity."*) without a `session_id`. The test captures the newly generated `session_id`.
   - **Turn 2**: Sends a follow-up query (*"What did I say my secret code name was?"*) passing the `session_id` from Turn 1.
   - **Assertion**: Asserts that the agent recalls the secret code name (`"antigravity"`) from the previous turn, confirming that conversational memory is functioning correctly.

---

## Getting Started

### 1. Prerequisites & Environment Setup

1. Make sure you have Python 3.10+ installed.
2. Install project dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables in `agents/root_agent/.env` (e.g. `GEMINI_API_KEY` or Vertex AI configuration).

---

### 2. Running the Tests

To run the integration test suite verifying health, single-turn, and multi-turn memory:

```bash
python3 tests/root_agent/test.py
```

---

### 3. Running the FastAPI Server

To start the agent API server directly:

```bash
python3 -m agents.root_agent.main
```
Or with Uvicorn:
```bash
uvicorn agents.root_agent.main:api --host 127.0.0.1 --port 8000 --reload
```

The API will be available at `http://127.0.0.1:8000`. You can explore the interactive OpenAPI documentation at `http://127.0.0.1:8000/docs`.

---

### 4. Running the Optional Web Chat UI (Frontend)

An optional modern Node.js/Express web chat interface is included in the `frontend` folder:

```bash
cd frontend
npm install
npm start
```

Open `http://localhost:3000` in your browser to chat with the agent in an interactive UI.
