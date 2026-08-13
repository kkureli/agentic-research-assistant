from app.schemas.evaluation import EvaluationResult


def print_case_result(result: EvaluationResult) -> None:
    tool_routing = result.tool_routing
    retrieval = result.retrieval
    answer_evaluation = result.answer_evaluation
    insufficient_evidence = result.insufficient_evidence_evaluation
    faithfulness = result.faithfulness
    citation_evaluation = result.citation_evaluation
    trajectory_evaluation = result.trajectory_evaluation
    observability = result.observability
    critic_evaluation = result.critic_evaluation

    # -----------------------
    # Tool routing output
    # -----------------------

    tool_status = "PASS" if tool_routing.passed else "FAIL"

    print(f"Tool routing: {tool_status}")
    print(f"Actual tools: {tool_routing.actual_tools}")

    if tool_routing.missing_required_tools:
        print(f"Missing required tools: {tool_routing.missing_required_tools}")

    if tool_routing.forbidden_tools_used:
        print(f"Forbidden tools used: {tool_routing.forbidden_tools_used}")

    # -----------------------
    # Retrieval output
    # -----------------------

    if not retrieval.applicable:
        retrieval_status = "N/A"
    elif retrieval.passed:
        retrieval_status = "PASS"
    else:
        retrieval_status = "FAIL"

    print(f"Retrieval: {retrieval_status}")
    print(f"Retrieved sources: {retrieval.retrieved_sources}")

    if retrieval.applicable:
        print(f"Recall:          {retrieval.recall * 100:.2f}%")
        print(f"Precision:       {retrieval.precision * 100:.2f}%")
        print(f"Reciprocal Rank: {retrieval.reciprocal_rank:.3f}")
        print(f"nDCG:            {retrieval.ndcg:.3f}")

    if retrieval.missing_sources:
        print(f"Missing sources: {retrieval.missing_sources}")

    # -----------------------
    # Answer evaluation output
    # -----------------------

    if answer_evaluation.applicable:
        answer_status = "PASS" if answer_evaluation.passed else "FAIL"

        print(f"Answer: {answer_status}")
        print(
            f"Answer correctness: {answer_evaluation.correctness_score * 100:.2f}%"
        )

        for fact_result in answer_evaluation.fact_results:
            fact_status = "PASS" if fact_result.supported else "FAIL"

            print(f"  [{fact_status}] {fact_result.fact}")
    else:
        print("Answer evaluation: N/A")

    # -----------------------
    # Insufficient evidence output
    # -----------------------

    if insufficient_evidence.applicable:
        insufficient_status = "PASS" if insufficient_evidence.passed else "FAIL"

        print(f"Insufficient evidence handling: {insufficient_status}")

        print(f"Correctly declined: {insufficient_evidence.correctly_declined}")
    else:
        print("Insufficient evidence evaluation: N/A")

    # -----------------------
    # Faithfulness output
    # -----------------------

    if faithfulness.applicable:
        faithfulness_status = "PASS" if faithfulness.passed else "FAIL"

        print(f"Faithfulness: {faithfulness_status}")
        print(f"Faithful: {faithfulness.faithful}")

        if faithfulness.unsupported_claims:
            print("Unsupported claims:")

            for claim in faithfulness.unsupported_claims:
                print(f"  - {claim}")
    else:
        print("Faithfulness evaluation: N/A")

    # -----------------------
    # Citation evaluation output
    # -----------------------

    if citation_evaluation.applicable:
        citation_status = "PASS" if citation_evaluation.passed else "FAIL"

        print(f"Citation: {citation_status}")
        print(f"Found citations: {citation_evaluation.found_citations}")
        print(f"Available citations: {citation_evaluation.available_citations}")

        if citation_evaluation.invalid_citations:
            print(f"Invalid citations: {citation_evaluation.invalid_citations}")

        if citation_evaluation.missing_prefixes:
            print(
                f"Missing citation prefixes: {citation_evaluation.missing_prefixes}"
            )
    else:
        print("Citation evaluation: N/A")

    # -----------------------
    # Trajectory evaluation output
    # -----------------------

    if trajectory_evaluation.applicable:
        trajectory_status = "PASS" if trajectory_evaluation.passed else "FAIL"

        print(f"Trajectory: {trajectory_status}")
        print(f"Tool calls: {trajectory_evaluation.tool_call_count}")
        print(f"Max step: {trajectory_evaluation.max_step}")
        print(f"Duplicate tool calls: {trajectory_evaluation.duplicate_tool_calls}")

        if trajectory_evaluation.excessive_tool_calls:
            print(f"Excessive tool calls: {trajectory_evaluation.excessive_tool_calls}")
    else:
        print("Trajectory evaluation: N/A")

    # -----------------------
    # Observability output
    # -----------------------

    print("Observability")
    print(f"Latency:    {observability.latency_seconds:.2f}s")
    print(f"Tool calls: {observability.tool_call_count}")
    print(f"LLM calls:  {observability.llm_call_count}")

    # -----------------------
    # Critic evaluation output
    # -----------------------

    if critic_evaluation.applicable:
        critic_status = "PASS" if critic_evaluation.passed else "FAIL"

        print(f"Critic: {critic_status}")
        print(f"Critic rounds: {critic_evaluation.critic_rounds}")
        print(f"Retries: {critic_evaluation.retry_count}")
        print(f"Initially sufficient: {critic_evaluation.initially_sufficient}")
        print(f"Eventually sufficient: {critic_evaluation.eventually_sufficient}")
    else:
        print("Critic evaluation: N/A")
