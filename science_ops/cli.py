from __future__ import annotations

import typer
from rich.console import Console

from . import __version__
from .tools import constants, units, stats, waves, lab_notebook, astro, chem, mech, relativity, bio

app = typer.Typer(
    help="Science Ops CLI — a terminal Swiss army knife for scientists and mathematicians."
)
console = Console()


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


# Mount sub-apps
app.add_typer(constants.app, name="constants")
app.add_typer(units.app, name="units")
app.add_typer(stats.app, name="stats")
app.add_typer(waves.app, name="waves")
app.add_typer(lab_notebook.app, name="notebook")
app.add_typer(astro.app, name="astro")
app.add_typer(chem.app, name="chem")
app.add_typer(mech.app, name="mech")
app.add_typer(relativity.app, name="relativity")
app.add_typer(bio.app, name="bio")


if __name__ == "__main__":
    app()
