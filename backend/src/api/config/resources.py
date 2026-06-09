"""A module for loading non-python resources such as prompts and data files."""

from pathlib import Path

from pydantic import FilePath

_RESOURCES_DIR = Path(__file__).parent.parent / "resources"


def load_prompt(filename: str) -> str:
    """Load a prompt string from the resources directory."""
    return load_resource("prompts", filename).read_text(encoding="utf-8")


def load_resource(*parts: str) -> FilePath:
    """Load a resource from the resources directory."""
    return _RESOURCES_DIR / Path(*parts)
