# Retrieval evaluation metrics:
#
# Recall:
# Measures how many of the expected relevant sources were successfully retrieved.
# High recall means the retriever is not missing important evidence.
#
# Precision:
# Measures how many of the retrieved sources are actually relevant.
# High precision means the retriever is not returning too much unnecessary evidence.
#
# Reciprocal Rank:
# Measures how high the first relevant source appears in the retrieved ranking.
# A relevant source at rank 1 gives 1.0, rank 2 gives 0.5, rank 3 gives 0.333, etc.
#
# nDCG:
# Measures the overall ranking quality of all relevant sources.
# It rewards relevant sources appearing near the top and penalizes them appearing lower.
#
# Retrieval PASS / FAIL:
# Checks whether all required relevant sources were retrieved.
#
# Retrieval N/A:
# Used when the evaluation case does not define relevant knowledge-base sources,
# so retrieval quality should not be scored for that case.

import re

from app.schemas.agent import AgentResult
from app.schemas.evaluation import (
    EvaluationCase,
    RetrievalEvaluation,
)
from evals.calculate_ndcg import calculate_ndcg


def extract_retrieved_sources(
    agent_result: AgentResult,
) -> list[str]:
    sources: list[str] = []

    for trace in agent_result.traces:
        if trace.tool_name != "search_knowledge_base":
            continue

        matches = re.findall(
            r"^Source:\s*(.+)$",
            trace.result,
            flags=re.MULTILINE,
        )

        sources.extend(match.strip() for match in matches)

    return list(dict.fromkeys(sources))


def evaluate_retrieval(
    case: EvaluationCase,
    agent_result: AgentResult,
) -> RetrievalEvaluation:
    retrieved_sources = extract_retrieved_sources(agent_result)

    if not case.relevant_sources:
        return RetrievalEvaluation(
            relevant_sources=[],
            retrieved_sources=retrieved_sources,
            missing_sources=[],
            applicable=False,
            passed=None,
            recall=None,
            precision=None,
            reciprocal_rank=None,
            ndcg=None,
        )

    relevant_set = set(case.relevant_sources)
    retrieved_set = set(retrieved_sources)

    found_relevant_sources = relevant_set & retrieved_set

    missing_sources = list(relevant_set - retrieved_set)

    recall = len(found_relevant_sources) / len(relevant_set)

    precision = (
        len(found_relevant_sources) / len(retrieved_set) if retrieved_set else 0.0
    )

    reciprocal_rank = 0.0

    for rank, source in enumerate(retrieved_sources, start=1):
        if source in relevant_set:
            reciprocal_rank = 1 / rank
            break

    return RetrievalEvaluation(
        relevant_sources=case.relevant_sources,
        retrieved_sources=retrieved_sources,
        missing_sources=missing_sources,
        applicable=True,
        passed=not missing_sources,
        recall=recall,
        precision=precision,
        reciprocal_rank=reciprocal_rank,
        ndcg=calculate_ndcg(relevant_set, retrieved_sources),
    )
