from pydantic import BaseModel

from app.schemas.evaluation import EvaluationResult


class EvaluationSummaryMetrics(BaseModel):
    total: int

    tool_passed: int
    tool_failed: int
    tool_accuracy: float

    retrieval_total: int
    retrieval_passed: int
    retrieval_failed: int
    retrieval_accuracy: float
    average_recall: float
    average_precision: float
    mean_reciprocal_rank: float
    average_ndcg: float

    answer_total: int
    answer_passed: int
    answer_failed: int
    answer_accuracy: float
    average_correctness: float

    insufficient_total: int
    insufficient_passed: int
    insufficient_failed: int
    insufficient_accuracy: float

    faithfulness_total: int
    faithfulness_passed: int
    faithfulness_failed: int
    faithfulness_accuracy: float

    citation_total: int
    citation_passed: int
    citation_failed: int
    citation_accuracy: float

    trajectory_total: int
    trajectory_passed: int
    trajectory_failed: int
    trajectory_accuracy: float
    average_tool_calls: float
    average_max_step: float

    average_latency_seconds: float
    average_llm_calls: float


def calculate_summary_metrics(
    results: list[EvaluationResult],
) -> EvaluationSummaryMetrics:
    total = len(results)

    # -----------------------
    # Tool routing metrics
    # -----------------------

    tool_passed = sum(1 for result in results if result.tool_routing.passed)

    tool_failed = total - tool_passed

    tool_accuracy = tool_passed / total * 100 if total > 0 else 0.0

    # -----------------------
    # Retrieval metrics
    # -----------------------

    retrieval_results = [
        result.retrieval for result in results if result.retrieval.applicable
    ]

    retrieval_total = len(retrieval_results)

    retrieval_passed = sum(1 for retrieval in retrieval_results if retrieval.passed)

    retrieval_failed = retrieval_total - retrieval_passed

    retrieval_accuracy = (
        retrieval_passed / retrieval_total * 100 if retrieval_total > 0 else 0.0
    )

    average_recall = (
        sum(
            retrieval.recall
            for retrieval in retrieval_results
            if retrieval.recall is not None
        )
        / retrieval_total
        if retrieval_total > 0
        else 0.0
    )

    average_precision = (
        sum(
            retrieval.precision
            for retrieval in retrieval_results
            if retrieval.precision is not None
        )
        / retrieval_total
        if retrieval_total > 0
        else 0.0
    )

    mean_reciprocal_rank = (
        sum(
            retrieval.reciprocal_rank
            for retrieval in retrieval_results
            if retrieval.reciprocal_rank is not None
        )
        / retrieval_total
        if retrieval_total > 0
        else 0.0
    )

    average_ndcg = (
        sum(
            retrieval.ndcg
            for retrieval in retrieval_results
            if retrieval.ndcg is not None
        )
        / retrieval_total
        if retrieval_total > 0
        else 0.0
    )

    # -----------------------
    # Answer evaluation metrics
    # -----------------------

    answer_results = [
        result.answer_evaluation
        for result in results
        if result.answer_evaluation.applicable
    ]

    answer_total = len(answer_results)

    answer_passed = sum(1 for answer in answer_results if answer.passed)

    answer_failed = answer_total - answer_passed

    answer_accuracy = answer_passed / answer_total * 100 if answer_total > 0 else 0.0

    average_correctness = (
        sum(
            answer.correctness_score
            for answer in answer_results
            if answer.correctness_score is not None
        )
        / answer_total
        if answer_total > 0
        else 0.0
    )

    # -----------------------
    # Insufficient evidence metrics
    # -----------------------

    insufficient_results = [
        result.insufficient_evidence_evaluation
        for result in results
        if result.insufficient_evidence_evaluation.applicable
    ]

    insufficient_total = len(insufficient_results)

    insufficient_passed = sum(
        1 for evaluation in insufficient_results if evaluation.passed
    )

    insufficient_failed = insufficient_total - insufficient_passed

    insufficient_accuracy = (
        insufficient_passed / insufficient_total * 100
        if insufficient_total > 0
        else 0.0
    )

    # -----------------------
    # Faithfulness metrics
    # -----------------------

    faithfulness_results = [
        result.faithfulness for result in results if result.faithfulness.applicable
    ]

    faithfulness_total = len(faithfulness_results)

    faithfulness_passed = sum(
        1 for evaluation in faithfulness_results if evaluation.passed
    )

    faithfulness_failed = faithfulness_total - faithfulness_passed

    faithfulness_accuracy = (
        faithfulness_passed / faithfulness_total * 100
        if faithfulness_total > 0
        else 0.0
    )

    # -----------------------
    # Citation evaluation metrics
    # -----------------------

    citation_results = [
        result.citation_evaluation
        for result in results
        if result.citation_evaluation.applicable
    ]

    citation_total = len(citation_results)

    citation_passed = sum(
        1 for evaluation in citation_results if evaluation.passed
    )

    citation_failed = citation_total - citation_passed

    citation_accuracy = (
        citation_passed / citation_total * 100 if citation_total > 0 else 0.0
    )

    # -----------------------
    # Trajectory evaluation metrics
    # -----------------------

    trajectory_results = [
        result.trajectory_evaluation
        for result in results
        if result.trajectory_evaluation.applicable
    ]

    trajectory_total = len(trajectory_results)

    trajectory_passed = sum(
        1 for evaluation in trajectory_results if evaluation.passed
    )

    trajectory_failed = trajectory_total - trajectory_passed

    trajectory_accuracy = (
        trajectory_passed / trajectory_total * 100 if trajectory_total > 0 else 0.0
    )

    average_tool_calls = (
        sum(evaluation.tool_call_count for evaluation in trajectory_results)
        / trajectory_total
        if trajectory_total > 0
        else 0.0
    )

    average_max_step = (
        sum(evaluation.max_step for evaluation in trajectory_results)
        / trajectory_total
        if trajectory_total > 0
        else 0.0
    )

    # -----------------------
    # Observability metrics
    # -----------------------

    average_latency_seconds = (
        sum(result.observability.latency_seconds for result in results) / total
        if total > 0
        else 0.0
    )

    average_llm_calls = (
        sum(result.observability.llm_call_count for result in results) / total
        if total > 0
        else 0.0
    )

    return EvaluationSummaryMetrics(
        total=total,
        tool_passed=tool_passed,
        tool_failed=tool_failed,
        tool_accuracy=tool_accuracy,
        retrieval_total=retrieval_total,
        retrieval_passed=retrieval_passed,
        retrieval_failed=retrieval_failed,
        retrieval_accuracy=retrieval_accuracy,
        average_recall=average_recall,
        average_precision=average_precision,
        mean_reciprocal_rank=mean_reciprocal_rank,
        average_ndcg=average_ndcg,
        answer_total=answer_total,
        answer_passed=answer_passed,
        answer_failed=answer_failed,
        answer_accuracy=answer_accuracy,
        average_correctness=average_correctness,
        insufficient_total=insufficient_total,
        insufficient_passed=insufficient_passed,
        insufficient_failed=insufficient_failed,
        insufficient_accuracy=insufficient_accuracy,
        faithfulness_total=faithfulness_total,
        faithfulness_passed=faithfulness_passed,
        faithfulness_failed=faithfulness_failed,
        faithfulness_accuracy=faithfulness_accuracy,
        citation_total=citation_total,
        citation_passed=citation_passed,
        citation_failed=citation_failed,
        citation_accuracy=citation_accuracy,
        trajectory_total=trajectory_total,
        trajectory_passed=trajectory_passed,
        trajectory_failed=trajectory_failed,
        trajectory_accuracy=trajectory_accuracy,
        average_tool_calls=average_tool_calls,
        average_max_step=average_max_step,
        average_latency_seconds=average_latency_seconds,
        average_llm_calls=average_llm_calls,
    )
