from pathlib import Path

from typer.testing import CliRunner

from science_ops.cli import app

runner = CliRunner()


def _make_csv(tmp_path: Path) -> Path:
    p = tmp_path / "data.csv"
    p.write_text("x,y,label\n1,2,a\n3,4,b\n5,6,c\n", encoding="utf-8")
    return p


def test_data_summarize(tmp_path):
    csv_path = _make_csv(tmp_path)
    result = runner.invoke(app, ["data", "summarize", str(csv_path)])
    assert result.exit_code == 0
    assert "x" in result.stdout
    assert "y" in result.stdout
    assert "Mean" in result.stdout


def test_data_head(tmp_path):
    csv_path = _make_csv(tmp_path)
    result = runner.invoke(app, ["data", "head", str(csv_path), "--rows", "2"])
    assert result.exit_code == 0
    assert "label" in result.stdout
    assert "a" in result.stdout
    assert "b" in result.stdout


def test_data_hist(tmp_path):
    csv_path = _make_csv(tmp_path)
    result = runner.invoke(app, ["data", "hist", str(csv_path), "x", "--bins", "2"])
    assert result.exit_code == 0
    assert "Histogram for" in result.stdout
    assert "*" in result.stdout
