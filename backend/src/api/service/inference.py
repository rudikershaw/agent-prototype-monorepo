"""Inference service module."""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from api.config import inference_config
from api.config.resources import load_prompt
from api.service.expression import get_cancer_types, get_expressions, get_targets


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
            tools=[get_targets, get_expressions, get_cancer_types],
        )

    async def chat(self, messages: str) -> AsyncGenerator[str, None]:
        """Handle a chat inference request."""
        async with self.agent.run_stream(messages) as result:
            async for text_chunk in result.stream_text():
                yield text_chunk


InferenceServiceDep = Annotated[InferenceService, Depends(InferenceService)]
