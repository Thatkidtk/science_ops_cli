from __future__ import annotations

from pathlib import Path
from datetime import datetime


def append_line(path: Path, line: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(line.rstrip() + "\n")


def timestamp() -> str:
    return datetime.now().isoformat(timespec="seconds")
