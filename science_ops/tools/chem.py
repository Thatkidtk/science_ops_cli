from __future__ import annotations

import typer
from rich.console import Console

app = typer.Typer(help="Chemistry helpers: molarity and dilution.")
console = Console()


def calculate_molarity(moles: float, volume_l: float) -> float:
    if volume_l <= 0:
        raise ValueError("Volume must be positive.")
    return moles / volume_l


def calculate_dilution_final_volume(c1: float, v1_ml: float, c2: float) -> float:
    if any(v <= 0 for v in [c1, v1_ml, c2]):
        raise ValueError("Concentrations and volume must be positive.")
    if c2 >= c1:
        raise ValueError("Target concentration must be lower than the stock for dilution.")
    return (c1 * v1_ml) / c2


@app.command("molarity")
def molarity(
    moles: float = typer.Option(..., "--moles", "-n", help="Amount of solute in moles."),
    volume_l: float = typer.Option(..., "--volume-l", "-v", help="Solution volume in liters."),
) -> None:
    """Compute molarity (mol/L)."""
    try:
        m = calculate_molarity(moles, volume_l)
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc

    console.print(f"Molarity = [bold]{m:.6g} M[/bold] ({moles} mol in {volume_l} L)")


@app.command("dilute")
def dilute(
    c1: float = typer.Option(..., "--c1", help="Stock concentration (M)."),
    v1: float = typer.Option(..., "--v1", help="Stock volume to use (mL)."),
    c2: float = typer.Option(..., "--c2", help="Target concentration (M)."),
) -> None:
    """Dilution using C1 * V1 = C2 * V2."""
    try:
        v2 = calculate_dilution_final_volume(c1, v1, c2)
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc

    solvent = v2 - v1
    console.print(f"Final volume: [bold]{v2:.3f} mL[/bold]")
    console.print(f"Add solvent : [bold]{solvent:.3f} mL[/bold]")
    console.print("(Assuming ideal mixing; adjust for density/temperature if needed.)")
