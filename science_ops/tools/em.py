from __future__ import annotations

import math

import typer
from rich.console import Console

app = typer.Typer(help="Electromagnetism tools: Coulomb force and reactance helpers.")
console = Console()

COULOMB_CONSTANT = 8.9875517923e9  # N m^2 / C^2


@app.command("coulomb")
def coulomb_force(
    q1: float = typer.Argument(..., help="Charge 1 (Coulombs)."),
    q2: float = typer.Argument(..., help="Charge 2 (Coulombs)."),
    r: float = typer.Argument(..., help="Separation distance (meters)."),
) -> None:
    """
    Coulomb's law:

        F = k * |q1*q2| / r^2

    Reports magnitude and whether the force is attractive or repulsive.
    """
    if r <= 0:
        console.print("[red]Separation distance r must be positive.[/red]")
        raise typer.Exit(code=1)

    magnitude = COULOMB_CONSTANT * abs(q1 * q2) / (r * r)
    interaction = "repulsive" if q1 * q2 > 0 else "attractive"
    console.print(f"F = [bold]{magnitude:.6g} N[/bold] ({interaction})")


@app.command("reactance")
def reactance(
    freq: float = typer.Argument(..., help="Frequency (Hz)."),
    inductance: float = typer.Option(0.0, "--L", help="Inductance (H)."),
    capacitance: float = typer.Option(0.0, "--C", help="Capacitance (F)."),
) -> None:
    """
    Reactive impedances for inductors and capacitors in series:

        X_L = 2π f L
        X_C = -1 / (2π f C)
        X_total = X_L + X_C
    """
    if freq <= 0:
        console.print("[red]Frequency must be positive.[/red]")
        raise typer.Exit(code=1)
    if inductance <= 0 and capacitance <= 0:
        console.print("[red]Provide at least one of --L or --C (positive values).[/red]")
        raise typer.Exit(code=1)

    omega = 2 * math.pi * freq
    x_l = omega * inductance if inductance > 0 else 0.0
    x_c = -(1.0 / (omega * capacitance)) if capacitance > 0 else 0.0
    x_total = x_l + x_c

    console.print(f"X_L = {x_l:.6g} Ω")
    console.print(f"X_C = {x_c:.6g} Ω")
    console.print(f"X_total (series) = [bold]{x_total:.6g} Ω[/bold]")
