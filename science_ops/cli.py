from __future__ import annotations

import typer
from rich.console import Console

from . import __version__
from .tools import (
    constants,
    units,
    stats,
    waves,
    lab_notebook,
    astro,
    chem,
    mech,
    relativity,
    bio,
    data,
    optics,
    em,
    config_cli,
)

app = typer.Typer(
    help="Science Ops CLI — a terminal Swiss army knife for scientists and mathematicians."
)
console = Console()
_subapps: list[tuple[str, typer.Typer]] = []


@app.callback()
def main(
    version: bool = typer.Option(
        False, "--version", "-v", help="Show version and exit.", is_eager=True
    )
) -> None:
    """Science Ops CLI entrypoint."""
    if version:
        console.print(f"Science Ops CLI version [bold]{__version__}[/bold]")
        raise typer.Exit()


def _register(subapp: typer.Typer, name: str) -> None:
    app.add_typer(subapp, name=name)
    _subapps.append((name, subapp))


# Mount sub-apps
_register(constants.app, "constants")
_register(units.app, "units")
_register(stats.app, "stats")
_register(waves.app, "waves")
_register(lab_notebook.app, "notebook")
_register(astro.app, "astro")
_register(chem.app, "chem")
_register(mech.app, "mech")
_register(relativity.app, "relativity")
_register(bio.app, "bio")
_register(data.app, "data")
_register(optics.app, "optics")
_register(em.app, "em")
_register(config_cli.app, "config")


@app.command("help-all")
def help_all() -> None:
    """
    Show all subcommands and their short help strings.
    """
    console.print("[bold]Science Ops CLI command index[/bold]\n")
    for name, sub in _subapps:
        help_text = getattr(getattr(sub, "info", None), "help", "") or ""
        console.print(f"[cyan]{name}[/cyan]: {help_text}")


if __name__ == "__main__":
    app()
