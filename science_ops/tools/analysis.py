from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import typer
from rich.console import Console
from rich.table import Table

from science_ops.tools.data import _load_table, _extract_numeric_pairs

app = typer.Typer(help="Data analysis helpers: regression and uncertainty.")
console = Console()


def _regression_pairs(file: Path, xcol: str, ycol: str, delimiter: str | None) -> np.ndarray:
    headers, rows = _load_table(file, delimiter=delimiter)
    if xcol not in headers or ycol not in headers:
        console.print(f"[red]Columns not found. Available: {', '.join(headers)}[/red]")
        raise typer.Exit(code=1)
    pts = _extract_numeric_pairs(rows, xcol, ycol)
    if pts.shape[0] < 2:
        console.print("[red]Need at least 2 numeric pairs for regression.[/red]")
        raise typer.Exit(code=1)
    return pts


@app.command("regress")
def regress(
    file: Path = typer.Argument(..., exists=True, readable=True, help="Path to CSV/TSV file."),
    xcol: str = typer.Argument(..., help="Column for x values."),
    ycol: str = typer.Argument(..., help="Column for y values."),
    delimiter: str | None = typer.Option(None, "--delimiter", "-d", help="Optional delimiter override."),
) -> None:
    """
    Simple linear regression y = m x + b.
    Prints slope m, intercept b, r, r^2.
    """
    pts = _regression_pairs(file, xcol, ycol, delimiter)
    x = pts[:, 0]
    y = pts[:, 1]

    m, b = np.polyfit(x, y, 1)
    y_pred = m * x + b
    ss_res = float(np.sum((y - y_pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot != 0 else 0.0
    r = float(np.sqrt(r2)) if m >= 0 else -float(np.sqrt(r2))

    table = Table(title=f"Linear regression: {ycol} vs {xcol}", header_style="bold cyan")
    table.add_column("Metric")
    table.add_column("Value")
    table.add_row("slope (m)", f"{m:.6g}")
    table.add_row("intercept (b)", f"{b:.6g}")
    table.add_row("r", f"{r:.6g}")
    table.add_row("r^2", f"{r2:.6g}")
    console.print(table)


@app.command("uncertainty")
def uncertainty_combine(
    values: List[float] = typer.Argument(..., help="Uncertainties to combine (independent)."),
) -> None:
    """
    Combine independent uncertainties in quadrature:

        u_total = sqrt(u1^2 + u2^2 + ...)
    """
    if not values:
        console.print("[red]Provide at least one uncertainty value.[/red]")
        raise typer.Exit(code=1)
    arr = np.array(values, dtype=float)
    total = float(np.sqrt(np.sum(arr * arr)))
    console.print(f"Combined uncertainty = [bold]{total:.6g}[/bold]")
