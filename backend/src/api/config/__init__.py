"""Configuration module for the API."""

from pydantic import BaseModel, Field


class InferenceConfig(BaseModel):
    """Configuration for the inference service."""

    model: str = Field(
        title="Model Name",
        description="The name of the model to use for inference.",
        default="qwen3.6-35b-a3b-uncensored-genesis-v2-apex-mtp",
    )

    host: str = Field(
        title="Inference Host",
        description="The host URL for the inference service.",
        default="http://localhost:1234/v1",
    )


inference_config = InferenceConfig()

__all__ = ["InferenceConfig", "inference_config"]
