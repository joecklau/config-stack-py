from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .env import expand_env_vars
from .errors import ConfigStackError
from .loader import load_mapping_file
from .merge import deep_merge_dicts
from .paths import as_path_list, resolve_relative_path


CONFIG_STACK_KIND = "config.stack"
STACK_CONTROL_KEYS = {"kind", "schema_version", "layers", "overrides"}


@dataclass(frozen=True)
class CompositionResult:
    config: dict[str, Any]
    source_path: Path
    source_kind: str | None


def compose_config_file(
    path: Path | str,
    *,
    base_config: dict[str, Any] | None = None,
    stack_kind: str = CONFIG_STACK_KIND,
    expand_env: bool = False,
    strict_env: bool = False,
) -> CompositionResult:
    """Compose a config file, applying generic stack layers when requested."""
    source_path = Path(path).resolve()
    payload = load_mapping_file(source_path)
    source_kind = normalize_kind(payload.get("kind"))

    if source_kind == stack_kind:
        config = _compose_stack_file(
            source_path,
            payload,
            expand_env=expand_env,
            strict_env=strict_env,
        )
    else:
        config = compose_document(
            source_path,
            expand_env=expand_env,
            strict_env=strict_env,
        )

    if base_config:
        config = deep_merge_dicts(base_config, config)

    return CompositionResult(
        config=config,
        source_path=source_path,
        source_kind=source_kind,
    )


def compose_document(
    path: Path | str,
    *,
    visited: set[Path] | None = None,
    expand_env: bool = False,
    strict_env: bool = False,
) -> dict[str, Any]:
    """Compose a non-stack document with generic `extends` support."""
    resolved_path = Path(path).resolve()
    active = set() if visited is None else set(visited)
    if resolved_path in active:
        raise ConfigStackError(
            f"Config composition cycle detected at '{resolved_path}'."
        )

    payload = load_mapping_file(resolved_path)
    combined: dict[str, Any] = {}
    nested_visited = set(active)
    nested_visited.add(resolved_path)

    for relative in as_path_list(payload.get("extends")):
        parent_path = resolve_relative_path(resolved_path, relative)
        parent_payload = compose_document(
            parent_path,
            visited=nested_visited,
            expand_env=expand_env,
            strict_env=strict_env,
        )
        combined = deep_merge_dicts(combined, parent_payload)

    result = deep_merge_dicts(combined, payload)
    if expand_env:
        return expand_env_vars(result, strict=strict_env)
    return result


def normalize_kind(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ConfigStackError(
            f"Config file kind must be a string, found {type(value).__name__}."
        )
    normalized = value.strip()
    return normalized or None


def _compose_stack_file(
    stack_path: Path,
    stack_payload: dict[str, Any],
    *,
    expand_env: bool,
    strict_env: bool,
) -> dict[str, Any]:
    composed: dict[str, Any] = {}
    visited = {stack_path.resolve()}

    for relative in as_path_list(stack_payload.get("layers")):
        layer_path = resolve_relative_path(stack_path, relative)
        layer_payload = compose_document(
            layer_path,
            visited=visited,
            expand_env=expand_env,
            strict_env=strict_env,
        )
        composed = deep_merge_dicts(composed, layer_payload)

    inline_payload = {
        key: deepcopy(value)
        for key, value in stack_payload.items()
        if key not in STACK_CONTROL_KEYS
    }
    if inline_payload:
        composed = deep_merge_dicts(composed, inline_payload)

    overrides = stack_payload.get("overrides") or {}
    if overrides:
        if not isinstance(overrides, dict):
            raise ConfigStackError(
                f"Stack file '{stack_path}' has a non-mapping 'overrides' section."
            )
        composed = deep_merge_dicts(composed, overrides)

    if expand_env:
        return expand_env_vars(composed, strict=strict_env)
    return composed
