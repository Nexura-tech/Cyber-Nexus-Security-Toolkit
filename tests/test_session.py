from core.session import Session


def test_session_starts_logged_out():
    session = Session()

    assert session.is_authenticated() is False
    assert session.get_username() is None


def test_session_login():
    session = Session()

    user = {
        "id": 1,
        "username": "testuser",
        "is_active": 1,
    }

    session.login(user)

    assert session.is_authenticated() is True
    assert session.get_username() == "testuser"


def test_session_logout():
    session = Session()

    user = {
        "id": 1,
        "username": "testuser",
        "is_active": 1,
    }

    session.login(user)
    session.logout()

    assert session.is_authenticated() is False
    assert session.get_username() is None
