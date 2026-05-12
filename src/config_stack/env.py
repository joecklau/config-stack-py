from __future__ import annotations

import os
import re
from copy import deepcopy
from typing import Any, Mapping

from .errors import ConfigStackError


_ENV_PATTERN = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(?::-(.*?))?\}")


def expand_env_vars(
    value: Any,
    *,
    environ: Mapping[str, str] | None = None,
    strict: bool = False,
) -> Any:
    """Recursively expand ${VAR} and ${VAR:-default} strings in config data."""
    env = os.environ if environ is None else environ

    if isinstance(value, dict):
        return {
            key: expand_env_vars(item, environ=env, strict=strict)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [expand_env_vars(item, environ=env, strict=strict) for item in value]
    if not isinstance(value, str):
        return deepcopy(value)

    def replace(match: re.Match[str]) -> str:
        name = match.group(1)
        default = match.group(2)
        if name in env:
            return env[name]
        if default is not None:
            return default
        if strict:
            raise ConfigStackError(f"Environment variable '{name}' is not set.")
        return match.group(0)

    return _ENV_PATTERN.sub(replace, value)

