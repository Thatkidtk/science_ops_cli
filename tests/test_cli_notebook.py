from pathlib import Path

from typer.testing import CliRunner

from science_ops.cli import app

runner = CliRunner()


def test_notebook_set_path(tmp_path):
    env = {"XDG_CONFIG_HOME": str(tmp_path)}
    new_path = tmp_path / "lab.md"

    result = runner.invoke(app, ["notebook", "set-path", str(new_path)], env=env)
    assert result.exit_code == 0
    assert new_path.exists() is False

    result2 = runner.invoke(app, ["notebook", "log", "hello"], env=env)
    assert result2.exit_code == 0
    assert new_path.exists()
    assert "hello" in new_path.read_text()
