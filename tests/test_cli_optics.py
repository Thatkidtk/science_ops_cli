from typer.testing import CliRunner

from science_ops.cli import app

runner = CliRunner()


def test_optics_snell_basic():
    result = runner.invoke(app, ["optics", "snell", "1.0", "1.5", "30"])
    assert result.exit_code == 0
    assert "θ2" in result.stdout


def test_optics_thin_lens():
    result = runner.invoke(app, ["optics", "thin-lens", "10", "30"])
    assert result.exit_code == 0
    assert "d_i" in result.stdout
    assert "m =" in result.stdout
