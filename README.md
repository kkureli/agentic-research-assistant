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
User
 ↓
Research Agent
 ↓
Tool Registry
 ├── Knowledge Base Search
 │      ↓
 │   Advanced Retrieval
 │   ├── Query Rewrite
 │   ├── Query Decomposition
 │   ├── Entity Resolution
 │   ├── Metadata Filtering
 │   ├── Dense Retrieval
 │   ├── Sparse Retrieval
 │   ├── RRF Fusion
 │   ├── Deduplication
 │   └── LLM Reranking
 │
 ├── Web Search
 └── Calculator
 ↓
Tool Evidence
 ↓
Research Agent
 ↓
Final Answer + Citations
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

This improves multi-entity questions such as:

```text
Compare the main causes of growth slowdown at Asteria and Nova.
```

Instead of relying on one embedding, the system decomposes the question, retrieves evidence for each entity, merges the results, and reranks them against the original query.

### Agentic Tool Orchestration

The Research Agent currently has three tools:

- `search_knowledge_base`
- `search_web`
- `calculate`

The model decides which tools are required. The application executes the Python functions and returns the results to the model.

Exact duplicate tool calls are blocked, while retries with different arguments remain allowed.

### Grounding and Citations

Internal evidence uses `[S*]` citations and web evidence uses `[W*]` citations.

The agent is instructed to:

- Ground factual claims in tool evidence
- Place citations close to supported claims
- Avoid invented citation IDs
- Avoid unsupported generalizations
- Clearly state when evidence is insufficient

## Evaluation & Observability

Sprint 5 introduced an automated evaluation framework covering:

- Tool routing
- Retrieval quality
- Answer correctness
- Insufficient evidence handling
- Faithfulness / groundedness
- Citation validation
- Agent trajectory efficiency
- Runtime observability

Retrieval metrics include Recall, Precision, Reciprocal Rank, MRR, and nDCG.

Trajectory evaluation checks exact duplicate tool calls, excessive tool usage, and maximum agent step depth.

Minimal observability currently tracks:

- Agent latency
- Tool-call count
- Agent LLM-call count

The evaluation suite uses a golden dataset containing internal retrieval, comparison, calculation, web research, and insufficient-evidence cases.

## Sprint Status

- Sprint 0 — Project Foundation ✅
- Sprint 1 — Document Ingestion & Semantic Retrieval ✅
- Sprint 2 — Baseline RAG & Grounded Generation ✅
- Sprint 3 — Advanced Retrieval ✅
- Sprint 4 — Agentic Research Workflow ✅
- Sprint 5 — Evaluation & Observability ✅
- Sprint 6 — Multi-Agent / Source Critic 🔜
- Sprint 7 — Production API & Integrations
- Sprint 8 — Enterprise Hardening & Governance

## Next: Multi-Agent / Source Critic

The next phase introduces a second specialized agent that evaluates evidence quality before the final answer is accepted.

```text
User
 ↓
Research Agent
 ↓
Evidence
 ↓
Source Critic Agent
 ↓
Evidence sufficient?
 ├── Yes → Final Answer
 └── No  → Feedback → Follow-up Research
```

The Source Critic will focus on evidence sufficiency, unsupported claims, conflicting evidence, missing evidence, and follow-up research requests.

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
