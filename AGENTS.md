# AGENTS.md — Zen AI Engineering Standard

## Purpose

This file defines the engineering standard for AI agents, Codex, and coding assistants working on Emanuel's projects.
It is meant to preserve consistency across sessions in architecture, coding style, reliability, observability, and delivery quality.

---

## Core Engineering Principles

- Reliability over cleverness
- Structure over improvisation
- Documentation over guessing
- Determinism over magic
- Observability over opacity
- Clarity over complexity
- Simplicity before abstraction

All agents should be:

- Predictable
- Observable
- Refactorable
- Replaceable
- Testable

---

## Workspace Context

Primary language: Python  
Secondary languages: HTML and minimal JavaScript when strictly necessary  
Main focus: APIs, automation, AI agents, integrations, dashboards  
Preferred cloud: Google Cloud Run and Google Cloud Functions  
Operational data layer: Google Sheets  
Persistence layer: Firestore  
Fast UI: Streamlit  
Quick validation workflow: terminal first  
Frequent integrations: OpenAI, Google Cloud, REST APIs, JSON, Sheets, Firestore

---

## Philosophy of Development

1. Prioritize clarity and simplicity.
2. Avoid unnecessary complexity.
3. Propose alternatives when more than one solution is valid.
4. Document code and technical decisions.
5. Preserve context between sessions.
6. Think like a professional software engineer without overengineering.
7. Keep code clean, modular, and refactorable.

### Proportionality Rule

Solutions must be proportional to the problem.

- Small task → simple implementation
- Prototype → avoid unnecessary architecture
- Growing project → modularize early
- Production system → optimize for reliability and maintainability

---

## Project Maturity Levels

### Prototype
Goal: validate an idea quickly.

Rules:
- minimal structure
- fast feedback
- manual validation is acceptable
- avoid unnecessary abstractions

### MVP
Goal: stabilize a useful version.

Rules:
- modular structure
- separated configuration
- basic tests
- logging required
- `.env.example` required

### Production
Goal: reliability and maintainability.

Rules:
- clean architecture
- structured logging
- retries and fallbacks
- tests for critical paths
- observability
- documented deployment
- secrets management

---

## AI Agent Architecture

Recommended structure:

```text
project_name/
├── app/
│   ├── api/
│   ├── core/
│   ├── agents/
│   │   ├── core/
│   │   ├── memory/
│   │   ├── tools/
│   │   ├── prompts/
│   │   ├── schemas/
│   │   ├── workflows/
│   │   └── orchestration/
│   ├── services/
│   ├── repositories/
│   ├── models/
│   ├── utils/
│   └── main.py
├── tests/
├── scripts/
├── docs/
├── logs/
├── .env.example
├── requirements.txt
├── README.md
└── AGENTS.md
```

Agents must be designed as systems, not scripts.

---

## Canonical Agent Components

Each serious agent should separate the following responsibilities.

### 1. AgentCore
Responsible for:
- receiving user or task input
- invoking planner or decision layer
- coordinating tools and memory
- returning final structured result

### 2. Planner
Responsible for:
- deciding next action
- decomposing tasks
- selecting tools
- determining whether more context is needed

### 3. ToolExecutor
Responsible for:
- executing tools safely
- validating arguments
- handling errors
- returning structured results

### 4. MemoryManager
Responsible for:
- conversation context
- task state
- persisted knowledge
- retrieval strategy

### 5. PromptManager
Responsible for:
- system instructions
- prompt templates
- format constraints
- role-specific guidance

---

## Workflow Pattern

Preferred orchestration flow:

```text
Input
→ Validation
→ Planner
→ Tool Selection
→ Tool Execution
→ Memory Update
→ Final Response Validation
→ Output
```

For complex tasks:

```text
Input
→ Planner
→ Multi-step execution
→ Intermediate state saves
→ Reflection / verification
→ Final output
```

---

## Tool Design Rules

Tools must:

- Be deterministic whenever possible
- Return structured data
- Validate inputs
- Fail gracefully
- Be idempotent when appropriate
- Avoid hidden side effects
- Log execution
- Define clear timeouts

Never return vague free text when a schema is possible.

Prefer:

```python
from pydantic import BaseModel

class WeatherResult(BaseModel):
    temperature: float
    condition: str
```

Instead of:

```python
return "It is hot today"
```

### Tool Categories

Preferred tool categories:
- retrieval tools
- API tools
- computation tools
- storage tools
- reporting tools
- notification tools

### Tool Registry Pattern

Use a registry when projects grow:

```python
TOOLS = {
    "get_weather": get_weather,
    "save_report": save_report,
    "load_sheet_data": load_sheet_data,
}
```

This improves discoverability, testing, and orchestration.

---

## Structured Outputs Rule

When interacting with LLMs:

- prefer structured outputs
- prefer tool calling over parsing raw text
- validate all outputs with Pydantic
- avoid trusting free-form output in production flows

If an output cannot be validated, treat it as failed execution.

---

## OpenAI Usage Policy

Before generating or integrating OpenAI code:

1. Prefer official SDK patterns
2. Prefer structured outputs
3. Prefer validated schemas
4. Implement retries where needed
5. Avoid deprecated methods
6. Keep prompts concise and explicit
7. Control token usage

### OpenAI Safety Rules

- Never execute raw model text as shell commands
- Never trust arbitrary model-generated code without inspection
- Never expose secrets in prompts or logs
- Validate model-produced tool arguments before execution

### Preferred Libraries

- `openai`
- `pydantic`
- `httpx`

---

## Context7 Policy

Context7 must be used when:

