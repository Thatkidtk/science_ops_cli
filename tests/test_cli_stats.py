from typer.testing import CliRunner

from science_ops.cli import app

runner = CliRunner()


def test_stats_describe():
    result = runner.invoke(app, ["stats", "describe", "1", "2", "3"])
    assert result.exit_code == 0
    assert "mean" in result.stdout.lower()
