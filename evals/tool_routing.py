from app.schemas.agent import AgentResult
from app.schemas.evaluation import EvaluationCase, ToolRoutingEvaluation


def evaluate_tool_routing(
    case: EvaluationCase,
    agent_result: AgentResult,
) -> ToolRoutingEvaluation:
    actual_tools = list(dict.fromkeys(trace.tool_name for trace in agent_result.traces))

    missing_required_tools = [
        tool for tool in case.required_tools if tool not in actual_tools
    ]

    forbidden_tools_used = [
        tool for tool in case.forbidden_tools if tool in actual_tools
    ]

    passed = not missing_required_tools and not forbidden_tools_used

    return ToolRoutingEvaluation(
        required_tools=case.required_tools,
        actual_tools=actual_tools,
        missing_required_tools=missing_required_tools,
        forbidden_tools_used=forbidden_tools_used,
        passed=passed,
    )
