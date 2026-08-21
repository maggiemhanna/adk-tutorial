# Google Agent Development Kit (ADK) Enablement Tutorial

Welcome to the **Google Agent Development Kit (ADK) Enablement Tutorial**. This repository provides production-grade reference implementations and architectural design patterns for building intelligent, reliable, and scalable multi-agent systems using **Google ADK**, **Gemini 2.5 Flash**, and **FastAPI**.

Each module in this repository demonstrates a foundational or advanced agentic pattern, complete with runnable FastAPI services, standalone tool executions, integration test suites, and architectural documentation.

---

## 🗺️ Architectural Patterns Overview

| Chapter | Pattern / Architecture | Primary ADK Classes | Key Capabilities |
| :--- | :--- | :--- | :--- |
| [**1. Root Agent with Memory**] | **Conversational Memory & Grounding** | `Agent`, `InMemorySessionService`, `Runner` | Multi-turn state tracking, session ID continuity, Google Search grounding, interactive web chat UI. |
| [**2. Controlled Schemas**] | **Strict Input & Output Validation** | `Agent(output_schema=...)`, `BaseModel`, `Enum` | Pydantic input validation, session state injection, constrained JSON outputs, SLA triage logic. |
| [**3. Custom Function Calling**] | **Custom Python Tool Integrations** | `Agent(tools=[...])`, `requests` | Python functions as ADK tools, auto JSON-schema generation from docstrings, multi-tool chaining. |
| [**4. Hierarchical Agent**] | **Dynamic Orchestration & Delegation** | `Agent(sub_agents=[...])` | Central coordinator delegating to domain specialist subagents in-memory with context isolation. |
| [**5. Agent as a Tool**] | **Agent-Tool Wrapping & State Sharing** | `AgentTool`, `ToolContext` | Specialized agents wrapped as callable tools; explicit state passing via `tool_context.state`. |
| [**6. Sequential Agent**] | **Deterministic Pipeline Execution** | `SequentialAgent`, `output_schema` $\rightarrow$ `input_schema` | Linear multi-stage pipeline where upstream agent output schema strictly feeds downstream agent input. |
| [**7. Parallel Agent & Synthesis**] | **Fan-Out / Fan-In Workflow** | `ParallelAgent`, `SequentialAgent`, `output_key` | Concurrent subagent execution across multiple domains followed by unified synthesis. |
| [**8. Router Agent**] | **Intent Classification & Microservices** | `Agent(output_schema=...)`, `httpx.AsyncClient` | LLM intent routing via Literal schema dispatching to distributed FastAPI agent microservices. |
| [**9. Loop Agent**] | **Iterative Refinement (Critic-Refiner)** | `LoopAgent`, `ToolContext.actions.escalate` | Feedback loop (Planner $\rightarrow$ Critic $\rightarrow$ Refiner) with tool-based condition checking and early loop exit. |

---

## 📂 Repository Structure

```
ADK Tutorial/
├── 1_root_agent_with_memory/           # Chapter 1: Foundation agent, multi-turn memory & web UI
├── 2_controlled_schema_input_and_output/# Chapter 2: Pydantic schemas, Enums, and SLA triage
├── 3_custom_function_calling/          # Chapter 3: Custom Python functions as tools
├── 4_hierarchical_agent/               # Chapter 4: Multi-agent hierarchy with sub_agents
├── 5_agent_as_a_tool/                  # Chapter 5: Wrapping agents with AgentTool & ToolContext
├── 6_sequential_agent/                 # Chapter 6: SequentialAgent with schema binding
├── 7_parallel_agent/                   # Chapter 7: ParallelAgent concurrent fan-out & synthesis
├── 8_router_agent/                     # Chapter 8: Intent router & distributed microservices
├── 9_loop_agent/                       # Chapter 9: LoopAgent iterative refinement & exit tools
└── README.md                           # Master enablement guide
```

---

## 🛠️ Common Framework Standards Across All Chapters

Every module in this tutorial is built following clean production standards:

1. **FastAPI Web Service**: Every agent is exposed via standard REST endpoints (`POST /run-...-agent`) with interactive OpenAPI docs at `/docs`.
2. **Session Lifecycle Management**: Demonstrates `InMemorySessionService` from `google.adk.sessions` to manage conversations, user contexts, and shared intermediate state.
3. **Structured & Colored Logging**: Uses `utils/logging.py` (`coloredlogs`) for rich terminal visibility into iteration events, tool calls, and payload flows.
4. **Automated Integration Testing**: Every chapter includes a dedicated test script (`tests/.../test.py`) using FastAPI's `TestClient` to validate health, single-turn, multi-turn, or multi-agent execution.

---

## 🚀 Getting Started

### 1. Prerequisites

- **Python 3.10+** (Python 3.11+ recommended)
- **Google Gemini API Key** or Vertex AI credentials

### 2. Environment Setup

Clone the repository and set up a Python virtual environment:

```bash
cd "ADK Tutorial"
python3 -m venv .venv
source .venv/bin/activate
```

### 3. API Key Configuration

Create a `.env` file in the agent directory of the chapter you wish to run (e.g. `1_root_agent_with_memory/agents/root_agent/.env`):

```bash
GEMINI_API_KEY="your-gemini-api-key"
```

### 4. Running Any Chapter

Navigate to the chapter directory, install dependencies, and run tests or start the server:

```bash
# Example: Running Chapter 9 (Loop Agent)
cd 9_loop_agent
pip install -r requirements.txt

# Run integration tests
python3 tests/sequential_agent/test.py

# Start the FastAPI service
python3 -m agents.sequential_agent.main
```

---