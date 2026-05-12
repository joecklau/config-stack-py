from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping


def deep_merge_dicts(
    base_dict: Mapping[str, Any], override_dict: Mapping[str, Any]
) -> dict[str, Any]:
    """Recursively merge mappings while replacing lists and scalar values."""
    merged = deepcopy(dict(base_dict))
    for key, value in override_dict.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge_dicts(merged[key], value)
        else:
            merged[key] = deepcopy(value)
    return merged
