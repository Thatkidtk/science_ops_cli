from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

DEFAULT_CONFIG_NAME = "science_ops_config.json"


@dataclass
class Config:
    notebook_path: Path
    default_body: Optional[str] = None
    color: bool = True

    @classmethod
    def default(cls) -> "Config":
        config_dir = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config")) / "science_ops"
        config_dir.mkdir(parents=True, exist_ok=True)
        return cls(
            notebook_path=config_dir / "lab_notebook.md",
            default_body=None,
            color=True,
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

    base = Config.default()

    notebook_path = Path(data.get("notebook_path", base.notebook_path))
    default_body = data.get("default_body", base.default_body)
    color = bool(data.get("color", base.color))

    return Config(notebook_path=notebook_path, default_body=default_body, color=color)


def save_config(config: Config) -> None:
    cf = _config_file()
    data = {
        "notebook_path": str(config.notebook_path),
        "default_body": config.default_body,
        "color": config.color,
    }
    cf.write_text(json.dumps(data, indent=2))
