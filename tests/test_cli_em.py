from typer.testing import CliRunner

from science_ops.cli import app

runner = CliRunner()


def test_em_coulomb_basic():
    result = runner.invoke(app, ["em", "coulomb", "1e-6", "1e-6", "0.05"])
    assert result.exit_code == 0
    assert "N" in result.stdout
    assert "repulsive" in result.stdout


def test_em_reactance_inductive_only():
    result = runner.invoke(app, ["em", "reactance", "1000", "--L", "0.01"])
    assert result.exit_code == 0
    assert "X_L" in result.stdout
    assert "X_total" in result.stdout
