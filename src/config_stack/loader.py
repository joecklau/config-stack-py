from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from .errors import ConfigStackError

try:  # pragma: no cover - Python < 3.11 compatibility
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore[no-redef]


def load_mapping_file(path: Path | str, *, missing_ok: bool = False) -> dict[str, Any]:
    """Load a YAML, JSON, or TOML file and require a mapping at the top level."""
    resolved = Path(path)
    if not resolved.exists():
        if missing_ok:
            return {}
        raise ConfigStackError(f"Config file '{resolved}' does not exist.")

    suffix = resolved.suffix.lower()
    if suffix == ".toml":
        with resolved.open("rb") as handle:
            payload = tomllib.load(handle)
    else:
        with resolved.open("r", encoding="utf-8") as handle:
            if suffix == ".json":
                payload = json.load(handle)
            else:
                payload = yaml.safe_load(handle)

    if payload is None:
        return {}
    if not isinstance(payload, dict):
        raise ConfigStackError(
            f"Config file '{resolved}' must contain a mapping at the top level."
        )
    return payload
