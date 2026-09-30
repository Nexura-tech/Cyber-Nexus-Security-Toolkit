from modules.user_manager.manager import (
    add_user,
    change_user_status,
    list_users,
)


def test_list_users(capsys, monkeypatch):
    fake_users = [
        {
            "id": 1,
            "username": "testuser",
            "created_at": "2026-09-26 12:00:00",
            "is_active": 1,
            "role": "user",
        }
    ]

    monkeypatch.setattr(
        "modules.user_manager.manager.get_all_users",
        lambda: fake_users,
    )

    list_users()

    output = capsys.readouterr().out

    assert "testuser" in output
    assert "Active" in output


def test_list_users_empty(capsys, monkeypatch):
    monkeypatch.setattr(
        "modules.user_manager.manager.get_all_users",
        lambda: [],
    )

    list_users()

    output = capsys.readouterr().out

    assert "No users found." in output


def test_add_user_success(monkeypatch, capsys):
    inputs = iter([
        "newuser",
        "TestPassword123!",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    monkeypatch.setattr(
        "modules.user_manager.manager.create_user",
        lambda username, password: 10,
    )

    add_user()

    output = capsys.readouterr().out

    assert "newuser" in output
    assert "created successfully" in output


def test_add_user_empty_username(monkeypatch, capsys):
    inputs = iter([
        "",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    add_user()

    output = capsys.readouterr().out

    assert "Username cannot be empty." in output


def test_add_user_duplicate(monkeypatch, capsys):
    inputs = iter([
        "existinguser",
        "TestPassword123!",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    def fake_create_user(username, password):
        raise ValueError(
            "Username 'existinguser' already exists."
        )

    monkeypatch.setattr(
        "modules.user_manager.manager.create_user",
        fake_create_user,
    )

    add_user()

    output = capsys.readouterr().out

    assert "already exists" in output


def test_change_user_status_activate(
    monkeypatch,
    capsys,
):
    inputs = iter([
        "testuser",
        "a",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    monkeypatch.setattr(
        "modules.user_manager.manager.set_user_active",
        lambda username, is_active: True,
    )

    change_user_status()

    output = capsys.readouterr().out

    assert "activated successfully" in output


def test_change_user_status_deactivate(
    monkeypatch,
    capsys,
):
    inputs = iter([
        "testuser",
        "d",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    monkeypatch.setattr(
        "modules.user_manager.manager.set_user_active",
        lambda username, is_active: True,
    )

    change_user_status()

    output = capsys.readouterr().out

    assert "deactivated successfully" in output


def test_change_user_status_invalid_action(
    monkeypatch,
    capsys,
):
    inputs = iter([
        "testuser",
        "x",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    change_user_status()

    output = capsys.readouterr().out

    assert "Invalid option." in output
