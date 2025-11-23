from __future__ import annotations

from typing import Iterable

from rich.table import Table


def simple_table(title: str, columns: Iterable[str], header_style: str = "bold cyan") -> Table:
    """Create a Rich table with the given columns."""
    table = Table(title=title, header_style=header_style)
    for col in columns:
        table.add_column(col)
    return table
