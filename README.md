# Agentic Research Assistant

A production-oriented Agentic RAG system for researching and comparing information across multiple documents.

## Goals

- Multi-document RAG
- Semantic retrieval with Qdrant
- Query rewriting and reranking
- Source citations
- Agentic tool orchestration
- Multi-step research
- Answer verification
- Retrieval evaluation

## Architecture

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
RAG Pipeline
  ├── Query Rewrite
  ├── Embedding
  ├── Qdrant Retrieval
  └── Reranking
  ↓
Verifier Agent
  ↓
Final Answer + Sources

## Current Status

### Sprint 0 — Project Foundation ✅

- FastAPI application setup
- Environment configuration
- Logging
- Docker setup
- Qdrant setup
- Synthetic research dataset
- Initial evaluation dataset

### Sprint 1 — Document Ingestion & Semantic Retrieval ✅

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

The baseline dense retriever performs well for focused single-entity questions.

Multi-entity comparison queries can retrieve incomplete context because a single query embedding may favor one entity over another.

Future retrieval improvements will explore:

- Query decomposition
- Metadata filtering
- Reranking
- Multi-query retrieval

### Sprint 2 — Baseline RAG & Grounded Answer Generation ✅

- OpenAI LLM integration
- Context construction from retrieved evidence
- Grounded system prompt
- End-to-end RAG pipeline
- Source-aware citations
- Multi-evidence answers
- No-answer behavior when evidence is insufficient
- Baseline RAG validation

### Baseline RAG Findings

The baseline system performs well on focused single-entity and multi-source questions.

A known limitation remains for multi-entity comparison queries: single-query dense retrieval may retrieve evidence for only one entity. The generation layer correctly refuses to fabricate missing evidence.

This limitation will be addressed in Sprint 3 using query decomposition, metadata filtering, multi-query retrieval, and reranking.