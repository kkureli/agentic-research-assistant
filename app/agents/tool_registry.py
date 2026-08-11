from app.agents.tools.calculator import calculate
from app.agents.tools.knowledge_base import search_knowledge_base
from app.agents.tools.web_search import search_web

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": (
                "Search the internal research knowledge base for relevant evidence."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                    },
                    "top_k": {
                        "type": "integer",
                        "default": 5,
                    },
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": (
                "Perform an arithmetic calculation. "
                "Use this tool instead of calculating numerical results yourself."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": [
                            "add",
                            "subtract",
                            "multiply",
                            "divide",
                        ],
                    },
                    "a": {
                        "type": "number",
                    },
                    "b": {
                        "type": "number",
                    },
                },
                "required": [
                    "operation",
                    "a",
                    "b",
                ],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": (
                "Search the public web for current or external information "
                "that is not available in the internal knowledge base."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                    },
                    "max_results": {
                        "type": "integer",
                        "default": 5,
                    },
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
    },
]


TOOL_FUNCTIONS = {
    "search_knowledge_base": search_knowledge_base,
    "calculate": calculate,
    "search_web": search_web,
}
