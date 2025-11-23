from typer.testing import CliRunner

from science_ops.cli import app

runner = CliRunner()


def test_help_all_lists_subcommands():
    result = runner.invoke(app, ["help-all"])
    assert result.exit_code == 0
    assert "constants" in result.stdout
    assert "mech" in result.stdout
    assert "bio" in result.stdout
    assert "data" in result.stdout
    assert "em" in result.stdout
    assert "analysis" in result.stdout
    assert "labcalc" in result.stdout
    assert "bioseq" in result.stdout
