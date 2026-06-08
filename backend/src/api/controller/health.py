"""Health check controller module."""

import os

from fastapi import APIRouter, Header
from pydantic import BaseModel, Field

router = APIRouter()


class HealthCheck(BaseModel):
    """Health check response model."""

    status: str = Field(
        title="Health check status",
        description="The status of the health check. Should be 'ok' if the service is healthy.",
        examples=["ok", "error"],
        default="ok",
    )
    user_agent: str | None = Field(
        title="User agent",
        description="The user agent of the request that triggered the health check.",
        default="",
    )
    api_env: str = Field(
        title="API environment",
        description="The current environment the API is running in (e.g., 'production', 'development').",
    )


@router.get("/", tags=["health"], response_model=HealthCheck)
async def health(user_agent: str | None = Header()) -> HealthCheck:
    """Health check endpoint."""
    return HealthCheck(
        user_agent=user_agent,
        api_env=os.getenv("APP_ENV", "production"),
    )
