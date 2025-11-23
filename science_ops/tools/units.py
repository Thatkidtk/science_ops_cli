from __future__ import annotations

import typer
from rich.console import Console

app = typer.Typer(help="Unit conversion with simple dimensional analysis.")
console = Console()

# Very minimal; extend later.
# Model: dimension -> { unit_name: (scale_to_SI, symbol) }
DIMENSIONS = {
    "length": {
        "m": (1.0, "m"),
        "km": (1_000.0, "km"),
        "cm": (0.01, "cm"),
        "mm": (0.001, "mm"),
        "ft": (0.3048, "ft"),
        "in": (0.0254, "in"),
    },
    "time": {
        "s": (1.0, "s"),
        "min": (60.0, "min"),
        "h": (3600.0, "h"),
    },
    "mass": {
        "kg": (1.0, "kg"),
        "g": (0.001, "g"),
        "lb": (0.45359237, "lb"),
    },
    "velocity": {
        "m/s": (1.0, "m/s"),
        "km/h": (1000.0 / 3600.0, "km/h"),
        "mph": (0.44704, "mph"),
    },
    "pressure": {
        "Pa": (1.0, "Pa"),
        "kPa": (1_000.0, "kPa"),
        "bar": (100_000.0, "bar"),
        "atm": (101_325.0, "atm"),
    },
}


def find_dimension(unit: str) -> str | None:
    for dim, table in DIMENSIONS.items():
        if unit in table:
            return dim
    return None


@app.command("list-dimensions")
def list_dimensions() -> None:
    """List known dimensions and their units."""
    for dim, table in DIMENSIONS.items():
        units = ", ".join(table.keys())
        console.print(f"[cyan]{dim}[/cyan]: {units}")


@app.command("convert")
def convert(
    value: float = typer.Argument(..., help="Numeric value to convert."),
    from_unit: str = typer.Argument(..., help="Source unit, e.g. 'm/s'."),
    to_unit: str = typer.Argument(..., help="Target unit, e.g. 'km/h'."),
) -> None:
    """Convert a value between compatible units."""
    from_dim = find_dimension(from_unit)
    to_dim = find_dimension(to_unit)

    if from_dim is None:
        console.print(f"[red]Unknown unit: {from_unit}[/red]")
        raise typer.Exit(code=1)
    if to_dim is None:
        console.print(f"[red]Unknown unit: {to_unit}[/red]")
        raise typer.Exit(code=1)
    if from_dim != to_dim:
        console.print(
            f"[red]Incompatible units: '{from_unit}' ({from_dim}) vs '{to_unit}' ({to_dim}).[/red]"
        )
        raise typer.Exit(code=1)

    scale_from, _ = DIMENSIONS[from_dim][from_unit]
    scale_to, _ = DIMENSIONS[to_dim][to_unit]

    # value_in_SI = value * scale_from
    # value_target = value_in_SI / scale_to
    value_SI = value * scale_from
    value_target = value_SI / scale_to

    console.print(f"{value} {from_unit} = [bold]{value_target:.6g} {to_unit}[/bold]")
