import json

from app.schemas.agent import AgentResult
from app.schemas.evaluation import TrajectoryEvaluation


def evaluate_trajectory(
    agent_result: AgentResult,
    max_tool_calls: int = 6,
    max_steps: int = 4,
) -> TrajectoryEvaluation:
    traces = agent_result.traces

    if not traces:
        return TrajectoryEvaluation(
            applicable=False,
            tool_call_count=0,
            max_step=0,
            duplicate_tool_calls=0,
            excessive_tool_calls=False,
            passed=None,
        )

    tool_call_count = len(traces)
    max_step = max(trace.step for trace in traces)

    seen_calls: set[tuple[str, str]] = set()
    duplicate_tool_calls = 0

    for trace in traces:
        call_key = (trace.tool_name, json.dumps(trace.arguments, sort_keys=True))

        if call_key in seen_calls:
            duplicate_tool_calls += 1
        else:
            seen_calls.add(call_key)

    excessive_tool_calls = tool_call_count > max_tool_calls

    return TrajectoryEvaluation(
        applicable=True,
        tool_call_count=tool_call_count,
        max_step=max_step,
        duplicate_tool_calls=duplicate_tool_calls,
        excessive_tool_calls=excessive_tool_calls,
        passed=(
            duplicate_tool_calls == 0
            and not excessive_tool_calls
            and max_step <= max_steps
        ),
    )
