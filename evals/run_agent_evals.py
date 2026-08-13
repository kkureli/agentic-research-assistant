"""
Agent evaluation runner.

This script evaluates the research agent across several dimensions:

- Tool Routing:
  Checks whether the agent selected the required tools
  and avoided forbidden tools.

- Retrieval Quality:
  Checks whether the expected knowledge-base sources were retrieved.
  Metrics include Recall, Precision, Reciprocal Rank, MRR, and nDCG.

- Answer Correctness:
  Compares the agent's final answer with the expected facts using
  an LLM judge and calculates a correctness score.

- Insufficient Evidence Handling:
  Checks whether the agent correctly states that information is unavailable
  when the evidence is insufficient, instead of guessing or inventing facts.

- Faithfulness / Groundedness:
  Checks whether factual claims in the final answer are supported by
  the evidence returned by the tools and identifies unsupported claims.

- Citation Evaluation:
  Checks whether required citation types are present and whether citations
  used in the final answer actually exist in the tool evidence.

- Agent Trajectory:
  Checks for exact duplicate tool calls, excessive tool usage,
  and unnecessarily long tool-use paths.

- Observability:
  Tracks agent runtime latency, LLM calls, and tool calls.

Each evaluation case produces a PASS / FAIL / N/A result, and the script
prints both case-level results and aggregate summary metrics.
"""

import time

from app.agents.research_agent import run_research_agent
from app.schemas.evaluation import EvaluationResult, ObservabilityMetrics
from evals.answer import evaluate_answer
from evals.citation import evaluate_citations
from evals.faithfulness import evaluate_faithfulness
from evals.insufficient_evidence import evaluate_insufficient_evidence
from evals.loader import load_evaluation_cases
from evals.reporting import print_case_result, print_evaluation_summary
from evals.retrieval import evaluate_retrieval
from evals.tool_routing import evaluate_tool_routing
from evals.trajectory import evaluate_trajectory


def run_agent_evaluations() -> list[EvaluationResult]:
    cases = load_evaluation_cases()

    results: list[EvaluationResult] = []

    for case in cases:
        print(f"\nRunning: {case.id}")
        print(f"Question: {case.question}")

        start_time = time.perf_counter()
        agent_result = run_research_agent(case.question)
        latency_seconds = time.perf_counter() - start_time

        observability = ObservabilityMetrics(
            latency_seconds=latency_seconds,
            tool_call_count=len(agent_result.traces),
            llm_call_count=agent_result.llm_call_count,
        )

        tool_routing = evaluate_tool_routing(
            case=case,
            agent_result=agent_result,
        )

        retrieval = evaluate_retrieval(
            case=case,
            agent_result=agent_result,
        )

        answer_evaluation = evaluate_answer(
            case=case,
            agent_result=agent_result,
        )

        insufficient_evidence = evaluate_insufficient_evidence(
            case=case,
            agent_result=agent_result,
        )

        faithfulness = evaluate_faithfulness(
            agent_result=agent_result,
        )

        citation_evaluation = evaluate_citations(
            case=case,
            agent_result=agent_result,
        )

        trajectory_evaluation = evaluate_trajectory(
            agent_result=agent_result,
        )

        result = EvaluationResult(
            case_id=case.id,
            question=case.question,
            answer=agent_result.answer,
            tool_routing=tool_routing,
            retrieval=retrieval,
            answer_evaluation=answer_evaluation,
            insufficient_evidence_evaluation=insufficient_evidence,
            faithfulness=faithfulness,
            citation_evaluation=citation_evaluation,
            trajectory_evaluation=trajectory_evaluation,
            observability=observability,
        )

        results.append(result)

        print_case_result(result)

    print_evaluation_summary(results)

    return results


if __name__ == "__main__":
    run_agent_evaluations()
