from __future__ import annotations

import json
from dataclasses import dataclass

from app.agents.tool_registry import TOOL_DEFINITIONS, TOOL_FUNCTIONS


@dataclass(frozen=True)
class ToolPolicyDecision:
    allowed: bool
    duplicate: bool = False
    message: str | None = None


def tool_call_key(tool_name: str, arguments: dict) -> tuple[str, str]:
    return (tool_name, json.dumps(arguments, sort_keys=True))


def evaluate_tool_call(
    tool_name: str,
    arguments: dict,
    *,
    executed_count: int,
    executed_keys: set[tuple[str, str]],
    max_tool_calls: int,
) -> ToolPolicyDecision:
    if tool_name not in TOOL_FUNCTIONS:
        return ToolPolicyDecision(
            allowed=False,
            message=(
                f"Unknown tool '{tool_name}'. Only registered tools can be executed."
            ),
        )

    if executed_count >= max_tool_calls:
        return ToolPolicyDecision(
            allowed=False,
            message=(
                "Tool call limit exceeded. Do not call additional tools. "
                "Answer with the evidence already collected."
            ),
        )

    definition = _definition_for(tool_name)
    if definition is None:
        return ToolPolicyDecision(
            allowed=False,
            message=(
                f"Unknown tool '{tool_name}'. Only registered tools can be executed."
            ),
        )

    argument_error = _validate_arguments(definition, arguments)
    if argument_error:
        return ToolPolicyDecision(allowed=False, message=argument_error)

    key = tool_call_key(tool_name, arguments)
    if key in executed_keys:
        return ToolPolicyDecision(
            allowed=False,
            duplicate=True,
            message=(
                "This exact tool call has already been executed. "
                "Use a different query or strategy if more evidence "
                "is needed."
            ),
        )

    return ToolPolicyDecision(allowed=True)


def _definition_for(tool_name: str) -> dict | None:
    for item in TOOL_DEFINITIONS:
        function = item.get("function", {})
        if function.get("name") == tool_name:
            return function
    return None


def _validate_arguments(definition: dict, arguments: dict) -> str | None:
    if not isinstance(arguments, dict):
        return "Tool arguments must be a JSON object."

    parameters = definition.get("parameters", {})
    properties = parameters.get("properties", {})
    required = parameters.get("required", [])
    additional = parameters.get("additionalProperties", True)

    missing = [name for name in required if name not in arguments]
    if missing:
        return f"Missing required tool arguments: {', '.join(missing)}."

    extra = sorted(set(arguments) - set(properties))
    if extra and additional is False:
        return f"Unexpected tool arguments: {', '.join(extra)}."

    for name, value in arguments.items():
        schema = properties.get(name)
        if not schema:
            continue

        error = _validate_value(name, value, schema)
        if error:
            return error

    return None


def _validate_value(name: str, value, schema: dict) -> str | None:
    enum_values = schema.get("enum")
    if enum_values is not None and value not in enum_values:
        return f"Invalid value for '{name}'."

    expected = schema.get("type")
    if expected == "string" and not isinstance(value, str):
        return f"Argument '{name}' must be a string."
    if expected == "integer" and type(value) is not int:
        return f"Argument '{name}' must be an integer."
    if expected == "number" and not isinstance(value, (int, float)):
        return f"Argument '{name}' must be a number."

    return None
