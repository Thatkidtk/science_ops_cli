from typer.testing import CliRunner

from science_ops.cli import app

runner = CliRunner()


def test_bio_gc_content_cli():
    result = runner.invoke(app, ["bio", "gc-content", "GCGC"])
    assert result.exit_code == 0
    assert "GC fraction" in result.stdout


def test_bio_translate_orf_only():
    result = runner.invoke(app, ["bio", "translate", "CCCATGGGGTAA", "--orf-only"])
    assert result.exit_code == 0
    assert "Protein" in result.stdout


def test_bio_translate_invalid_frame():
    result = runner.invoke(app, ["bio", "translate", "ATG", "--frame", "3"])
    assert result.exit_code != 0
    assert "range" in result.stdout or "Frame must" in result.stdout


def test_bio_find_orfs():
    seq = "CCCATGGGGTAA"  # one short ORF (ATG->TAA) of length 3 aa
    result = runner.invoke(app, ["bio", "find-orfs", seq, "--min-aa", "2"])
    assert result.exit_code == 0
    assert "ORFs" in result.stdout
