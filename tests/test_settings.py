from pathlib import Path

from modules.settings.manager import (
    save_request_timeout,
)


def test_save_request_timeout_creates_env_file(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"

    monkeypatch.setattr(
        "modules.settings.manager.ENV_FILE",
        env_file,
    )

    save_request_timeout(25)

    assert env_file.exists()
    assert (
        "CYBER_NEXUS_REQUEST_TIMEOUT=25"
        in env_file.read_text(encoding="utf-8")
    )


def test_save_request_timeout_updates_existing_value(
    tmp_path,
    monkeypatch,
):
    env_file = tmp_path / ".env"

    env_file.write_text(
        "CYBER_NEXUS_REQUEST_TIMEOUT=10\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "modules.settings.manager.ENV_FILE",
        env_file,
    )

    save_request_timeout(30)

    content = env_file.read_text(
        encoding="utf-8"
    )

    assert "CYBER_NEXUS_REQUEST_TIMEOUT=30" in content
    assert "CYBER_NEXUS_REQUEST_TIMEOUT=10" not in content


def test_save_request_timeout_preserves_other_settings(
    tmp_path,
    monkeypatch,
):
    env_file = tmp_path / ".env"

    env_file.write_text(
        "CYBER_NEXUS_REQUEST_TIMEOUT=10\n"
        "CYBER_NEXUS_MAX_LOGIN_ATTEMPTS=5\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "modules.settings.manager.ENV_FILE",
        env_file,
    )

    save_request_timeout(20)

    content = env_file.read_text(
        encoding="utf-8"
    )

    assert "CYBER_NEXUS_REQUEST_TIMEOUT=20" in content
    assert "CYBER_NEXUS_MAX_LOGIN_ATTEMPTS=5" in content

def test_change_request_timeout_logs_change(
    monkeypatch,
    caplog,
):
    monkeypatch.setattr(
        "modules.settings.manager.save_request_timeout",
        lambda value: None,
    )

    monkeypatch.setattr(
        "modules.settings.manager.REQUEST_TIMEOUT",
        10,
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt="": "25",
    )

    from modules.settings.manager import change_request_timeout

    with caplog.at_level("INFO", logger="cyber_nexus"):
        change_request_timeout()

    assert (
        "Request timeout changed from 10 to 25 seconds."
        in caplog.text
    )
