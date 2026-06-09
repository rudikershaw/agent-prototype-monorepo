"""Configuration module for the API."""

import os

from pydantic import BaseModel, Field


class InferenceConfig(BaseModel):
    """Configuration for the inference service."""

    model: str = Field(
        title="Model Name",
        description="The name of the model to use for inference.",
    )

    host: str | None = Field(
        title="Inference Host",
        description="The host URL for the inference service.",
        default="http://localhost:1234/v1",
    )


_inference_host = os.getenv("INFERENCE_HOST", None)
_inference_model = os.getenv("INFERENCE_MODEL", "anthropic:claude-sonnet-4-6")

inference_config = InferenceConfig(model=_inference_model, host=_inference_host)

__all__ = ["InferenceConfig", "inference_config"]
