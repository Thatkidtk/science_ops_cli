from __future__ import annotations

import math

import typer
from rich.console import Console

from .physics_constants import BODIES, get_body, C, G

app = typer.Typer(help="Relativity tools: time dilation, length contraction, energy.")
console = Console()


def _gamma_from_beta(beta: float) -> float:
    if beta < 0 or beta >= 1:
        raise ValueError("β must be in [0, 1).")
    return 1.0 / math.sqrt(1.0 - beta * beta)


@app.command("gamma")
def lorentz_gamma(
    v: float = typer.Argument(..., help="Velocity."),
    as_fraction_c: bool = typer.Option(
        True,
        "--fraction-c/--m-per-s",
        help="Interpret v as fraction of c (default) or as m/s.",
    ),
) -> None:
    """Compute Lorentz factor γ = 1 / sqrt(1 - v^2/c^2)."""
    if as_fraction_c:
        beta = v
    else:
        beta = v / C

    try:
        gamma = _gamma_from_beta(beta)
    except ValueError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(code=1)

    console.print(f"β = {beta:.6g}")
    console.print(f"γ = [bold]{gamma:.10g}[/bold]")


@app.command("time-dilation")
def time_dilation(
    proper_time: float = typer.Argument(..., help="Proper time interval Δτ (seconds)."),
    v: float = typer.Argument(..., help="Velocity."),
    as_fraction_c: bool = typer.Option(
        True,
        "--fraction-c/--m-per-s",
        help="Interpret v as fraction of c (default) or as m/s.",
    ),
) -> None:
    """
    Time dilation in special relativity:

        Δt = γ Δτ
    """
    if proper_time < 0:
        console.print("[red]Proper time must be non-negative.[/red]")
        raise typer.Exit(code=1)

    beta = v if as_fraction_c else v / C
    try:
        gamma = _gamma_from_beta(beta)
    except ValueError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(code=1)

    dilated = gamma * proper_time
    console.print(f"β = {beta:.6g}, γ = {gamma:.10g}")
    console.print(f"Δt = [bold]{dilated:.6g} s[/bold]")


@app.command("length-contraction")
def length_contraction(
    proper_length: float = typer.Argument(..., help="Proper length L0 (meters)."),
    v: float = typer.Argument(..., help="Velocity."),
    as_fraction_c: bool = typer.Option(
        True,
        "--fraction-c/--m-per-s",
        help="Interpret v as fraction of c (default) or as m/s.",
    ),
) -> None:
    """
    Length contraction:

        L = L0 / γ
    """
    if proper_length < 0:
        console.print("[red]Proper length must be non-negative.[/red]")
        raise typer.Exit(code=1)

    beta = v if as_fraction_c else v / C
    try:
        gamma = _gamma_from_beta(beta)
    except ValueError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(code=1)

    contracted = proper_length / gamma
    console.print(f"β = {beta:.6g}, γ = {gamma:.10g}")
    console.print(f"L = [bold]{contracted:.6g} m[/bold]")


@app.command("energy")
def relativistic_energy(
    mass: float = typer.Argument(..., help="Rest mass m (kg)."),
    v: float = typer.Argument(..., help="Velocity."),
    as_fraction_c: bool = typer.Option(
        True,
        "--fraction-c/--m-per-s",
        help="Interpret v as fraction of c (default) or as m/s.",
    ),
) -> None:
    """
    Relativistic energy:

        E = γ m c^2
        E_rest = m c^2
        K = (γ - 1) m c^2
    """
    if mass < 0:
        console.print("[red]Mass must be non-negative.[/red]")
        raise typer.Exit(code=1)

    beta = v if as_fraction_c else v / C
    try:
        gamma = _gamma_from_beta(beta)
    except ValueError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(code=1)

    mc2 = mass * C * C
    E = gamma * mc2
    K = (gamma - 1.0) * mc2

    console.print(f"β = {beta:.6g}, γ = {gamma:.10g}")
    console.print(f"E_rest = {mc2:.6g} J")
    console.print(f"E_total = [bold]{E:.6g} J[/bold]")
    console.print(f"Kinetic = [bold]{K:.6g} J[/bold]")


@app.command("grav-dilation")
def gravitational_time_dilation(
    mass: float | None = typer.Option(
        None, "--mass", help="Mass M creating field (kg). Use with --radius when not using --body."
    ),
    radius: float | None = typer.Option(
        None, "--radius", help="Radial distance r from center of mass (m). Use with --mass when not using --body."
    ),
    body: str | None = typer.Option(
        "earth",
        "--body",
        help=f"Preset body for mass/radius ({', '.join(sorted(BODIES))}). Use 'none' to disable presets.",
    ),
    altitude: float = typer.Option(
        0.0, "--altitude", help="Altitude above body surface (m) when using --body presets."
    ),
) -> None:
    """
    Gravitational time dilation (Schwarzschild, outside a non-rotating mass):

        dτ = dt * sqrt(1 - 2GM / (r c^2))

    Prints the factor f = dτ / dt.
    """
    mass_val = mass
    radius_val = radius

    if body and body.lower() != "none":
        try:
            data = get_body(body)
        except KeyError:
            console.print(f"[red]Unknown body '{body}'. Try: {', '.join(sorted(BODIES))}.[/red]")
            raise typer.Exit(code=1)
        mass_val = data["mass"]
        radius_val = data["radius"] + max(0.0, altitude)
    elif altitude:
        console.print("[red]--altitude requires a preset --body.[/red]")
        raise typer.Exit(code=1)

    if mass_val is None or radius_val is None:
        console.print("[red]Provide --body or both --mass and --radius.[/red]")
        raise typer.Exit(code=1)

    if mass_val <= 0 or radius_val <= 0:
        console.print("[red]Mass and radius must be positive.[/red]")
        raise typer.Exit(code=1)

    rs_over_r = 2 * G * mass_val / (radius_val * C * C)
    if rs_over_r >= 1:
        console.print("[red]r is at or inside the Schwarzschild radius; formula breaks.[/red]")
        raise typer.Exit(code=1)

    factor = math.sqrt(1.0 - rs_over_r)
    console.print(f"Using mass={mass_val:.6g} kg, r={radius_val:.6g} m")
    console.print(f"2GM/(r c^2) = {rs_over_r:.6g}")
    console.print(f"dτ/dt = [bold]{factor:.10g}[/bold] (proper time per far-away coordinate time)")
