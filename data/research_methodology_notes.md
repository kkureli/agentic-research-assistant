---
company: internal
document_type: methodology
period: 2026
date: 2026-08-04
sector: research
---

# Research Methodology Notes

## Purpose
This dataset is synthetic and is designed for evaluating retrieval, multi-document comparison, metadata filtering, query rewriting, reranking, agent planning, and citation verification.

## Recommended Metadata Filters
Queries may be filtered by:
- company
- document_type
- period
- date
- sector

## Example Multi-Step Questions
- Compare Asteria's Q1 and Q2 revenue growth and explain the main drivers of the change.
- Which Asteria risks persisted across FY2025, Q1 2026, and Q2 2026?
- How did Nova's revenue guidance change from Q1 to Q2?
- Compare Asteria and Nova: which company improved gross margin in Q2 and why?
- Which company appears more exposed to customer expansion risk versus hardware deployment risk?

## Evaluation Guidance
A strong system should:
1. Retrieve the correct company and period.
2. Avoid mixing facts between Asteria and Nova.
3. Distinguish reported facts from analyst interpretation.
4. Cite the source document supporting each major claim.
5. Recognize when industry reports provide context rather than company-specific facts.
