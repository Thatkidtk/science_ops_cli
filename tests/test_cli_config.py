from pathlib import Path

from typer.testing import CliRunner

from science_ops.cli import app

runner = CliRunner()


def test_config_show(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    result = runner.invoke(app, ["config", "show"])
    assert result.exit_code == 0
    assert "notebook_path" in result.stdout


def test_config_set(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    new_path = tmp_path / "lab.md"
    result = runner.invoke(app, ["config", "set", "notebook_path", str(new_path)])
    assert result.exit_code == 0
    assert "lab.md" in result.stdout
