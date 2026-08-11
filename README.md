# Agentic Research Assistant

A production-oriented Agentic RAG system for researching, analyzing, and comparing information across multiple documents.

The project is built incrementally, starting from a baseline semantic RAG pipeline and evolving toward an agentic research system with advanced retrieval, tool orchestration, verification, and evaluation.

## Goals

- Multi-document research and comparison
- Hybrid dense + sparse retrieval with Qdrant
- Query rewriting and decomposition
- Metadata-aware retrieval
- Multi-query retrieval
- LLM-based reranking
- Grounded answer generation with source citations
- Agentic tool orchestration
- Multi-step research
- Answer verification
- Retrieval and answer evaluation

---

## Current Architecture

```text
User Question
      ↓
FastAPI
      ↓
Advanced RAG Pipeline
      ↓
Query Rewriting
      ↓
Query Decomposition
      ↓
Metadata Extraction & Entity Resolution
      ↓
Per-Query Metadata Filtering
      ↓
┌─────────────────────┐
│   Hybrid Retrieval  │
│                     │
│ Dense      Sparse   │
│ Semantic   Lexical  │
└─────────┬───────────┘
          ↓
      RRF Fusion
          ↓
Multi-Query Result Merge
          ↓
    Deduplication
          ↓
    LLM Reranking
          ↓
 Context Construction
          ↓
Grounded LLM Generation
          ↓
Final Answer + Sources
```

### Retrieval Strategy

The retrieval layer combines two complementary search strategies:

- **Dense retrieval** captures semantic similarity between queries and document chunks.
- **Sparse retrieval** captures lexical similarity and exact-term matches.

Hybrid retrieval combines both signals using **Reciprocal Rank Fusion (RRF)**.

This improves retrieval for queries containing exact terms such as product names, dates, identifiers, financial metrics, and domain-specific terminology while preserving semantic search capabilities.

---

## Planned Agentic Architecture

```text
Client
  ↓
FastAPI
  ↓
Agent Orchestrator
  ↓
Planner Agent
  ↓
Research Agent
  ↓
Tools
├── Knowledge Base Search
├── Web Search
└── Calculator
  ↓
Verifier Agent
  ↓
Final Answer + Sources
```

Future iterations will allow the system to dynamically decide which retrieval strategies and tools are required for a given research question.

---

# Current Status

## Sprint 0 — Project Foundation ✅

- FastAPI application setup
- Environment configuration
- Logging
- Docker setup
- Qdrant setup
- Synthetic research dataset
- Initial evaluation dataset

---

## Sprint 1 — Document Ingestion & Semantic Retrieval ✅

- Markdown document loading
- YAML front matter parsing
- Metadata preservation
- Recursive character chunking
- OpenAI batch embeddings
- Qdrant vector collection
- Deterministic point IDs
- Document ingestion pipeline
- Cosine similarity search
- Top-K semantic retrieval

### Baseline Retrieval Findings

The baseline dense retriever performed well for focused single-entity questions.

However, multi-entity comparison queries could retrieve incomplete context because a single query embedding could favor one entity over another.

For example, a question comparing growth slowdowns at two companies could retrieve strong evidence for one company while failing to retrieve sufficient evidence for the other.

These findings motivated the advanced retrieval work implemented in Sprint 3.

---

## Sprint 2 — Baseline RAG & Grounded Answer Generation ✅

- OpenAI LLM integration
- Context construction from retrieved evidence
- Grounded system prompt
- End-to-end RAG pipeline
- Source-aware citations
- Multi-evidence answers
- No-answer behavior when evidence is insufficient
- Baseline RAG validation

### Baseline RAG Findings

The baseline system performed well on focused single-entity and multi-source questions.

A known limitation remained for multi-entity comparison queries: single-query dense retrieval could retrieve evidence for only one entity.

Importantly, the generation layer correctly refused to fabricate missing evidence when the retrieved context was insufficient.

This established a useful separation between:

- **Retrieval quality**
- **Generation quality**

The retrieval limitation became the primary focus of Sprint 3.

---

## Sprint 3 — Advanced Retrieval ✅

Sprint 3 upgraded the baseline semantic retriever into a multi-stage retrieval pipeline designed for more complex research questions.

### Query Understanding

- Query rewriting
- Query decomposition
- Structured metadata extraction
- Entity resolution
- Company alias normalization

### Retrieval

- Dense semantic retrieval
- Sparse lexical retrieval
- Hybrid dense + sparse search
- Reciprocal Rank Fusion (RRF)
- Metadata-aware filtering
- Per-subquery filtering
- Multi-query retrieval

### Post-Retrieval Processing

- Multi-query result merging
- Deterministic chunk IDs
- Document deduplication
- LLM-based reranking
- Top-K evidence selection

### Pipeline Integration

- Advanced retrieval orchestration
- Context construction from reranked evidence
- Grounded answer generation
- Source-aware citations
- Baseline vs advanced retrieval validation

