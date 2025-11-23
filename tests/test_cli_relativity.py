from typer.testing import CliRunner

from science_ops.cli import app

runner = CliRunner()


def test_relativity_gamma_invalid():
    result = runner.invoke(app, ["relativity", "gamma", "1.2"])
    assert result.exit_code != 0
    assert "must be in [0, 1)" in result.stdout


def test_relativity_grav_dilation_body_default():
    result = runner.invoke(app, ["relativity", "grav-dilation"])
    assert result.exit_code == 0
    assert "dτ/dt" in result.stdout
