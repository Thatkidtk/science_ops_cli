from __future__ import annotations

from collections import Counter
from typing import Dict, Tuple

import typer
from rich.console import Console

from science_ops.utils.display import simple_table

app = typer.Typer(help="Genetics & population biology tools.")
console = Console()


# --- Hardy–Weinberg ---------------------------------------------------------


@app.command("hardy-weinberg")
def hardy_weinberg(
    p: float = typer.Option(
        None,
        "--p",
        help="Allele A frequency p. If omitted, will be estimated from genotype counts.",
    ),
    aa: int = typer.Option(0, "--aa", help="Count of genotype AA."),
    ab: int = typer.Option(0, "--ab", help="Count of genotype AB."),
    bb: int = typer.Option(0, "--bb", help="Count of genotype BB."),
) -> None:
    """
    Hardy–Weinberg equilibrium calculator.

    If p is not provided, it's estimated from genotype counts as:

        p_hat = (2*AA + AB) / (2N)
        q_hat = 1 - p_hat

    Then expected genotype frequencies in HW equilibrium are:

        AA: p^2
        AB: 2pq
        BB: q^2
    """
    # If no counts and no p, bail.
    if p is None and (aa + ab + bb) == 0:
        console.print("[red]Provide either p or genotype counts.[/red]")
        raise typer.Exit(code=1)

    if p is not None:
        if not (0.0 <= p <= 1.0):
            console.print("[red]p must be between 0 and 1.[/red]")
            raise typer.Exit(code=1)
        q = 1.0 - p
    else:
        N = aa + ab + bb
        if N == 0:
            console.print("[red]Total count is zero.[/red]")
            raise typer.Exit(code=1)
        p = (2 * aa + ab) / (2.0 * N)
        q = 1.0 - p
        console.print(f"Estimated p = {p:.6g}, q = {q:.6g} from genotype counts.")

    # Expected frequencies
    p2 = p * p
    q2 = q * q
    two_pq = 2.0 * p * q

    table = simple_table("Hardy–Weinberg equilibrium", ["Genotype", "Expected frequency"])

    table.add_row("AA", f"{p2:.6g}")
    table.add_row("AB", f"{two_pq:.6g}")
    table.add_row("BB", f"{q2:.6g}")

    console.print(table)

    # If user gave counts, compare observed vs expected
    if (aa + ab + bb) > 0:
        N = aa + ab + bb
        obs_AA = aa / N
        obs_AB = ab / N
        obs_BB = bb / N

        table2 = simple_table(
            "Observed vs expected (frequencies)",
            ["Genotype", "Observed", "Expected"],
            header_style="bold magenta",
        )

        table2.add_row("AA", f"{obs_AA:.6g}", f"{p2:.6g}")
        table2.add_row("AB", f"{obs_AB:.6g}", f"{two_pq:.6g}")
        table2.add_row("BB", f"{obs_BB:.6g}", f"{q2:.6g}")

        console.print(table2)


# --- Punnett squares --------------------------------------------------------


def _normalize_genotype(gen: str) -> Tuple[str, str]:
    gen = gen.strip()
    if len(gen) != 2:
        raise ValueError("Genotype must be 2 characters, e.g. 'Aa' or 'aa'.")
    return gen[0], gen[1]


@app.command("punnett")
def punnett(
    parent1: str = typer.Argument(..., help="Genotype for parent 1 (e.g. 'Aa')."),
    parent2: str = typer.Argument(..., help="Genotype for parent 2 (e.g. 'Aa')."),
) -> None:
    """
    Single-locus Punnett square.

    Assumes a diploid organism and 2-character genotypes (e.g. Aa, AA, aa).
    """
    try:
        a1, a2 = _normalize_genotype(parent1)
        b1, b2 = _normalize_genotype(parent2)
    except ValueError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(code=1)

    gametes1 = [a1, a2]
    gametes2 = [b1, b2]

    offspring: Counter[str] = Counter()
    total = 0

    for g1 in gametes1:
        for g2 in gametes2:
            child = "".join(sorted([g1, g2]))  # sort so 'Aa' == 'aA'
            offspring[child] += 1
            total += 1

    table = simple_table("Punnett square outcome", ["Genotype", "Probability"])

    for genotype, count in sorted(offspring.items()):
        prob = count / total
        table.add_row(genotype, f"{prob:.6g}")

    console.print(table)


# --- Sequence utilities -----------------------------------------------------


CODON_TABLE: Dict[str, str] = {
    # Standard genetic code (64 codons)
    "TTT": "F", "TTC": "F", "TTA": "L", "TTG": "L",
    "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S",
    "TAT": "Y", "TAC": "Y", "TAA": "*", "TAG": "*",
    "TGT": "C", "TGC": "C", "TGA": "*", "TGG": "W",
    "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
    "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "CAT": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
    "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "ATT": "I", "ATC": "I", "ATA": "I", "ATG": "M",
    "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "AAT": "N", "AAC": "N", "AAA": "K", "AAG": "K",
    "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R",
    "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
    "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E",
    "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
}

START_CODONS = {"ATG"}
STOP_CODONS = {"TAA", "TAG", "TGA"}


