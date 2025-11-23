from __future__ import annotations

import math
import typer
from rich.console import Console

from science_ops.utils.display import simple_table
from .physics_constants import BODIES, get_body

app = typer.Typer(help="Classical mechanics tools: projectiles, work, energy, orbits.")
console = Console()

DEFAULT_BODY = "earth"
DEFAULT_G = BODIES[DEFAULT_BODY]["g"]
DEFAULT_MU = BODIES[DEFAULT_BODY]["mu"]


@app.command("projectile")
def projectile_motion(
    v0: float = typer.Argument(..., help="Initial speed (m/s)."),
    angle_deg: float = typer.Argument(..., help="Launch angle above horizontal (degrees)."),
    y0: float = typer.Option(0.0, "--y0", help="Initial height (m)."),
    g: float = typer.Option(DEFAULT_G, "--g", help="Gravitational acceleration (m/s^2)."),
    body: str | None = typer.Option(
        None, "--body", help=f"Preset surface gravity body ({', '.join(sorted(BODIES))}). Overrides --g."
    ),
) -> None:
    """
    Simple projectile motion in a uniform gravitational field (no drag).

    Assumptions:
    - Flat Earth approximation
    - No air resistance
    - Constant g
    """
    if body:
        try:
            g = get_body(body)["g"]
        except KeyError:
            console.print(f"[red]Unknown body '{body}'. Try: {', '.join(sorted(BODIES))}.[/red]")
            raise typer.Exit(code=1)

    theta = math.radians(angle_deg)
    vx0 = v0 * math.cos(theta)
    vy0 = v0 * math.sin(theta)

    # Time of flight (quadratic in y)
    # y(t) = y0 + vy0 t - 0.5 g t^2
    # 0 = y0 + vy0 t - 0.5 g t^2
    a = -0.5 * g
    b = vy0
    c = y0

    disc = b * b - 4 * a * c
    if disc < 0:
        console.print("[red]No real impact time (object never reaches y=0).[/red]")
        raise typer.Exit(code=1)

    t1 = (-b + math.sqrt(disc)) / (2 * a)
    t2 = (-b - math.sqrt(disc)) / (2 * a)
    t_flight = max(t1, t2)

    # Max height at vy=0: t = vy0/g
    t_peak = vy0 / g if g != 0 else 0.0
    y_max = y0 + vy0 * t_peak - 0.5 * g * t_peak * t_peak

    range_x = vx0 * t_flight

    table = simple_table("Projectile Motion (no drag)", ["Quantity", "Value"])
    table.add_row("Time of flight", f"{t_flight:.4g} s")
    table.add_row("Horizontal range", f"{range_x:.4g} m")
    table.add_row("Maximum height", f"{y_max:.4g} m")
    table.add_row("vx0", f"{vx0:.4g} m/s")
    table.add_row("vy0", f"{vy0:.4g} m/s")
    console.print(table)


@app.command("work")
def work_done(
    force: float = typer.Argument(..., help="Force magnitude (N)."),
    distance: float = typer.Argument(..., help="Displacement magnitude (m)."),
    angle_deg: float = typer.Option(
        0.0,
        "--angle",
        help="Angle between force and displacement (degrees). 0° = same direction.",
    ),
) -> None:
    """Compute mechanical work: W = F * d * cos(theta)."""
    theta = math.radians(angle_deg)
    work = force * distance * math.cos(theta)
    console.print(f"W = [bold]{work:.6g} J[/bold]")


@app.command("power")
def power_from_work(
    work: float = typer.Argument(..., help="Work done (J)."),
    time_s: float = typer.Argument(..., help="Time interval (s)."),
) -> None:
    """Compute average power: P = W / Δt."""
    if time_s <= 0:
        console.print("[red]Time must be positive.[/red]")
        raise typer.Exit(code=1)
    p = work / time_s
    console.print(f"P = [bold]{p:.6g} W[/bold]")


@app.command("pendulum")
def simple_pendulum(
    length: float = typer.Argument(..., help="Pendulum length (m)."),
    g: float = typer.Option(DEFAULT_G, "--g", help="Gravitational acceleration (m/s^2)."),
    body: str | None = typer.Option(
        None, "--body", help=f"Preset surface gravity body ({', '.join(sorted(BODIES))}). Overrides --g."
    ),
) -> None:
    """
    Small-angle approximation period for a simple pendulum:

    T = 2π * sqrt(L / g)
    """
    if body:
        try:
            g = get_body(body)["g"]
        except KeyError:
            console.print(f"[red]Unknown body '{body}'. Try: {', '.join(sorted(BODIES))}.[/red]")
            raise typer.Exit(code=1)

    if length <= 0:
        console.print("[red]Length must be > 0 m.[/red]")
        raise typer.Exit(code=1)
    if g <= 0:
        console.print("[red]g must be > 0 m/s^2.[/red]")
        raise typer.Exit(code=1)

    T = 2 * math.pi * math.sqrt(length / g)
    console.print(f"T = [bold]{T:.6g} s[/bold]")


@app.command("orbit-period")
def orbit_period(
    semi_major_axis: float = typer.Argument(..., help="Semi-major axis a (m)."),
    mu: float = typer.Option(
        DEFAULT_MU,
        "--mu",
        help="Standard gravitational parameter μ = GM (m^3/s^2). Default = Earth.",
    ),
    body: str | None = typer.Option(
        None, "--body", help=f"Preset central body for μ ({', '.join(sorted(BODIES))}). Overrides --mu."
    ),
) -> None:
    """
    Orbital period for a Keplerian two-body orbit:

        T = 2π * sqrt(a^3 / μ)
    """
    if body:
        try:
            mu = get_body(body)["mu"]
        except KeyError:
            console.print(f"[red]Unknown body '{body}'. Try: {', '.join(sorted(BODIES))}.[/red]")
            raise typer.Exit(code=1)

    if semi_major_axis <= 0:
        console.print("[red]Semi-major axis must be > 0 m.[/red]")
        raise typer.Exit(code=1)
    if mu <= 0:
        console.print("[red]μ must be > 0 m^3/s^2.[/red]")
        raise typer.Exit(code=1)

    T = 2 * math.pi * math.sqrt(semi_major_axis ** 3 / mu)
    console.print(f"T = [bold]{T:.6g} s[/bold]")
