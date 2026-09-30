from core.session import Session


def test_session_starts_logged_out():
    session = Session()

    assert session.is_authenticated() is False
    assert session.get_username() is None
    assert session.get_role() is None
    assert session.is_admin() is False


def test_session_login():
    session = Session()

    user = {
        "id": 1,
        "username": "testuser",
        "is_active": 1,
        "role": "user",
    }

    session.login(user)

    assert session.is_authenticated() is True
    assert session.get_username() == "testuser"
    assert session.get_role() == "user"
    assert session.is_admin() is False


def test_session_admin_role():
    session = Session()

    user = {
        "id": 1,
        "username": "adminuser",
        "is_active": 1,
        "role": "admin",
    }

    session.login(user)

    assert session.get_role() == "admin"
    assert session.is_admin() is True


def test_session_normal_user_role():
    session = Session()

    user = {
        "id": 2,
        "username": "normaluser",
        "is_active": 1,
        "role": "user",
    }

    session.login(user)

    assert session.get_role() == "user"
    assert session.is_admin() is False


def test_session_logged_out_role():
    session = Session()

    assert session.get_role() is None
    assert session.is_admin() is False


def test_session_logout():
    session = Session()

    user = {
        "id": 1,
        "username": "testuser",
        "is_active": 1,
        "role": "user",
    }

    session.login(user)
    session.logout()

    assert session.is_authenticated() is False
    assert session.get_username() is None
    assert session.get_role() is None
    assert session.is_admin() is False
