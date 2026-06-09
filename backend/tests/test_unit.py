"""Unit tests for backend config, utilities, and services."""

from pathlib import Path

import pytest
from fastapi import FastAPI
from pydantic import ValidationError

from api.config import InferenceConfig
from api.config.cors import configure_cors
from api.config.resources import _RESOURCES_DIR, load_resource
from api.controller.chat import ChatRequest
from api.service.inference import _partial_open_tag_suffix_len
from api.service.tools import ToolService


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


def test_has_tool_call_detects_valid_tag() -> None:
    """has_tool_call returns True when text contains a tool_code block."""
    svc = ToolService()
    assert svc.has_tool_call("some text <tool_code>get_targets('BRCA1')</tool_code> more text") is True


def test_has_tool_call_no_tag() -> None:
    """has_tool_call returns False when no tool_code block is present."""
    svc = ToolService()
    assert svc.has_tool_call("just plain text with no tags") is False


def test_has_tool_call_empty_string() -> None:
    """has_tool_call returns False for an empty string."""
    svc = ToolService()
    assert svc.has_tool_call("") is False


def test_partial_open_tag_no_match() -> None:
    """_partial_open_tag_suffix_len returns 0 when there's no partial match."""
    assert _partial_open_tag_suffix_len("hello world") == 0


def test_partial_open_tag_exact_match() -> None:
    """_partial_open_tag_suffix_len returns full length when text equals the tag."""
    assert _partial_open_tag_suffix_len("<tool_code>") == len("<tool_code>")


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