---

## Sprint 3 — Key Improvement

The baseline retrieval pipeline failed on some multi-entity comparison queries because a single dense query could retrieve evidence for only one entity.

For example:

```text
Compare the main causes of growth slowdown at Asteria and Nova.
```

The baseline retriever could return primarily Asteria evidence, leaving the generation model without sufficient information about Nova.

The advanced retrieval pipeline now:

```text
Original Question
      ↓
Query Rewrite
      ↓
Query Decomposition
      ↓
Subqueries
      ↓
Metadata Extraction
      ↓
Per-Subquery Filtering
      ↓
Hybrid Dense + Sparse Retrieval
      ↓
RRF Fusion
      ↓
Merge Results
      ↓
Deduplicate
      ↓
Rerank Against Original Question
      ↓
Best Evidence
```

The comparison query can therefore be decomposed into independently retrievable questions such as:

```text
What are the main causes of growth slowdown at Asteria?

What are the main causes of growth slowdown at Nova?
```

Each subquery receives its own metadata filters and hybrid retrieval operation.

The resulting evidence is merged, deduplicated, and reranked against the original comparison question.

### Result

The previously failing comparison query now retrieves evidence for both companies and produces a grounded comparative answer with citations.

This demonstrates a measurable improvement over the baseline retrieval architecture.

---

# Retrieval Pipeline

The current retrieval pipeline can be summarized as:

```text
Question
   ↓
Rewrite
   ↓
Decompose
   ↓
Extract Metadata
   ↓
Resolve Entities
   ↓
For Each Subquery
   │
   ├── Apply Metadata Filters
   │
   ├── Dense Retrieval
   │
   ├── Sparse Retrieval
   │
   └── RRF Fusion
   ↓
Merge Candidates
   ↓
Deduplicate
   ↓
LLM Rerank
   ↓
Top Evidence
```

### Dense Retrieval

Dense embeddings represent the semantic meaning of document chunks and queries.

This allows semantically related expressions to match even when they do not share the same exact words.

```text
"revenue growth slowed"

≈

"growth decelerated"
```

### Sparse Retrieval

Sparse retrieval provides lexical matching for important exact terms.

It is particularly useful for:

- Product names
- Company names
- Dates and reporting periods
- Financial terminology
- Identifiers
- Domain-specific terminology

### Hybrid Retrieval

Dense and sparse searches run independently against the same document chunks.

```text
                 Query
                   │
          ┌────────┴────────┐
          ↓                 ↓
    Dense Search      Sparse Search
          ↓                 ↓
    Semantic Rank      Lexical Rank
          └────────┬────────┘
                   ↓
               RRF Fusion
                   ↓
             Unified Ranking
```

RRF combines ranking positions rather than directly comparing dense and sparse similarity scores.

---

# Document Representation

Each document is divided into chunks during ingestion.

Every chunk contains:

```text
Document Chunk
├── Text
├── Metadata
│   ├── source
│   ├── chunk_id
│   ├── chunk_index
│   ├── company
│   ├── company_id
│   ├── year
│   ├── quarter
│   └── document_type
│
├── Dense Vector
└── Sparse Vector
```

The same chunk therefore supports both semantic and lexical retrieval without duplicating the underlying document.

---

# Next Steps

## Sprint 4 — Agentic Research Workflow

Planned work:

- Agent orchestrator
- Research planning
- Tool selection
- Knowledge base search tool
- Multi-step research execution
- Research state management
- Dynamic retrieval strategy selection
- Conditional research loops

## Sprint 5 — Evaluation & Observability

Planned work:

- Retrieval evaluation
- Answer evaluation
- Golden datasets
- MRR
- NDCG
- Recall@K
- LLM-as-a-Judge
- Retrieval regression testing
- Failure analysis
- Latency tracking
- Token usage tracking
- Cost tracking
- Tracing and observability

## Sprint 6 — API & Productionization

Planned work:

- Production FastAPI endpoints
- Request/response schemas
- Error handling
- Structured logging
- Configuration management
- Dockerized deployment
- Health checks
- Production-ready service boundaries

## Sprint 7 — Final Polish

Planned work:

- Automated tests
- Architecture documentation
- Architecture diagram
- Example research queries
- README refinement
- Demo workflow
- Repository cleanup
- Deployment documentation

---

# Backlog

Potential future improvements that are intentionally outside the current core roadmap:

- Cross-encoder reranking
- Semantic chunking
- Query expansion
- HyDE retrieval
- Parent-child retrieval
- Contextual compression
- Embedding and retrieval caching
- Streaming responses
- Document upload and incremental ingestion
- Background ingestion jobs
- Local LLM support
- Model/provider fallback
- Multi-language retrieval
- Tenant-level authorization filtering
- Prompt injection defenses
- Human-in-the-loop workflows
- User feedback loops
- Load testing
- Kubernetes deployment