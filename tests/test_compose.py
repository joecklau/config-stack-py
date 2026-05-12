from __future__ import annotations

from pathlib import Path

import pytest

from config_stack import ConfigStackError, compose_config_file


def test_compose_stack_layers_inline_payload_and_overrides(tmp_path: Path) -> None:
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "base.yaml").write_text(
        """
app:
  name: demo
  values:
    - base
nested:
  a: 1
""".lstrip(),
        encoding="utf-8",
    )
    (config_dir / "env.yaml").write_text(
        """
nested:
  b: 2
""".lstrip(),
        encoding="utf-8",
    )
    stack = config_dir / "config.stack.yaml"
    stack.write_text(
        """
kind: config.stack
layers:
  - base.yaml
  - env.yaml
inline: true
overrides:
  app:
    values:
      - override
  nested:
    a: 3
""".lstrip(),
        encoding="utf-8",
    )

    result = compose_config_file(stack)

    assert result.source_kind == "config.stack"
    assert result.config == {
        "app": {"name": "demo", "values": ["override"]},
        "inline": True,
        "nested": {"a": 3, "b": 2},
    }


def test_compose_document_supports_relative_extends(tmp_path: Path) -> None:
    (tmp_path / "parent.yaml").write_text(
        """
settings:
  a: 1
  b: parent
""".lstrip(),
        encoding="utf-8",
    )
    child = tmp_path / "child.yaml"
    child.write_text(
        """
extends: parent.yaml
settings:
  b: child
""".lstrip(),
        encoding="utf-8",
    )

    result = compose_config_file(child)

    assert result.config["settings"] == {"a": 1, "b": "child"}


def test_compose_document_detects_extends_cycles(tmp_path: Path) -> None:
    (tmp_path / "a.yaml").write_text("extends: b.yaml\n", encoding="utf-8")
    (tmp_path / "b.yaml").write_text("extends: a.yaml\n", encoding="utf-8")

    with pytest.raises(ConfigStackError, match="cycle"):
        compose_config_file(tmp_path / "a.yaml")


def test_compose_stack_can_expand_environment_values(tmp_path: Path) -> None:
    stack = tmp_path / "config.stack.yaml"
    stack.write_text(
        """
kind: config.stack
value: ${CONFIG_STACK_TEST_VALUE:-fallback}
""".lstrip(),
        encoding="utf-8",
    )

    result = compose_config_file(stack, expand_env=True)

    assert result.config["value"] == "fallback"

