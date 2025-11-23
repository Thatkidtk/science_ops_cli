from pathlib import Path

from typer.testing import CliRunner

from science_ops.cli import app

runner = CliRunner()


def _make_fasta(tmp_path: Path) -> Path:
    p = tmp_path / "seq.fa"
    p.write_text(">test\nATGGCC\n", encoding="utf-8")
    return p


def test_bioseq_gc_file(tmp_path):
    f = _make_fasta(tmp_path)
    result = runner.invoke(app, ["bioseq", "gc-file", str(f)])
    assert result.exit_code == 0
    assert "GC fraction" in result.stdout


def test_bioseq_translate_file(tmp_path):
    f = _make_fasta(tmp_path)
    result = runner.invoke(app, ["bioseq", "translate-file", str(f)])
    assert result.exit_code == 0
    assert "Protein" in result.stdout
