from __future__ import annotations

import math

import typer
from rich.console import Console

from science_ops.utils.math_helpers import linspace

app = typer.Typer(help="Waveform generation and ASCII plotting.")
console = Console()


def _ascii_plot(y_values, height: int = 10) -> None:
    """Very simple ASCII plot centered around 0."""
    y_min = min(y_values)
    y_max = max(y_values)
    span = max(abs(y_min), abs(y_max))
    if span == 0:
        span = 1.0

    # Each line represents a y-level; 0 is in the middle.
    rows = []
    for y in y_values:
        # Map y in [-span, span] to position on line
        ratio = (y / (2 * span)) + 0.5  # [0,1]
        idx = int(ratio * (height - 1))
        rows.append(idx)

    # Build the vertical plot
    for level in reversed(range(height)):
        line_chars = []
        for idx in rows:
            if idx == level:
                line_chars.append("*")
            else:
                line_chars.append(" ")
        console.print("".join(line_chars))


@app.command("sine")
def sine(
    freq: float = typer.Option(1.0, "--freq", help="Frequency in arbitrary units."),
    samples: int = typer.Option(40, "--samples", help="Number of sample points."),
) -> None:
    """Generate a simple sine wave and draw it as ASCII."""
    t = linspace(0.0, 1.0, samples)
    y = [math.sin(2 * math.pi * freq * ti) for ti in t]
    _ascii_plot(y)


@app.command("square")
def square(
    freq: float = typer.Option(1.0, "--freq", help="Frequency in arbitrary units."),
    samples: int = typer.Option(40, "--samples", help="Number of sample points."),
    duty: float = typer.Option(0.5, "--duty", help="Duty cycle between 0 and 1."),
) -> None:
    """Generate a square wave and draw it as ASCII."""
    t = linspace(0.0, 1.0, samples)
    y = [
        1.0 if (freq * ti) % 1.0 < duty else -1.0
        for ti in t
    ]
    _ascii_plot(y)
