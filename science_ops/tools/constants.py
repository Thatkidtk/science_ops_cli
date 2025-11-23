from __future__ import annotations

import typer
from rich.table import Table
from rich.console import Console

app = typer.Typer(help="Physical constants: search and list commonly used values.")

console = Console()

# Very small starter set — you can expand this later or pull from a JSON file.
CONSTANTS = {
    "c": {
        "name": "Speed of light in vacuum",
        "symbol": "c",
        "value": 2.99792458e8,
        "unit": "m/s",
        "reference": "CODATA 2018",
    },
    "h": {
        "name": "Planck constant",
        "symbol": "h",
        "value": 6.62607015e-34,
        "unit": "J·s",
        "reference": "CODATA 2018",
    },
    "kb": {
        "name": "Boltzmann constant",
        "symbol": "k_B",
        "value": 1.380649e-23,
        "unit": "J/K",
        "reference": "CODATA 2018",
    },
    "na": {
        "name": "Avogadro constant",
        "symbol": "N_A",
        "value": 6.02214076e23,
        "unit": "1/mol",
        "reference": "CODATA 2018",
    },
}


@app.command("list")
def list_constants() -> None:
    """List available constants."""
    table = Table(title="Physical Constants")
    table.add_column("Key", style="cyan", no_wrap=True)
    table.add_column("Name")
    table.add_column("Symbol", style="magenta")
    table.add_column("Value")
    table.add_column("Unit")
    table.add_column("Reference", style="green")

    for key, c in CONSTANTS.items():
        table.add_row(
            key,
            c["name"],
            c["symbol"],
            f"{c['value']:.6g}",
            c["unit"],
            c["reference"],
        )

    console.print(table)


@app.command("get")
def get_constant(query: str = typer.Argument(..., help="Key or name fragment.")) -> None:
    """Get information about a constant by key or fuzzy name match."""
    query_lower = query.lower()

    # Exact key first
    if query_lower in CONSTANTS:
        c = CONSTANTS[query_lower]
        console.print(f"[cyan]{query_lower}[/cyan] - {c['name']}")
        console.print(f"Symbol   : {c['symbol']}")
        console.print(f"Value    : {c['value']:.10g} {c['unit']}")
        console.print(f"Ref      : {c['reference']}")
        return

    # Fuzzy match by name or symbol
    matches = {
        key: c
        for key, c in CONSTANTS.items()
        if query_lower in c["name"].lower() or query_lower in c["symbol"].lower()
    }

    if not matches:
        console.print(f"[red]No constants matched '{query}'.[/red]")
        raise typer.Exit(code=1)

    for key, c in matches.items():
        console.print(f"[cyan]{key}[/cyan] - {c['name']} ({c['symbol']}) = {c['value']:.10g} {c['unit']}")
