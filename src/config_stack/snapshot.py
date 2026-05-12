from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

import yaml


def write_resolved_snapshot(config: Mapping[str, Any], path: Path | str) -> Path:
    """Write a resolved config snapshot as YAML or JSON based on suffix."""
    snapshot_path = Path(path)
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    suffix = snapshot_path.suffix.lower()
    with snapshot_path.open("w", encoding="utf-8", newline="\n") as handle:
        if suffix == ".json":
            json.dump(config, handle, indent=2, sort_keys=True)
            handle.write("\n")
        else:
            yaml.safe_dump(
                dict(config),
                handle,
                sort_keys=True,
                allow_unicode=False,
            )
    return snapshot_path

