from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="General lab calculations: dilutions, error, solution prep.")
console = Console()


@app.command("stock-dilution")
def stock_dilution(
    c_stock: float = typer.Argument(..., help="Stock concentration (same units as c_final)."),
    c_final: float = typer.Argument(..., help="Target concentration."),
    v_final: float = typer.Argument(..., help="Target final volume."),
) -> None:
    """
    Compute volume of stock needed to reach c_final in v_final (C1 V1 = C2 V2).
    """
    if c_stock <= 0 or c_final <= 0 or v_final <= 0:
        console.print("[red]All values must be positive.[/red]")
        raise typer.Exit(code=1)
    if c_final >= c_stock:
        console.print("[red]Target concentration must be less than stock concentration.[/red]")
        raise typer.Exit(code=1)
    v_stock = (c_final * v_final) / c_stock
    solvent = v_final - v_stock
    table = Table(title="Stock dilution", header_style="bold cyan")
    table.add_column("Quantity")
    table.add_column("Value")
    table.add_row("Stock volume", f"{v_stock:.6g}")
    table.add_row("Add solvent", f"{solvent:.6g}")
    console.print(table)


@app.command("percent-error")
def percent_error(
    measured: float = typer.Argument(..., help="Measured value."),
    true: float = typer.Argument(..., help="True/expected value."),
) -> None:
    """Percent error: (measured - true) / true * 100."""
    if true == 0:
        console.print("[red]True value cannot be zero for percent error.[/red]")
        raise typer.Exit(code=1)
    err = (measured - true) / true * 100.0
    console.print(f"Percent error = [bold]{err:.6g}%[/bold]")
