"""Inference service module."""

import asyncio
from collections.abc import AsyncGenerator

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from api.config import inference_config
from api.config.resources import load_prompt
from api.service.tools import TOOL_CLOSE_TAG, TOOL_OPEN_TAG, ToolService


def _partial_open_tag_suffix_len(text: str) -> int:
    """Return the length of the longest suffix of text that is a prefix of TOOL_OPEN_TAG.

    Prevents yielding the start of an opening tag before we know if it's real.
    """
    for length in range(min(len(text), len(TOOL_OPEN_TAG)), 0, -1):
        if text.endswith(TOOL_OPEN_TAG[:length]):
            return length
    return 0


class InferenceService:
    """Service for handling inference requests."""

    def __init__(self) -> None:
        """Initialize the inference service."""
        self.model: OpenAIChatModel | str
        if inference_config.host:
            self.model = OpenAIChatModel(
                inference_config.model,
                provider=OpenAIProvider(inference_config.host),
            )
        else:
            self.model = inference_config.model

        self.agent = Agent(
            self.model,
            system_prompt=load_prompt("system-prompt.md"),
        )
        self.tool_service = ToolService()

    async def chat(self, messages: str) -> AsyncGenerator[str, None]:  # noqa: PLR0912
        """Stream a response, pausing to resolve tool calls before resuming the stream."""
        while True:
            buffer = ""
            tool_detected = False

            async with self.agent.run_stream(messages) as result:
                async for chunk in result.stream_text(delta=True):
                    buffer += chunk

                    if tool_detected:
                        if TOOL_CLOSE_TAG in buffer:
                            break
                        continue

                    if TOOL_OPEN_TAG in buffer:
                        tool_detected = True
                        # Yield anything that came before the opening tag
                        preamble = buffer[: buffer.index(TOOL_OPEN_TAG)]
                        if preamble:
                            yield preamble
                        if TOOL_CLOSE_TAG in buffer:
                            break
                        continue

                    # Stream normally up-to the tool call
                    partial_len = _partial_open_tag_suffix_len(buffer)
                    if partial_len:
                        safe = buffer[:-partial_len]
                        if safe:
                            yield safe
                        buffer = buffer[-partial_len:]
                    else:
                        yield buffer
                        buffer = ""

            if not tool_detected:
                # Normal end of stream. Flush buffer.
                if buffer:
                    yield buffer
                break

            if TOOL_CLOSE_TAG not in buffer:
                yield "I'm sorry, it seems I am having trouble processing that request. Would you like me to try again?"
                break

            tool_result = self.tool_service.execute(buffer)
            messages += f"ASSISTANT: {buffer}\n\nSYSTEM: {tool_result}"
            asyncio.create_task(result.cancel())  # noqa: RUF006
            # Loop continues - Call LLM again with complete history with tool call appended.
