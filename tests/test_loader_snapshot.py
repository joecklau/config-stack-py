from __future__ import annotations

import json
from pathlib import Path

from config_stack import load_mapping_file, write_resolved_snapshot


def test_load_mapping_file_supports_json(tmp_path: Path) -> None:
    path = tmp_path / "config.json"
    path.write_text(json.dumps({"a": 1}), encoding="utf-8")

    assert load_mapping_file(path) == {"a": 1}


def test_load_mapping_file_supports_toml(tmp_path: Path) -> None:
    path = tmp_path / "config.toml"
    path.write_text(
        """
[service]
workers = 3
""",
        encoding="utf-8",
    )

    assert load_mapping_file(path) == {"service": {"workers": 3}}


def test_write_resolved_snapshot_creates_parent_dirs(tmp_path: Path) -> None:
    path = tmp_path / "snapshots" / "resolved.json"

    write_resolved_snapshot({"b": 2, "a": 1}, path)

    assert json.loads(path.read_text(encoding="utf-8")) == {"a": 1, "b": 2}
