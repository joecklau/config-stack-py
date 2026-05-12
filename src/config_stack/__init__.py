from __future__ import annotations

from .composer import (
    CONFIG_STACK_KIND,
    CompositionResult,
    compose_config_file,
    compose_document,
)
from .env import expand_env_vars
from .errors import ConfigStackError
from .loader import load_mapping_file
from .merge import deep_merge_dicts
from .paths import as_path_list, resolve_relative_path
from .snapshot import write_resolved_snapshot

__all__ = [
    "CONFIG_STACK_KIND",
    "CompositionResult",
    "ConfigStackError",
    "as_path_list",
    "compose_config_file",
    "compose_document",
    "deep_merge_dicts",
    "expand_env_vars",
    "load_mapping_file",
    "resolve_relative_path",
    "write_resolved_snapshot",
]

