"""Chat controller module."""

import asyncio
from collections.abc import AsyncIterable

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from api.service.inference import InferenceService

router = APIRouter()
_inference_service = InferenceService()


class ChatRequest(BaseModel):
    """Chat request model."""

    messages: str = Field(
        title="Chat messages",
        description="The chat history as a string.",
    )


@router.post("/chat", tags=["chat"], response_class=StreamingResponse)
async def chat(chat_request: ChatRequest) -> AsyncIterable[str]:
    """Chat endpoint."""
    try:
        async with asyncio.timeout(30.0):
            async for text_chunk in _inference_service.chat(chat_request.messages):
                yield text_chunk
    except TimeoutError:
        yield "My apologies, I've been unable to process your request. Would you like me to try again?"
