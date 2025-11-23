from typer.testing import CliRunner

from science_ops.cli import app

runner = CliRunner()


def test_mech_projectile_cli():
    result = runner.invoke(app, ["mech", "projectile", "20", "45"])
    assert result.exit_code == 0
    assert "Time of flight" in result.stdout
    assert "Horizontal range" in result.stdout


def test_mech_projectile_unknown_body():
    result = runner.invoke(app, ["mech", "projectile", "20", "45", "--body", "pluto"])
    assert result.exit_code != 0
    assert "Unknown body" in result.stdout


def test_mech_pendulum_invalid_length():
    result = runner.invoke(app, ["mech", "pendulum", "0"])
    assert result.exit_code != 0
    assert "Length must be > 0" in result.stdout