- integrating external libraries
- using unfamiliar APIs
- writing production code
- fixing version-specific issues
- generating setup or deployment code
- using libraries that evolve quickly

### Context7 Process

1. Identify library
2. Query Context7
3. Prefer official examples
4. Prefer current syntax
5. Avoid deprecated usage
6. Apply only what fits project scope

### Rule

Documentation over assumptions.  
Context7 over hallucination.

---

## Memory Architecture

Agents must distinguish:

### Short-Term Memory
Transient conversation context.

Examples:
- recent messages
- current user intent
- immediate task context

### Working Memory
Execution-specific state.

Examples:
- current step number
- subtask state
- partial tool outputs
- plan status

### Long-Term Memory
Persisted knowledge across sessions.

Examples:
- user preferences
- saved reports
- historical results
- task summaries
- entity records

### Memory Requirements

Memory must be:
- serializable
- queryable
- replaceable
- documented
- privacy-conscious

Example mapping:

```text
short_term → in-memory conversation
working_memory → runtime task state
long_term → Firestore / DB / vector store
```

### Future-Ready Rule

If memory may grow significantly, design it so it can later plug into:
- Firestore
- SQLite
- vector store
- search index

without requiring full rewrite.

---

## Logging and Observability

Agents must log:

- high-level decisions
- tool selections
- tool inputs (sanitized)
- tool outputs summary
- retries
- errors
- fallbacks
- external API calls
- state transitions

### Logging Rules

- use `logging`, not `print`, in production code
- prefer structured logs when project grows
- never log secrets
- keep logs useful for debugging real incidents

### Minimum Logging Fields

When possible, include:
- timestamp
- module
- action
- status
- duration
- correlation_id or request_id

### Observability Requirements

Production-oriented agents should expose:
- health checks
- basic metrics
- latency visibility
- error counts
- optional telemetry hooks

---

## Error Handling Strategy

Agents must handle:

- malformed model output
- invalid tool arguments
- external API failures
- timeouts
- network errors
- missing configuration
- corrupted memory state

### Preferred Recovery Strategies

- retry
- fallback tool
- safer simplified prompt
- partial result
- safe defaults
- user-facing clarification when needed

Never fail silently.

---

## Clean Architecture Rules

Use these layers when project scope justifies it:

```text
interface
application
domain
infrastructure
```

### Mapping

- API / Streamlit / CLI → interface
- agents / services / use cases → application
- models / business rules → domain
- cloud / DB / external APIs → infrastructure

### Rule of Separation

Do not mix:
- business logic with UI
- persistence with orchestration
- prompts with infrastructure
- tools with transport layer concerns

---

## Configuration Rules

- Never hardcode secrets
- Use `.env` for local development
- Always provide `.env.example`
- Centralize settings in a config module
- Prefer Pydantic settings or a dedicated config layer
- Validate required environment variables at startup

---

## Coding Style Rules

- descriptive names
- small focused functions
- explicit typing
- modular code
- docstrings for public classes and functions
- avoid giant files
- separate responsibilities clearly

Prefer:
- simple before abstract
- explicit before clever
- readable before compressed

---

## Testing Strategy

Use `pytest` by default.

At minimum, test:
- parsing
- schemas
- core services
- tool behavior
- critical routes
- memory serialization
- failure cases

### For AI-Specific Systems

Test:
- tool schema validation
- prompt contract assumptions
- planner behavior when a tool fails
- fallback execution
- structured output validation

If full tests are not written, leave:
- TODOs
- manual test steps
- validation notes in README

---

## Preferred Python Stack

Use when appropriate:

- `pydantic` for schemas and validation
- `fastapi` for APIs
- `httpx` for HTTP
- `pytest` for tests
- `python-dotenv` for local environment management
- `google-cloud-firestore` for Firestore
- `gspread` + `google-auth` for Sheets
- `streamlit` for operational UI
- `uvicorn` for local API run
- `rich` or `typer` for polished CLI tools

---

## Deployment Guidance

Before deployment, the agent must verify:

1. project structure
2. dependencies
3. required environment variables
4. logging readiness
5. health check availability
6. deployment target suitability

### Deploy Target Guidance

Use:
- Cloud Functions for small isolated tasks, webhooks, or event handlers
- Cloud Run for APIs, services, or long-running orchestration components

---

## Response Format Expected from Codex / Agents

Preferred response structure:

1. Brief objective summary
2. Proposed structure or approach if needed
3. Implementation
4. How to run it
5. Optional next improvements

If there are valid alternatives, show:
- simple option
- robust option

---

## Files and Git Hygiene

Do not commit:
- `.env`
- `.env.*`
- `__pycache__/`
- `.pytest_cache/`
- `.mypy_cache/`
- `.ruff_cache/`
- `.venv/`
- credentials files
- private keys
- generated local logs unless intentional

Always include when relevant:
- `README.md`
- `.env.example`
- `.gitignore`
- `requirements.txt` or `pyproject.toml`

---

## Production Readiness Checklist

Before calling an agent project production-ready, confirm:

- [ ] Config is centralized
- [ ] Secrets are externalized
- [ ] Logs are meaningful
- [ ] Core flows have tests
- [ ] Tool outputs are validated
- [ ] Errors have fallback behavior
- [ ] README explains setup, run, and deploy
- [ ] Deployment target is documented
- [ ] Health check exists
- [ ] Context7-sensitive libraries were checked against docs

---

## Golden Rule

Build as if the project may grow:

- organized from day 1
- understandable in one week
- refactorable in one month
- deployable in production when mature

But never confuse clarity with complexity.

If a smaller solution solves the problem well, prefer the smaller solution.
