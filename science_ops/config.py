from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

DEFAULT_CONFIG_NAME = "science_ops_config.json"


@dataclass
class Config:
    notebook_path: Path

    @classmethod
    def default(cls) -> "Config":
        config_dir = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config")) / "science_ops"
        config_dir.mkdir(parents=True, exist_ok=True)
        return cls(
            notebook_path=config_dir / "lab_notebook.md",
        )


def _config_file() -> Path:
    config_dir = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config")) / "science_ops"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / DEFAULT_CONFIG_NAME


def load_config() -> Config:
    cf = _config_file()
    if not cf.exists():
        return Config.default()

    try:
        data: Dict[str, Any] = json.loads(cf.read_text())
    except json.JSONDecodeError:
        return Config.default()

    notebook_path = Path(data.get("notebook_path", Config.default().notebook_path))
    return Config(notebook_path=notebook_path)


def save_config(config: Config) -> None:
    cf = _config_file()
    data = {
        "notebook_path": str(config.notebook_path),
    }
    cf.write_text(json.dumps(data, indent=2))
