"""Load YAML configs from the project configs/ directory."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from city_value.paths import project_path


def load_yaml(name: str) -> dict[str, Any]:
    """Load `configs/<name>.yaml` (name without extension or with .yaml)."""
    filename = name if name.endswith((".yaml", ".yml")) else f"{name}.yaml"
    path: Path = project_path("configs", filename)
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Config {path} must be a mapping at the top level")
    return data
