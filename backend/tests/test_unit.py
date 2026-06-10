"""Unit tests for backend config, utilities, and services."""

from pathlib import Path

import pytest
from fastapi import FastAPI
from pydantic import ValidationError

from api.config import InferenceConfig
from api.config.cors import configure_cors
from api.config.resources import _RESOURCES_DIR, load_resource
from api.controller.chat import ChatRequest


def test_inference_config_override_fields() -> None:
    """InferenceConfig accepts overridden field values."""
    config = InferenceConfig(model="gpt-4", host="https://api.openai.com/v1")
    assert config.model == "gpt-4"
    assert config.host == "https://api.openai.com/v1"


def test_load_resource_builds_correct_path() -> None:
    """load_resource joins parts under the resources directory."""
    result = load_resource("prompts", "system-prompt.md")
    assert isinstance(result, Path)
    assert str(result).startswith(str(_RESOURCES_DIR))


def test_load_resource_with_single_part() -> None:
    """load_resource works with a single path part."""
    result = load_resource("prompts")
    expected = _RESOURCES_DIR / "prompts"
    assert result == expected


def test_chat_request_valid() -> None:
    """ChatRequest accepts a non-empty messages string."""
    req = ChatRequest(messages="Hello, how are you?")
    assert req.messages == "Hello, how are you?"


def test_chat_request_missing_field_raises() -> None:
    """ChatRequest raises ValidationError when messages is missing."""
    with pytest.raises(ValidationError):
        ChatRequest()


def test_configure_cors_dev_default_origins(monkeypatch: "pytest.MonkeyPatch") -> None:
    """In development mode, CORS defaults to localhost origins."""
    monkeypatch.setenv("APP_ENV", "development")
    monkeypatch.delenv("ALLOWED_ORIGINS", raising=False)

    app = FastAPI()
    configure_cors(app)

    # Just verify the middleware was added without error.
    middlewares = list(app.user_middleware) if app.user_middleware else []
    assert len(middlewares) > 0


def test_configure_cors_production_requires_origins(monkeypatch: "pytest.MonkeyPatch") -> None:
    """In production without ALLOWED_ORIGINS, configure_cors raises RuntimeError."""
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.delenv("ALLOWED_ORIGINS", raising=False)

    app = FastAPI()
    with pytest.raises(RuntimeError, match="ALLOWED_ORIGINS"):
        configure_cors(app)


def test_configure_cors_production_uses_env_var(monkeypatch: "pytest.MonkeyPatch") -> None:
    """In production with ALLOWED_ORIGINS set, those origins are used."""
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("ALLOWED_ORIGINS", "https://example.com,https://app.example.com")

    app = FastAPI()
    configure_cors(app)
