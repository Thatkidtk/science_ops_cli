from __future__ import annotations

import math

import typer
from rich.console import Console

app = typer.Typer(help="Geometric optics tools: Snell's law, thin lens, mirrors.")
console = Console()


@app.command("snell")
def snell(
    n1: float = typer.Argument(..., help="Index of refraction of medium 1."),
    n2: float = typer.Argument(..., help="Index of refraction of medium 2."),
    theta1_deg: float = typer.Argument(..., help="Angle of incidence θ1 in degrees."),
) -> None:
    """
    Snell's law:

        n1 * sin(θ1) = n2 * sin(θ2)

    Reports θ2 and whether total internal reflection occurs.
    """
    if n1 <= 0 or n2 <= 0:
        console.print("[red]Indices of refraction must be positive.[/red]")
        raise typer.Exit(code=1)

    theta1_rad = math.radians(theta1_deg)
    sin_theta1 = math.sin(theta1_rad)
    ratio = n1 / n2
    sin_theta2 = ratio * sin_theta1

    if abs(sin_theta2) > 1.0:
        console.print("[yellow]Total internal reflection: no transmitted ray.[/yellow]")
        return

    theta2_rad = math.asin(sin_theta2)
    theta2_deg = math.degrees(theta2_rad)

    console.print(f"θ1 = {theta1_deg:.6g}°")
    console.print(f"θ2 = [bold]{theta2_deg:.6g}°[/bold]")


@app.command("thin-lens")
def thin_lens(
    f: float = typer.Argument(..., help="Focal length f (same units as distances)."),
    d_o: float = typer.Argument(..., help="Object distance d_o (positive if in front of lens)."),
) -> None:
    """
    Thin lens equation:

        1/f = 1/d_o + 1/d_i

    Reports image distance d_i and magnification m = -d_i / d_o.
    """
    if f == 0:
        console.print("[red]Focal length f cannot be zero.[/red]")
        raise typer.Exit(code=1)
    if d_o == 0:
        console.print("[red]Object distance d_o cannot be zero.[/red]")
        raise typer.Exit(code=1)

    denom = (1.0 / f) - (1.0 / d_o)
    if denom == 0:
        console.print("[yellow]Image at infinity (collimated output).[/yellow]")
        return

    d_i = 1.0 / denom
    m = -d_i / d_o

    image_type = "real" if d_i > 0 else "virtual"
    orientation = "inverted" if m < 0 else "upright"

    console.print(f"d_i = [bold]{d_i:.6g}[/bold] (image distance, {image_type})")
    console.print(f"m = [bold]{m:.6g}[/bold] (magnification, {orientation})")
