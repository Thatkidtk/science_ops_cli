from typer.testing import CliRunner
from pathlib import Path

from science_ops.cli import app

runner = CliRunner()


def _make_csv(tmp_path: Path) -> Path:
    p = tmp_path / "reg.csv"
    p.write_text("x,y\n1,2\n2,4\n3,6\n", encoding="utf-8")
    return p


def test_analysis_regress(tmp_path):
    csv_path = _make_csv(tmp_path)
    result = runner.invoke(app, ["analysis", "regress", str(csv_path), "x", "y"])
    assert result.exit_code == 0
    assert "slope" in result.stdout
    assert "r^2" in result.stdout


def test_analysis_uncertainty():
    result = runner.invoke(app, ["analysis", "uncertainty", "1.0", "2.0"])
    assert result.exit_code == 0
    assert "Combined uncertainty" in result.stdout
