from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import typer
from rich.console import Console
from rich.table import Table

from science_ops.utils.math_helpers import describe

app = typer.Typer(help="Quick data exploration for CSV/TSV files.")
console = Console()


def _load_table(path: Path, delimiter: str | None = None) -> Tuple[List[str], List[Dict[str, str]]]:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    # Guess delimiter: default comma, fallback to tab if no commas
    text = path.read_text(encoding="utf-8", errors="ignore")
    if delimiter is None:
        delimiter = "\t" if ("," not in text and "\t" in text) else ","

    reader = csv.DictReader(text.splitlines(), delimiter=delimiter)
    rows = list(reader)
    if not rows:
        raise ValueError("File appears to be empty or has no data rows.")
    headers = reader.fieldnames or []
    return headers, rows


def _extract_numeric_column(rows: List[Dict[str, str]], col: str) -> np.ndarray:
    values: List[float] = []
    for r in rows:
        raw = r.get(col, "").strip()
        if raw == "":
            continue
        try:
            values.append(float(raw))
        except ValueError:
            # Non-numeric entries are skipped
            continue
    return np.array(values, dtype=float)


@app.command("summarize")
def summarize(
    file: Path = typer.Argument(..., exists=True, readable=True, help="Path to CSV/TSV file."),
    delimiter: str | None = typer.Option(None, "--delimiter", "-d", help="Optional delimiter override."),
) -> None:
    """
    Compute descriptive statistics for each numeric column in a CSV/TSV file.
    """
    headers, rows = _load_table(file, delimiter=delimiter)

    table = Table(title=f"Summary: {file}", header_style="bold cyan")
    table.add_column("Column")
    table.add_column("Count")
    table.add_column("Mean")
    table.add_column("Std")
    table.add_column("Min")
    table.add_column("Max")
    table.add_column("Median")

    any_numeric = False

    for col in headers:
        data = _extract_numeric_column(rows, col)
        if data.size == 0:
            continue
        any_numeric = True
        stats = describe(data)
        table.add_row(
            col,
            str(stats["count"]),
            f"{stats['mean']:.6g}",
            f"{stats['std']:.6g}",
            f"{stats['min']:.6g}",
            f"{stats['max']:.6g}",
            f"{stats['median']:.6g}",
        )

    if not any_numeric:
        console.print("[yellow]No numeric columns detected.[/yellow]")
        return

    console.print(table)


@app.command("head")
def head(
    file: Path = typer.Argument(..., exists=True, readable=True, help="Path to CSV/TSV file."),
    rows: int = typer.Option(5, "--rows", "-n", help="Number of rows to show."),
    delimiter: str | None = typer.Option(None, "--delimiter", "-d", help="Optional delimiter override."),
) -> None:
    """
    Display the first N rows of a CSV/TSV file.
    """
    headers, data_rows = _load_table(file, delimiter=delimiter)
    rows = max(1, rows)

    table = Table(title=f"Head: {file}", header_style="bold cyan", show_lines=False)
    for h in headers:
        table.add_column(h)

    for r in data_rows[:rows]:
        table.add_row(*(r.get(h, "") for h in headers))

    console.print(table)


@app.command("hist")
def hist(
    file: Path = typer.Argument(..., exists=True, readable=True, help="Path to CSV/TSV file."),
    column: str = typer.Argument(..., help="Column name to histogram."),
    bins: int = typer.Option(10, "--bins", help="Number of histogram bins."),
    width: int = typer.Option(40, "--width", help="Histogram bar width (characters)."),
    delimiter: str | None = typer.Option(None, "--delimiter", "-d", help="Optional delimiter override."),
) -> None:
    """
    ASCII histogram of a numeric column in a CSV/TSV file.
    """
    headers, rows = _load_table(file, delimiter=delimiter)
    if column not in headers:
        console.print(f"[red]Column '{column}' not found. Available: {', '.join(headers)}[/red]")
        raise typer.Exit(code=1)

    data = _extract_numeric_column(rows, column)
    if data.size == 0:
        console.print(f"[yellow]Column '{column}' has no numeric data.[/yellow]")
        raise typer.Exit(code=1)

    hist, edges = np.histogram(data, bins=bins)
    max_count = max(hist) if hist.size else 1

    console.print(f"Histogram for [bold]{column}[/bold] ({data.size} values):")
    for count, left, right in zip(hist, edges[:-1], edges[1:]):
        bar_len = int((count / max_count) * width) if max_count > 0 else 0
        bar = "*" * bar_len
        console.print(f"{left: .4g} – {right: .4g} | {bar} ({count})")
