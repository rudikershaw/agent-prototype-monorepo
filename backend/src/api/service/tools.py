"""Tool service module."""

import ast
import re

from api.service.expression import CancerGeneExpressionService

TOOL_OPEN_TAG = "<tool_code>"
TOOL_CLOSE_TAG = "</tool_code>"


class ToolService:
    """Service for parsing and executing tool calls."""

    def __init__(self) -> None:
        """Initialize the tool service."""
        self._expression_service = CancerGeneExpressionService()
        self._tool_re = re.compile(rf"{TOOL_OPEN_TAG}(.*?){TOOL_CLOSE_TAG}", re.DOTALL)
        self._call_re = re.compile(r"(\w+)\((.*)\)", re.DOTALL)

        self._tools = {
            "get_targets": self._expression_service.get_targets,
            "get_expressions": self._expression_service.get_expressions,
        }

    def has_tool_call(self, text: str) -> bool:
        """Return True if text contains a complete tool call."""
        return bool(self._tool_re.search(text))

    def execute(self, text: str) -> str:
        """Parse and execute the first tool call found in text, returning the result as a string."""
        match = self._tool_re.search(text)
        if not match:
            raise ValueError("No tool call found in text")

        call_str = match.group(1).strip()
        call_match = self._call_re.match(call_str)
        if not call_match:
            raise ValueError(f"Unparseable tool call: {call_str!r}")

        func_name = call_match.group(1)
        if func_name not in self._tools:
            raise ValueError(f"Unknown tool: {func_name!r}")

        args_str = call_match.group(2).strip()
        args = ast.literal_eval(f"({args_str},)")
        return str(self._tools[func_name](*args))  # type: ignore
