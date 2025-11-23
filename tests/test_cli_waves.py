from typer.testing import CliRunner

from science_ops.cli import app

runner = CliRunner()


def test_waves_sine():
    result = runner.invoke(app, ["waves", "sine", "--freq", "1", "--samples", "20"])
    assert result.exit_code == 0
    assert "*" in result.stdout
