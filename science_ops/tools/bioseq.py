from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from science_ops.tools.bio import CODON_TABLE, STOP_CODONS

app = typer.Typer(help="Bio sequence helpers with file support (FASTA/plain).")
console = Console()


def _read_sequence_from_file(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    seq_parts = []
    for line in lines:
        if line.startswith(">"):
            continue
        seq_parts.append(line.strip())
    seq = "".join(seq_parts).upper().replace(" ", "")
    return seq


def _gc_content(seq: str) -> float:
    if not seq:
        return 0.0
    valid = [b for b in seq if b in ("A", "C", "G", "T")]
    if not valid:
        return 0.0
    gc = sum(1 for b in valid if b in ("G", "C"))
    return gc / len(valid)


def _translate(seq: str, frame: int = 0) -> str:
    seq = seq.upper().replace(" ", "")
    protein = []
    for i in range(frame, len(seq) - 2, 3):
        codon = seq[i : i + 3]
        aa = CODON_TABLE.get(codon, "X")
        if aa in STOP_CODONS:
            break
        protein.append(aa)
    return "".join(protein)


@app.command("gc-file")
def gc_file(
    file: Path = typer.Argument(..., exists=True, readable=True, help="FASTA or plain sequence file."),
) -> None:
    """Compute GC content from a file."""
    seq = _read_sequence_from_file(file)
    if not seq:
        console.print("[red]No sequence data found.[/red]")
        raise typer.Exit(code=1)
    frac = _gc_content(seq)
    console.print(f"Length = {len(seq)}")
    console.print(f"GC fraction = [bold]{frac:.6g}[/bold]")


@app.command("translate-file")
def translate_file(
    file: Path = typer.Argument(..., exists=True, readable=True, help="FASTA or plain coding sequence."),
    frame: int = typer.Option(0, "--frame", min=0, max=2, help="Reading frame offset."),
) -> None:
    """Translate coding sequence from a file (stops at first stop codon)."""
    seq = _read_sequence_from_file(file)
    if not seq:
        console.print("[red]No sequence data found.[/red]")
        raise typer.Exit(code=1)
    protein = _translate(seq, frame=frame)
    console.print(f"Protein: [bold]{protein}[/bold]")
