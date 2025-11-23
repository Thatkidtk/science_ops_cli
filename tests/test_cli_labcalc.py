from typer.testing import CliRunner

from science_ops.cli import app

runner = CliRunner()


def test_labcalc_stock_dilution():
    result = runner.invoke(app, ["labcalc", "stock-dilution", "10", "1", "100"])
    assert result.exit_code == 0
    assert "Stock volume" in result.stdout
    assert "Add solvent" in result.stdout


def test_labcalc_percent_error():
    result = runner.invoke(app, ["labcalc", "percent-error", "10", "9"])
    assert result.exit_code == 0
    assert "Percent error" in result.stdout
