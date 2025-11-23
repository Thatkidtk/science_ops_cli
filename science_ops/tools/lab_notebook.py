from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from science_ops.config import load_config, save_config
from science_ops.utils.io import append_line, timestamp

app = typer.Typer(help="Simple lab notebook logging.")
console = Console()


@app.command("log")
def log_entry(
    text: str = typer.Argument(..., help="Note or observation to log."),
) -> None:
    """Append a timestamped entry to the lab notebook."""
    cfg = load_config()
    line = f"- [{timestamp()}] {text}"
    append_line(cfg.notebook_path, line)
    console.print(f"Logged to [green]{cfg.notebook_path}[/green]")


@app.command("show")
def show_notebook() -> None:
    """Print the current notebook contents."""
    cfg = load_config()
    try:
        content = cfg.notebook_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        console.print("[yellow]Notebook is empty (file not found).[/yellow]")
        return

    console.print(f"# Notebook: {cfg.notebook_path}\n")
    console.print(content)


@app.command("set-path")
def set_path(
    path: str = typer.Argument(..., help="New notebook path (file will be created on first write)."),
) -> None:
    """Change the notebook file path."""
    cfg = load_config()
    cfg.notebook_path = Path(path)
    save_config(cfg)
    console.print(f"Notebook path set to [green]{cfg.notebook_path}[/green]")
