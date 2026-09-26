from app import login, logout
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
        "WrongPassword",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
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
