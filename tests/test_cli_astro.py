from typer.testing import CliRunner

from science_ops.cli import app

runner = CliRunner()


def test_astro_help_runs():
    result = runner.invoke(app, ["astro", "--help"])
    assert result.exit_code == 0
    assert "Usage" in result.stdout or "Commands" in result.stdout
