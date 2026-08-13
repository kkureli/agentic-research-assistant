# Agentic Research Assistant

A production-oriented Agentic RAG system for researching internal documents and public web sources using advanced retrieval, tool-calling agents, grounded generation, citations, and automated evaluation.

## What It Does

The system can:

- Search an internal knowledge base
- Search the public web
- Perform deterministic calculations
- Rewrite and decompose complex queries
- Apply metadata-aware hybrid retrieval
- Rerank and deduplicate evidence
- Decide which tools to use dynamically
- Handle insufficient evidence safely
- Produce source-aware citations
- Evaluate retrieval, answers, citations, tool usage, and agent trajectories
- Track basic runtime observability

## Architecture

```text
Client
 ↓
FastAPI
 ├── API key auth
 ├── rate limiting
 ├── request ID
 └── validation
 ↓
Research Service
 ↓
Runtime governance
 ├── timeout/limits
 └── tool policy
 ↓
Research Agent
 ↔ Source Critic
 ↓
Tools
 ├── Qdrant
 ├── Tavily
 └── Calculator
 ↓
Tracing / Logs / Audit Metadata
 ↓
Structured Response
```

The agent runs in a bounded multi-step loop. Tool results are returned to the model as evidence, and the model decides whether to answer, call another tool, or safely decline when evidence is insufficient.

## Core Capabilities

### Advanced Retrieval

The internal retrieval pipeline includes:

- Query rewriting
- Query decomposition
- Multi-query retrieval
- Entity resolution
- Metadata filtering
- Dense semantic retrieval
- Sparse BM25 retrieval
- Hybrid search with Reciprocal Rank Fusion
- Deduplication
- LLM-based reranking

### Agentic Tool Orchestration

The Research Agent currently has three tools:

- `search_knowledge_base`
- `search_web`
- `calculate`

Exact duplicate tool calls are blocked. Unknown tools and invalid arguments are rejected. Tool call count is bounded by configuration.

### Grounding and Citations

Internal evidence uses `[S*]` citations and web evidence uses `[W*]` citations.

## Evaluation & Observability

The evaluation framework covers:

- Tool routing
- Retrieval quality
- Answer correctness
- Insufficient evidence handling
- Faithfulness / groundedness
- Citation validation
- Agent trajectory efficiency
- Runtime observability
- Source Critic evaluation

Retrieval metrics include Recall, Precision, Reciprocal Rank, MRR, and nDCG.

## Production

### Required environment variables

Copy `.env.example` and set:

- `OPENAI_API_KEY`
- `TAVILY_API_KEY`
- `API_KEY` (required in production)
- `QDRANT_URL` (default `http://localhost:6333`)

Useful optional variables:

- `APP_ENV=development|test|production`
- `LOG_LEVEL`
- `RATE_LIMIT_PER_MINUTE`
- `MAX_AGENT_STEPS`
- `MAX_CRITIC_ROUNDS`
- `RESEARCH_TIMEOUT_SECONDS`
- `MAX_QUESTION_LENGTH`
- `MAX_TOOL_CALLS_PER_REQUEST`
- `CORS_ORIGINS`
- `OPENAI_TIMEOUT_SECONDS` / `OPENAI_MAX_RETRIES`
- `TAVILY_TIMEOUT_SECONDS`
- `QDRANT_TIMEOUT_SECONDS`

### Authentication

`POST /api/v1/research` requires header `X-API-Key`.

- missing or invalid key → `401`
- valid key → request continues

`GET /health` and `GET /ready` are unauthenticated.

### Rate limiting

Research is limited in-process by `RATE_LIMIT_PER_MINUTE` (default 10/minute). Exceeding the limit returns `429` with the standard error shape:

```json
{"code": "rate_limit_exceeded", "message": "Rate limit exceeded. Try again later."}
```

This limiter is local to a single process. Multi-instance deployments would need shared state such as Redis. Redis is not used in this project.

### Endpoints

- Liveness: `GET /health`
- Readiness: `GET /ready`
- Research: `POST /api/v1/research`
- OpenAPI / Swagger: `http://localhost:8000/docs` (disabled when `APP_ENV=production`)

Example:

```bash
curl -X POST http://localhost:8000/api/v1/research \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"question": "What was Asteria Cloud Systems'\'' revenue growth in Q2 2026?"}'
```

### Local run

```bash
docker compose up -d qdrant
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker

```bash
docker compose up --build
```

The API image runs as a non-root user, does not copy `.env` into the image, and includes a `/health` healthcheck. Uvicorn shuts down on SIGTERM with a graceful timeout.

### Tracing

The project keeps internal request/agent/critic traces and structured audit logs (`request_id`, latency, tool names, LLM counts, critic outcome, citation IDs). An external tracing platform was not added, to avoid extra vendor setup and accidental prompt/document export.

### Request timeout limitation

The API timeout stops waiting for a response. It does not forcibly cancel the worker thread. Work is still bounded by OpenAI/Tavily/Qdrant timeouts, max agent steps, max critic rounds, and max tool calls.

## Sprint Status

- Sprint 0 — Project Foundation ✅
- Sprint 1 — Document Ingestion & Semantic Retrieval ✅
- Sprint 2 — Baseline RAG & Grounded Generation ✅
- Sprint 3 — Advanced Retrieval ✅
- Sprint 4 — Agentic Research Workflow ✅
- Sprint 5 — Evaluation & Observability ✅
- Sprint 6 — Multi-Agent / Source Critic ✅
- Sprint 7 — Production API & Integrations ✅
- Sprint 8 — Enterprise Hardening & Governance ✅

## Technology Stack

- Python
- FastAPI
- OpenAI
- Qdrant
- Docker
- Tavily
- Pydantic
- Dense embeddings
- Sparse BM25 retrieval
- Reciprocal Rank Fusion
- LLM reranking

## Project Goal

The project is designed to evolve beyond basic:

```text
embed → retrieve → prompt → answer
```

toward a research system that can decide what information it needs, where to search, whether the evidence is sufficient, whether another tool call is required, and whether it can safely answer.

The goal is a research workflow that is measurable, traceable, grounded, and production-oriented.