@app.command("gc-content")
def gc_content(
    sequence: str = typer.Argument(..., help="DNA sequence (A/C/G/T)."),
) -> None:
    """Compute GC content (fraction of G or C bases) of a DNA sequence."""
    seq = sequence.upper().replace(" ", "")
    if not seq:
        console.print("[red]Empty sequence.[/red]")
        raise typer.Exit(code=1)

    valid = set("ACGT")
    invalid = set(seq) - valid
    if invalid:
        console.print(f"[yellow]Warning: ignoring invalid characters: {''.join(sorted(invalid))}[/yellow]")
        seq = "".join(ch for ch in seq if ch in valid)
        if not seq:
            console.print("[red]No valid bases left after filtering.[/red]")
            raise typer.Exit(code=1)

    total = len(seq)
    gc = sum(1 for b in seq if b in ("G", "C"))
    frac = gc / total

    console.print(f"Length = {total}")
    console.print(f"GC count = {gc}")
    console.print(f"GC fraction = [bold]{frac:.6g}[/bold]")


@app.command("translate")
def translate_dna(
    sequence: str = typer.Argument(..., help="DNA coding sequence (5'→3')."),
    stop_at_stop: bool = typer.Option(
        True,
        "--stop-at-stop/--read-through",
        help="Stop translation at first stop codon (default) or include '*' in output.",
    ),
    frame: int = typer.Option(
        0, "--frame", min=0, max=2, help="Reading frame offset (0, 1, or 2)."
    ),
    orf_only: bool = typer.Option(
        False,
        "--orf-only/--full-sequence",
        help="Start at first ATG in-frame and stop at stop codon.",
    ),
) -> None:
    """
    Translate DNA sequence into a protein sequence using a simple codon table.

    Any incomplete codon at the end is ignored.
    """
    seq = sequence.upper().replace(" ", "").replace("\n", "")
    if not seq:
        console.print("[red]Empty sequence.[/red]")
        raise typer.Exit(code=1)

    if frame not in (0, 1, 2):
        console.print("[red]Frame must be 0, 1, or 2.[/red]")
        raise typer.Exit(code=1)

    start_index = frame
    if orf_only:
        idx = seq.find("ATG", frame)
        if idx == -1 or (idx - frame) % 3 != 0:
            console.print("[red]No in-frame start codon (ATG) found from the chosen frame.[/red]")
            raise typer.Exit(code=1)
        start_index = idx

    protein = []
    for i in range(start_index, len(seq) - 2, 3):
        codon = seq[i:i+3]
        aa = CODON_TABLE.get(codon, "X")  # X = unknown/invalid
        if aa == "*" and stop_at_stop:
            break
        protein.append(aa)

    prot_str = "".join(protein)
    console.print(f"Protein: [bold]{prot_str}[/bold]")


@app.command("find-orfs")
def find_orfs(
    sequence: str = typer.Argument(..., help="DNA sequence (A/C/G/T)."),
    min_aa: int = typer.Option(30, "--min-aa", help="Minimum amino-acid length to report."),
    frames: str = typer.Option("1,2,3", "--frames", help="Comma-separated frames to scan (subset of 1,2,3)."),
    stop_at_stop: bool = typer.Option(
        True,
        "--stop-at-stop/--read-through",
        help="Stop ORF at first in-frame stop (default) or include '*' in protein.",
    ),
) -> None:
    """
    Scan DNA sequence for open reading frames across one or more frames.

    - Frames numbered 1,2,3 correspond to offsets 0,1,2.
    - ORFs start at ATG and end at the first in-frame stop (or continue if --read-through).
    """
    seq = sequence.upper().replace(" ", "").replace("\n", "")
    if not seq:
        console.print("[red]Empty sequence.[/red]")
        raise typer.Exit(code=1)

    valid = set("ACGT")
    invalid = set(seq) - valid
    if invalid:
        console.print(f"[yellow]Warning: ignoring invalid characters: {''.join(sorted(invalid))}[/yellow]")
        seq = "".join(ch for ch in seq if ch in valid)
        if not seq:
            console.print("[red]No valid bases left after filtering.[/red]")
            raise typer.Exit(code=1)

    try:
        frame_list = sorted({int(f.strip()) for f in frames.split(",") if f.strip()})
    except ValueError:
        console.print("[red]Frames must be a comma-separated list of 1, 2, 3.[/red]")
        raise typer.Exit(code=1)
    if any(f not in (1, 2, 3) for f in frame_list):
        console.print("[red]Frames must be among 1, 2, 3.[/red]")
        raise typer.Exit(code=1)

    orfs: list[tuple[int, int, int, str]] = []

    for frame in frame_list:
        offset = frame - 1
        i = offset
        while i <= len(seq) - 3:
            codon = seq[i:i+3]
            if codon in START_CODONS:
                j = i
                aa_seq = []
                while j <= len(seq) - 3:
                    c = seq[j:j+3]
                    aa = CODON_TABLE.get(c, "X")
                    if c in STOP_CODONS:
                        if stop_at_stop:
                            break
                        aa_seq.append("*")
                    else:
                        aa_seq.append(aa)
                    j += 3
                aa_str = "".join(aa_seq)
                if len(aa_str) >= min_aa:
                    start_nt = i + 1  # 1-based inclusive
                    end_nt = j if stop_at_stop else min(len(seq), j)
                    orfs.append((frame, start_nt, end_nt, aa_str))
                i += 3
            else:
                i += 3

    if not orfs:
        console.print(f"[yellow]No ORFs found with length >= {min_aa} aa in frames {frame_list}.[/yellow]")
        return

    table = simple_table(f"ORFs (min length {min_aa} aa)", ["Frame", "Start nt", "End nt", "AA length", "Protein"])
    for frame, start_nt, end_nt, aa_str in orfs:
        preview = (aa_str[:30] + "...") if len(aa_str) > 30 else aa_str
        table.add_row(str(frame), str(start_nt), str(end_nt), str(len(aa_str)), preview)

    console.print(table)
