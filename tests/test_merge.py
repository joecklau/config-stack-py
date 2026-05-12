from __future__ import annotations

from config_stack import deep_merge_dicts


def test_deep_merge_replaces_lists_and_scalars() -> None:
    base = {
        "nested": {"a": 1, "list": ["old"]},
        "scalar": "base",
    }
    override = {
        "nested": {"b": 2, "list": ["new"]},
        "scalar": "override",
    }

    result = deep_merge_dicts(base, override)

    assert result == {
        "nested": {"a": 1, "b": 2, "list": ["new"]},
        "scalar": "override",
    }
    assert base["nested"]["list"] == ["old"]
