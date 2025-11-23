from __future__ import annotations

from typing import List

import typer
from rich.console import Console
from rich.table import Table

from science_ops.utils.math_helpers import describe

app = typer.Typer(help="Basic statistics helpers.")
console = Console()


@app.command("describe")
def describe_cmd(
    values: List[float] = typer.Argument(..., help="Numeric values to summarize."),
) -> None:
    """Show count, mean, std, min, max, median."""
    stats = describe(values)
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Metric")
    table.add_column("Value")

    for k in ["count", "mean", "std", "min", "max", "median"]:
        table.add_row(k, f"{stats[k]:.6g}" if k != "count" else str(stats[k]))

    console.print(table)


@app.command("normal-pdf")
def normal_pdf(
    x: float = typer.Argument(..., help="Point at which to evaluate the PDF."),
    mu: float = typer.Option(0.0, "--mu", help="Mean of the distribution."),
    sigma: float = typer.Option(1.0, "--sigma", help="Standard deviation."),
) -> None:
    """Evaluate the normal distribution PDF at x."""
    import math

    if sigma <= 0:
        console.print("[red]Sigma must be positive.[/red]")
        raise typer.Exit(code=1)

    coeff = 1.0 / (sigma * math.sqrt(2 * math.pi))
    z = (x - mu) / sigma
    pdf = coeff * math.exp(-0.5 * z * z)
    console.print(f"pdf(x={x}, mu={mu}, sigma={sigma}) = [bold]{pdf:.10g}[/bold]")


@app.command("normal-cdf")
def normal_cdf(
    x: float = typer.Argument(..., help="Point at which to evaluate the CDF."),
    mu: float = typer.Option(0.0, "--mu", help="Mean of the distribution."),
    sigma: float = typer.Option(1.0, "--sigma", help="Standard deviation."),
) -> None:
    """Approximate the normal distribution CDF at x."""
    import math

    if sigma <= 0:
        console.print("[red]Sigma must be positive.[/red]")
        raise typer.Exit(code=1)

    z = (x - mu) / (sigma * math.sqrt(2.0))
    # Using error function erf
    cdf = 0.5 * (1.0 + math.erf(z))
    console.print(f"cdf(x={x}, mu={mu}, sigma={sigma}) = [bold]{cdf:.10g}[/bold]")
