import importlib


def reload_config(monkeypatch):
    import core.config as config

    importlib.reload(config)
    return config


def test_default_request_timeout(monkeypatch):
    monkeypatch.delenv(
        "CYBER_NEXUS_REQUEST_TIMEOUT",
        raising=False,
    )

    config = reload_config(monkeypatch)

    assert config.REQUEST_TIMEOUT == 10


def test_custom_request_timeout(monkeypatch):
    monkeypatch.setenv(
        "CYBER_NEXUS_REQUEST_TIMEOUT",
        "15",
    )

    config = reload_config(monkeypatch)

    assert config.REQUEST_TIMEOUT == 15


def test_invalid_request_timeout(monkeypatch):
    monkeypatch.setenv(
        "CYBER_NEXUS_REQUEST_TIMEOUT",
        "abc",
    )

    config = reload_config(monkeypatch)

    assert config.REQUEST_TIMEOUT == 10


def test_negative_request_timeout(monkeypatch):
    monkeypatch.setenv(
        "CYBER_NEXUS_REQUEST_TIMEOUT",
        "-5",
    )

    config = reload_config(monkeypatch)

    assert config.REQUEST_TIMEOUT == 10
