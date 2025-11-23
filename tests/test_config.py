from pathlib import Path

from science_ops.config import Config, load_config, save_config


def test_config_round_trip(tmp_path, monkeypatch):
    cfg_file_dir = tmp_path
    monkeypatch.setenv("XDG_CONFIG_HOME", str(cfg_file_dir))

    cfg = Config(notebook_path=tmp_path / "note.md")
    save_config(cfg)

    loaded = load_config()
    assert loaded.notebook_path == cfg.notebook_path
