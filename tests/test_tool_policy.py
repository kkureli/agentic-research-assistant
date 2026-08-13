from unittest.mock import patch

from app.agents.tool_policy import evaluate_tool_call, tool_call_key
from app.agents.tool_registry import TOOL_FUNCTIONS


def test_unknown_tool_is_rejected_without_execution() -> None:
    with patch.dict(TOOL_FUNCTIONS, {}, clear=False):
        decision = evaluate_tool_call(
            "os_system",
            {"command": "rm -rf /"},
            executed_count=0,
            executed_keys=set(),
            max_tool_calls=8,
        )

    assert decision.allowed is False
    assert decision.duplicate is False
    assert "Unknown tool" in (decision.message or "")
    assert "os_system" not in TOOL_FUNCTIONS


def test_tool_call_limit_returns_controlled_failure() -> None:
    with patch.object(TOOL_FUNCTIONS["calculate"], "__call__") as calculate:
        decision = evaluate_tool_call(
            "calculate",
            {"operation": "add", "a": 1, "b": 2},
            executed_count=8,
            executed_keys=set(),
            max_tool_calls=8,
        )

    assert decision.allowed is False
    assert "Tool call limit exceeded" in (decision.message or "")
    calculate.assert_not_called()


def test_duplicate_exact_tool_call_remains_blocked() -> None:
    arguments = {"operation": "add", "a": 1, "b": 2}
    key = tool_call_key("calculate", arguments)

    decision = evaluate_tool_call(
        "calculate",
        arguments,
        executed_count=1,
        executed_keys={key},
        max_tool_calls=8,
    )

    assert decision.allowed is False
    assert decision.duplicate is True
    assert "already been executed" in (decision.message or "")


def test_invalid_arguments_are_rejected() -> None:
    decision = evaluate_tool_call(
        "calculate",
        {"operation": "add", "a": 1},
        executed_count=0,
        executed_keys=set(),
        max_tool_calls=8,
    )

    assert decision.allowed is False
    assert "Missing required tool arguments" in (decision.message or "")


def test_registered_tool_with_valid_arguments_is_allowed() -> None:
    decision = evaluate_tool_call(
        "search_knowledge_base",
        {"query": "Asteria Q2 growth"},
        executed_count=0,
        executed_keys=set(),
        max_tool_calls=8,
    )

    assert decision.allowed is True
    assert decision.duplicate is False
