from app.schemas.evaluation import EvaluationResult
from evals.reporting.metrics import calculate_summary_metrics


def print_evaluation_summary(
    results: list[EvaluationResult],
) -> None:
    metrics = calculate_summary_metrics(results)

    print("\n==============================")
    print("Evaluation Summary")
    print("==============================")

    print(f"Total cases: {metrics.total}")

    print("\nTool Routing")
    print(f"Passed:   {metrics.tool_passed}")
    print(f"Failed:   {metrics.tool_failed}")
    print(f"Accuracy: {metrics.tool_accuracy:.2f}%")

    print("\nRetrieval")
    print(f"Applicable cases: {metrics.retrieval_total}")
    print(f"Passed:            {metrics.retrieval_passed}")
    print(f"Failed:            {metrics.retrieval_failed}")
    print(f"Accuracy:          {metrics.retrieval_accuracy:.2f}%")
    print(f"Average Recall:    {metrics.average_recall * 100:.2f}%")
    print(f"Average Precision: {metrics.average_precision * 100:.2f}%")
    print(f"MRR:               {metrics.mean_reciprocal_rank:.3f}")
    print(f"Average nDCG:      {metrics.average_ndcg:.3f}")

    print("\nAnswer Evaluation")
    print(f"Applicable cases:    {metrics.answer_total}")
    print(f"Passed:              {metrics.answer_passed}")
    print(f"Failed:              {metrics.answer_failed}")
    print(f"Accuracy:            {metrics.answer_accuracy:.2f}%")
    print(f"Average Correctness: {metrics.average_correctness * 100:.2f}%")

    print("\nInsufficient Evidence")
    print(f"Applicable cases: {metrics.insufficient_total}")
    print(f"Passed:           {metrics.insufficient_passed}")
    print(f"Failed:           {metrics.insufficient_failed}")
    print(f"Accuracy:         {metrics.insufficient_accuracy:.2f}%")

    print("\nFaithfulness")
    print(f"Applicable cases: {metrics.faithfulness_total}")
    print(f"Passed:           {metrics.faithfulness_passed}")
    print(f"Failed:           {metrics.faithfulness_failed}")
    print(f"Accuracy:         {metrics.faithfulness_accuracy:.2f}%")

    print("\nCitation Evaluation")
    print(f"Applicable cases: {metrics.citation_total}")
    print(f"Passed:           {metrics.citation_passed}")
    print(f"Failed:           {metrics.citation_failed}")
    print(f"Accuracy:         {metrics.citation_accuracy:.2f}%")

    print("\nTrajectory Evaluation")
    print(f"Applicable cases: {metrics.trajectory_total}")
    print(f"Passed:           {metrics.trajectory_passed}")
    print(f"Failed:           {metrics.trajectory_failed}")
    print(f"Accuracy:         {metrics.trajectory_accuracy:.2f}%")
    print(f"Avg Tool Calls:   {metrics.average_tool_calls:.2f}")
    print(f"Avg Max Step:     {metrics.average_max_step:.2f}")

    print("\nObservability")
    print(f"Avg Latency:   {metrics.average_latency_seconds:.2f}s")
    print(f"Avg LLM Calls: {metrics.average_llm_calls:.2f}")
    print(f"Avg Tool Calls: {metrics.average_tool_calls:.2f}")

    print("\nCritic Evaluation")
    print(f"Applicable cases:       {metrics.critic_total}")
    print(f"Passed:                 {metrics.critic_passed}")
    print(f"Failed:                 {metrics.critic_failed}")
    print(f"Accuracy:               {metrics.critic_accuracy:.2f}%")
    print(f"Avg Critic Rounds:      {metrics.average_critic_rounds:.2f}")
    print(f"Avg Critic Retries:     {metrics.average_critic_retries:.2f}")
    print(f"Eventual Sufficiency:   {metrics.critic_eventual_success_rate:.2f}%")
