from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Any

from .errors import ConfigStackError


def as_path_list(value: Any) -> Iterable[str]:
    """Normalize a string or list of strings into a path iterable."""
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    raise ConfigStackError(
        "Config composition path lists must be strings or lists of strings."
    )


def resolve_relative_path(source_path: Path | str, relative: str) -> Path:
    """Resolve a config path relative to the file that referenced it."""
    candidate = Path(relative)
    if candidate.is_absolute():
        return candidate
    return (Path(source_path).parent / candidate).resolve()
