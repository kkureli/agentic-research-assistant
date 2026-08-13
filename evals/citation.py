from app.schemas.agent import AgentResult
from app.schemas.evaluation import CitationEvaluation, EvaluationCase
from app.utils.citations import extract_citations


def evaluate_citations(
    case: EvaluationCase,
    agent_result: AgentResult,
) -> CitationEvaluation:
    found_citations = extract_citations(agent_result.answer)

    available_citations = extract_citations(
        "\n".join(trace.result for trace in agent_result.traces)
    )

    if not case.expected_citation_prefixes:
        return CitationEvaluation(
            applicable=False,
            found_citations=found_citations,
            available_citations=available_citations,
            passed=None,
        )

    available_set = set(available_citations)

    invalid_citations = [
        citation for citation in found_citations if citation not in available_set
    ]

    missing_prefixes = [
        prefix
        for prefix in case.expected_citation_prefixes
        if not any(citation.startswith(prefix) for citation in found_citations)
    ]

    return CitationEvaluation(
        applicable=True,
        found_citations=found_citations,
        available_citations=available_citations,
        invalid_citations=invalid_citations,
        missing_prefixes=missing_prefixes,
        passed=not invalid_citations and not missing_prefixes,
    )
