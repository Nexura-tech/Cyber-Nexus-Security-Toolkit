from app import (
    login,
    logout,
    run_command,
)
from core.commands import COMMANDS
from core.session import Session

def test_login_success(monkeypatch):
    class FakeUser:
        pass

    fake_user = {
        "id": 1,
        "username": "testuser",
        "password_hash": "hashed",
        "created_at": "2026-09-26 12:00:00",
        "is_active": 1,
        "role": "user",
    }

    monkeypatch.setattr(
        "app.authenticate_user",
        lambda username, password: fake_user,
    )

    inputs = iter([
        "testuser",
        "TestPassword123!",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    result = login()

    assert result == fake_user


def test_login_empty_username(monkeypatch):
    inputs = iter([
        "",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    result = login()

    assert result is None


def test_login_empty_password(monkeypatch):
    inputs = iter([
        "testuser",
        "",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    result = login()

    assert result is None

def test_login_invalid_credentials(monkeypatch):
    monkeypatch.setattr(
        "app.authenticate_user",
        lambda username, password: None,
    )

    inputs = iter([
        "testuser",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    monkeypatch.setattr(
        "app.getpass",
        lambda _: "WrongPassword",
    )

    result = login()

    assert result is None


def test_logout_success(capsys):
    session = Session()

    session.login({
        "id": 1,
        "username": "testuser",
        "is_active": 1,
    })

    result = logout(session)

    assert result is True
    assert session.is_authenticated() is False
    assert session.get_username() is None

    output = capsys.readouterr().out

    assert "logged out successfully" in output

def test_logout_without_login(capsys):
    session = Session()

    result = logout(session)

    assert result is False
    assert session.is_authenticated() is False

    output = capsys.readouterr().out

    assert "No user is currently logged in." in output

def test_run_command_blocks_non_admin(capsys):
    session = Session()

    session.login({
        "id": 2,
        "username": "normaluser",
        "is_active": 1,
        "role": "user",
    })

    run_command("12", session)

    output = capsys.readouterr().out

    assert "Access denied" in output


def test_run_command_allows_admin(monkeypatch):
    session = Session()

    session.login({
        "id": 1,
        "username": "adminuser",
        "is_active": 1,
        "role": "admin",
    })

    called = []

    monkeypatch.setitem(
        COMMANDS,
        "12",
        (
            "User Management",
            lambda: called.append(True),
        ),
    )

    run_command("12", session)

    assert called == [True]

def test_show_menu_hides_user_management_for_normal_user(capsys):
    session = Session()

    session.login({
        "id": 2,
        "username": "normaluser",
        "is_active": 1,
        "role": "user",
    })

    from app import show_menu

    show_menu(session)

    output = capsys.readouterr().out

    assert "12. User Management" not in output
    assert "13. Logout" in output


def test_show_menu_shows_user_management_for_admin(capsys):
    session = Session()

    session.login({
        "id": 1,
        "username": "adminuser",
        "is_active": 1,
        "role": "admin",
    })

    from app import show_menu

    show_menu(session)

    output = capsys.readouterr().out

    assert "12. User Management" in output
    assert "13. Logout" in output
