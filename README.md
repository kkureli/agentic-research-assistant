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

Sprint 0 — Project Foundation