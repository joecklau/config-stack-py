# config-stack-py

[![Tests](https://github.com/joecklau/config-stack-py/actions/workflows/tests.yml/badge.svg)](https://github.com/joecklau/config-stack-py/actions/workflows/tests.yml)

`config-stack-py` is a small generic YAML/JSON/TOML config composition library.

It understands files, stack layers, recursive dictionary merge, final overrides,
relative paths, optional environment-variable expansion, and resolved snapshots.
It does not know about any consuming project's schema or runtime behavior.

## Example

```yaml
kind: config.stack
layers:
  - base.yaml
  - environment/dev.yaml
overrides:
  nested:
    threshold: 0.1
```

```python
from config_stack import compose_config_file

result = compose_config_file("config.stack.yaml")
resolved = result.config
```

## Dependency Model

During local development, consuming repositories can use an editable sibling
path dependency:

```toml
[project]
dependencies = [
    "config-stack-py>=0.1.0",
]

[tool.uv.sources]
config-stack-py = { path = "../config-stack-py", editable = true }
```

## Boundary

This package treats all non-control keys as ordinary data. Project-specific
schema validation belongs in the consuming project.

Generic control keys are:

- `kind`
- `schema_version`
- `extends`
- `layers`
- `overrides`
