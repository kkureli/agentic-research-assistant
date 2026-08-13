from app.schemas.agent import AgentResult
from app.schemas.evaluation import CriticEvaluation

DEFAULT_MAX_CRITIC_ROUNDS = 2


def evaluate_critic(
    agent_result: AgentResult,
    max_critic_rounds: int = DEFAULT_MAX_CRITIC_ROUNDS,
) -> CriticEvaluation:
    traces = agent_result.critic_traces
    critic_rounds = len(traces)
    retry_count = max(critic_rounds - 1, 0)

    if not traces:
        return CriticEvaluation(
            applicable=False,
            critic_rounds=0,
            retry_count=0,
            initially_sufficient=None,
            eventually_sufficient=None,
            passed=None,
        )

    initially_sufficient = traces[0].sufficient
    eventually_sufficient = any(trace.sufficient for trace in traces)

    bounded = critic_rounds <= max_critic_rounds
    retry_consistent = retry_count == critic_rounds - 1
    no_retry_after_success = not initially_sufficient or critic_rounds == 1

    return CriticEvaluation(
        applicable=True,
        critic_rounds=critic_rounds,
        retry_count=retry_count,
        initially_sufficient=initially_sufficient,
        eventually_sufficient=eventually_sufficient,
        passed=bounded and retry_consistent and no_retry_after_success,
    )
