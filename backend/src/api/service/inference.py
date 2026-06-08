"""Inference service module."""

from collections.abc import AsyncGenerator

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from api.config import inference_config


class InferenceService:
    """Service for handling inference requests."""

    def __init__(self) -> None:
        """Initialize the inference service."""
        self.model: OpenAIChatModel | str
        if inference_config.host:
            self.model = OpenAIChatModel(inference_config.model, provider=OpenAIProvider(inference_config.host))
        else:
            self.model = inference_config.model

        self.agent = Agent(
            self.model,
            system_prompt="SYSTEM: You are Gene, a helpful assistant for researchers \
                in BioTech. Maintain a friendly, concise, and professionally tone. \
                Provide accurate and relevant information. If you don't know the \
                answer, say you don't know. Always be concise and to the point.",
        )

    async def chat(self, messages: str) -> AsyncGenerator[str, None]:
        """Handle a chat inference request."""
        async with self.agent.run_stream(messages) as result:
            async for text_chunk in result.stream_text(delta=True):
                yield text_chunk
