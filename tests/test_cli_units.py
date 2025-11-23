from typer.testing import CliRunner

from science_ops.cli import app

runner = CliRunner()


def test_units_convert_length():
    result = runner.invoke(app, ["units", "convert", "1000", "m", "km"])
    assert result.exit_code == 0
    assert "1" in result.stdout
    assert "km" in result.stdout


def test_units_incompatible_dims():
    result = runner.invoke(app, ["units", "convert", "10", "m", "s"])
    assert result.exit_code != 0
    assert "Incompatible units" in result.stdout
