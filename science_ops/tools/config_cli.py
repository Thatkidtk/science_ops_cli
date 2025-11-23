from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from science_ops.config import load_config, save_config

app = typer.Typer(help="View and modify Science Ops configuration.")
console = Console()


@app.command("show")
def show_config() -> None:
    """Display current configuration values."""
    cfg = load_config()
    table = Table(title="Science Ops Config", header_style="bold cyan")
    table.add_column("Key")
    table.add_column("Value")

    table.add_row("notebook_path", str(cfg.notebook_path))
    table.add_row("default_body", str(cfg.default_body))
    table.add_row("color", str(cfg.color))

    console.print(table)


@app.command("set")
def set_config(
    key: str = typer.Argument(..., help="Config key: notebook_path, default_body, color"),
    value: str = typer.Argument(..., help="New value."),
) -> None:
    """Set a configuration value."""
    cfg = load_config()

    if key == "notebook_path":
        cfg.notebook_path = Path(value)
    elif key == "default_body":
        cfg.default_body = value or None
    elif key == "color":
        if value.lower() in ("1", "true", "yes", "on"):
            cfg.color = True
        elif value.lower() in ("0", "false", "no", "off"):
            cfg.color = False
        else:
            console.print("[red]color must be one of: true/false, yes/no, on/off, 1/0.[/red]")
            raise typer.Exit(code=1)
    else:
        console.print("[red]Unknown config key. Use: notebook_path, default_body, color.[/red]")
        raise typer.Exit(code=1)

    save_config(cfg)
    console.print(f"[green]Config updated:[/green] {key} = {value}")
    show_config()
