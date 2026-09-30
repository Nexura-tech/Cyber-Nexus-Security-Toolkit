from database.manager import (
    add_report_history,
    get_connection,
    get_report_by_file_path,
    get_report_by_id,
    get_report_history,
    update_report_status,
    authenticate_user,
    create_user,
    get_user_by_username,
    set_user_active,
)
from core.passwords import verify_password


def test_database_connection(tmp_path, monkeypatch):
    database_file = tmp_path / "test.db"

    monkeypatch.setattr(
        "database.manager.DATABASE_FILE",
        database_file,
    )

    connection = get_connection()

    try:
        assert connection is not None

    finally:
        connection.close()


def test_database_row_factory(tmp_path, monkeypatch):
    database_file = tmp_path / "test.db"

    monkeypatch.setattr(
        "database.manager.DATABASE_FILE",
        database_file,
    )

    connection = get_connection()

    try:
        import sqlite3

        assert connection.row_factory == sqlite3.Row

    finally:
        connection.close()


def test_metadata_table(tmp_path, monkeypatch):
    database_file = tmp_path / "test.db"

    monkeypatch.setattr(
        "database.manager.DATABASE_FILE",
        database_file,
    )

    connection = get_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS app_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL UNIQUE,
                value TEXT
            )
            """
        )

        connection.commit()

        result = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name = 'app_metadata'
            """
        ).fetchone()

        assert result is not None
        assert result["name"] == "app_metadata"

    finally:
        connection.close()


def test_metadata_insert_and_read(tmp_path, monkeypatch):
    database_file = tmp_path / "test.db"

    monkeypatch.setattr(
        "database.manager.DATABASE_FILE",
        database_file,
    )

    connection = get_connection()

    try:
        connection.execute(
            """
            CREATE TABLE app_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL UNIQUE,
                value TEXT
            )
            """
        )

        connection.execute(
            """
            INSERT INTO app_metadata (key, value)
            VALUES (?, ?)
            """,
            ("app_version", "1.0.0"),
        )

        connection.commit()

        row = connection.execute(
            """
            SELECT key, value
            FROM app_metadata
            WHERE key = ?
            """,
            ("app_version",),
        ).fetchone()

        assert row is not None
        assert row["key"] == "app_version"
        assert row["value"] == "1.0.0"

    finally:
        connection.close()


def test_report_history(tmp_path, monkeypatch):
    database_file = tmp_path / "test.db"

    monkeypatch.setattr(
        "database.manager.DATABASE_FILE",
        database_file,
    )

    add_report_history(
        report_name="test_report.json",
        report_type="JSON",
        file_path="reports/test_report.json",
        created_at="2026-09-25 03:30:00",
    )

    history = get_report_history()

    assert len(history) == 1

    report = history[0]

    assert report["report_name"] == "test_report.json"
    assert report["report_type"] == "JSON"
    assert report["file_path"] == "reports/test_report.json"
    assert report["created_at"] == "2026-09-25 03:30:00"
    assert report["status"] == "available"


def test_report_history_limit(tmp_path, monkeypatch):
    database_file = tmp_path / "test.db"

    monkeypatch.setattr(
        "database.manager.DATABASE_FILE",
        database_file,
    )

    for number in range(5):
        add_report_history(
            report_name=f"report_{number}.json",
            report_type="JSON",
            file_path=f"reports/report_{number}.json",
            created_at=f"2026-09-25 03:3{number}:00",
        )

    history = get_report_history(limit=3)

    assert len(history) == 3


def test_get_report_by_id(tmp_path, monkeypatch):
    database_file = tmp_path / "test.db"

    monkeypatch.setattr(
        "database.manager.DATABASE_FILE",
        database_file,
    )

    add_report_history(
        report_name="test_report.json",
        report_type="JSON",
        file_path="reports/test_report.json",
        created_at="2026-09-25 03:30:00",
    )

    history = get_report_history()

    report_id = history[0]["id"]

    report = get_report_by_id(report_id)

    assert report is not None
    assert report["id"] == report_id
    assert report["report_name"] == "test_report.json"
    assert report["status"] == "available"


def test_update_report_status(tmp_path, monkeypatch):
    database_file = tmp_path / "test.db"

    monkeypatch.setattr(
        "database.manager.DATABASE_FILE",
        database_file,
    )

    add_report_history(
        report_name="test_report.json",
        report_type="JSON",
        file_path="reports/test_report.json",
        created_at="2026-09-25 03:30:00",
    )

    history = get_report_history()

    report_id = history[0]["id"]

    result = update_report_status(
        report_id,
        "deleted",
    )

    assert result is True

    report = get_report_by_id(report_id)

    assert report is not None
    assert report["status"] == "deleted"


def test_update_nonexistent_report_status(
    tmp_path,
    monkeypatch,
):
    database_file = tmp_path / "test.db"

    monkeypatch.setattr(
        "database.manager.DATABASE_FILE",
        database_file,
    )

    result = update_report_status(
        99999,
        "deleted",
    )

    assert result is False

def test_report_history_invalid_limit(
    tmp_path,
    monkeypatch,
):
    database_file = tmp_path / "test.db"

    monkeypatch.setattr(
        "database.manager.DATABASE_FILE",
        database_file,
    )

    for number in range(3):
        add_report_history(
            report_name=f"report_{number}.json",
            report_type="JSON",
            file_path=f"reports/report_{number}.json",
            created_at="2026-09-26 10:00:00",
        )

    history = get_report_history(
        "invalid"
    )

    assert len(history) == 3


def test_report_history_zero_limit(
    tmp_path,
    monkeypatch,
):
    database_file = tmp_path / "test.db"

    monkeypatch.setattr(
        "database.manager.DATABASE_FILE",
        database_file,
    )

    for number in range(3):
        add_report_history(
            report_name=f"report_{number}.json",
            report_type="JSON",
            file_path=f"reports/report_{number}.json",
            created_at="2026-09-26 10:00:00",
        )

    history = get_report_history(0)

    assert len(history) == 3


def test_report_history_negative_limit(
    tmp_path,
    monkeypatch,
):
    database_file = tmp_path / "test.db"

    monkeypatch.setattr(
        "database.manager.DATABASE_FILE",
        database_file,
    )

    for number in range(3):
        add_report_history(
            report_name=f"report_{number}.json",
            report_type="JSON",
            file_path=f"reports/report_{number}.json",
            created_at="2026-09-26 10:00:00",
        )

    history = get_report_history(-10)

    assert len(history) == 3

def test_update_report_status_rejects_invalid_status(
    tmp_path,
    monkeypatch,
):
    database_file = tmp_path / "test.db"

    monkeypatch.setattr(
        "database.manager.DATABASE_FILE",
        database_file,
    )

    add_report_history(
        report_name="test_report.json",
        report_type="JSON",
        file_path="reports/test_report.json",
        created_at="2026-09-26 10:00:00",
    )

    history = get_report_history()

    report_id = history[0]["id"]

    result = update_report_status(
        report_id,
        "invalid_status",
    )

    assert result is False

    report = get_report_by_id(report_id)

    assert report is not None
    assert report["status"] == "available"

def test_get_report_by_id_invalid_input(
    tmp_path,
    monkeypatch,
):
    database_file = tmp_path / "test.db"

    monkeypatch.setattr(
        "database.manager.DATABASE_FILE",
        database_file,
    )

    assert get_report_by_id("invalid") is None
    assert get_report_by_id(None) is None
    assert get_report_by_id(0) is None
    assert get_report_by_id(-1) is None

def test_report_history_complete_workflow(
    tmp_path,
    monkeypatch,
):
    database_file = tmp_path / "test.db"

    monkeypatch.setattr(
        "database.manager.DATABASE_FILE",
        database_file,
    )

    # Step 1: Create report history
    add_report_history(
        report_name="security_report.json",
        report_type="JSON",
        file_path="reports/security_report.json",
        created_at="2026-09-26 11:00:00",
    )

    # Step 2: Verify report exists
    history = get_report_history()

    assert len(history) == 1

    report_id = history[0]["id"]

    assert history[0]["status"] == "available"

    # Step 3: Retrieve report directly
    report = get_report_by_id(report_id)

    assert report is not None
    assert report["report_name"] == "security_report.json"
    assert report["status"] == "available"

    # Step 4: Mark report as deleted
    result = update_report_status(
        report_id,
        "deleted",
    )

    assert result is True

    # Step 5: Verify status changed
    updated_report = get_report_by_id(
        report_id
    )

    assert updated_report is not None
    assert updated_report["status"] == "deleted"

    # Step 6: Verify history was not removed
    history_after_delete = get_report_history()

    assert len(history_after_delete) == 1
    assert history_after_delete[0]["id"] == report_id
    assert history_after_delete[0]["status"] == "deleted"

def test_get_report_by_file_path(
    tmp_path,
    monkeypatch,
):
    database_file = tmp_path / "test.db"

    monkeypatch.setattr(
        "database.manager.DATABASE_FILE",
        database_file,
    )

    add_report_history(
        report_name="security_report.json",
        report_type="JSON",
        file_path="/project/reports/security_report.json",
        created_at="2026-09-26 11:30:00",
    )

    report = get_report_by_file_path(
        "/project/reports/security_report.json"
    )

    assert report is not None
    assert report["report_name"] == "security_report.json"
    assert report["report_type"] == "JSON"
    assert (
        report["file_path"]
        == "/project/reports/security_report.json"
    )
    assert report["status"] == "available"


def test_get_report_by_file_path_not_found(
    tmp_path,
    monkeypatch,
):
    database_file = tmp_path / "test.db"

    monkeypatch.setattr(
        "database.manager.DATABASE_FILE",
        database_file,
    )

    report = get_report_by_file_path(
        "/project/reports/missing.json"
    )

    assert report is None


def test_get_report_by_file_path_invalid_input(
    tmp_path,
    monkeypatch,
):
    database_file = tmp_path / "test.db"

    monkeypatch.setattr(
        "database.manager.DATABASE_FILE",
        database_file,
    )

    assert get_report_by_file_path(None) is None
    assert get_report_by_file_path("") is None
    assert get_report_by_file_path("   ") is None

def test_create_user():
    username = "test_create_user"

    user_id = create_user(
        username,
        "TestPassword123!",
    )

    assert isinstance(user_id, int)
    assert user_id > 0

    user = get_user_by_username(username)

    assert user is not None
    assert user["username"] == username
    assert user["is_active"] == 1


def test_password_is_hashed():
    username = "test_password_hash"

    create_user(
        username,
        "TestPassword123!",
    )

    user = get_user_by_username(username)

    assert user is not None

    assert user["password_hash"] != "TestPassword123!"

    assert verify_password(
        "TestPassword123!",
        user["password_hash"],
    )

    assert not verify_password(
        "WrongPassword",
        user["password_hash"],
    )


def test_get_nonexistent_user():
    user = get_user_by_username(
        "this_user_does_not_exist"
    )

    assert user is None


def test_set_user_active():
    username = "test_user_active"

    create_user(
        username,
        "TestPassword123!",
    )

    result = set_user_active(
        username,
        False,
    )

    assert result is True

    user = get_user_by_username(username)

    assert user is not None
    assert user["is_active"] == 0

    result = set_user_active(
        username,
        True,
    )

    assert result is True

    user = get_user_by_username(username)

    assert user["is_active"] == 1


def test_set_user_active_nonexistent():
    result = set_user_active(
        "nonexistent_user_12345",
        False,
    )

    assert result is False

def test_create_duplicate_user():
    username = "test_duplicate_user"

    create_user(
        username,
        "TestPassword123!",
    )

    try:
        create_user(
            username,
            "AnotherPassword123!",
        )
        assert False, "Expected ValueError for duplicate username."

    except ValueError as error:
        assert str(error) == (
            f"Username '{username}' already exists."
        )


def test_authenticate_user_success():
    username = "test_auth_success"

    create_user(
        username,
        "TestPassword123!",
    )

    user = authenticate_user(
        username,
        "TestPassword123!",
    )

    assert user is not None
    assert user["username"] == username
    assert user["is_active"] == 1


def test_authenticate_user_wrong_password():
    username = "test_auth_wrong_password"

    create_user(
        username,
        "TestPassword123!",
    )

    user = authenticate_user(
        username,
        "WrongPassword",
    )

    assert user is None


def test_authenticate_nonexistent_user():
    user = authenticate_user(
        "user_that_does_not_exist",
        "TestPassword123!",
    )

    assert user is None


def test_authenticate_inactive_user():
    username = "test_auth_inactive"

    create_user(
        username,
        "TestPassword123!",
    )

    result = set_user_active(
        username,
        False,
    )

    assert result is True

    user = authenticate_user(
        username,
        "TestPassword123!",
    )

    assert user is None

def test_create_user_always_creates_normal_user():
    from database.manager import (
        create_user,
        get_user_by_username,
    )

    create_user("normaltest", "TestPassword123!")

    user = get_user_by_username("normaltest")

    assert user is not None
    assert user["role"] == "user"


def test_create_first_admin_only_allows_sabbo():
    from database.manager import (
        create_first_admin,
        get_user_by_username,
    )

    create_first_admin("Sabbo", "AdminPassword123!")

    user = get_user_by_username("Sabbo")

    assert user is not None
    assert user["role"] == "admin"


def test_create_first_admin_rejects_other_username():
    from database.manager import create_first_admin

    try:
        create_first_admin("OtherAdmin", "AdminPassword123!")
        assert False
    except ValueError as error:
        assert "Sabbo" in str(error)


def test_create_first_admin_allows_only_one_admin():
    from database.manager import (
        create_first_admin,
        get_admin_count,
    )

    if get_admin_count() == 0:
        create_first_admin(
            "Sabbo",
            "AdminPassword123!",
        )

    assert get_admin_count() == 1

    try:
        create_first_admin(
            "Sabbo",
            "AnotherPassword123!",
        )
        assert False
    except ValueError as error:
        assert "already exists" in str(error)

    assert get_admin_count() == 1

def test_ensure_admin_account_creates_sabbo():
    from database.manager import (
        ensure_admin_account,
        get_user_by_username,
    )

    result = ensure_admin_account(
        "AdminPassword123!"
    )

    assert result is True

    user = get_user_by_username("Sabbo")

    assert user is not None
    assert user["role"] == "admin"


def test_ensure_admin_account_does_not_create_second_admin():
    from database.manager import ensure_admin_account

    ensure_admin_account(
        "AdminPassword123!"
    )

    result = ensure_admin_account(
        "AnotherPassword123!"
    )

    assert result is False


def test_ensure_admin_account_does_not_change_existing_user():
    from database.manager import (
        create_user,
        ensure_admin_account,
        get_user_by_username,
    )

    create_user(
        "normaluser",
        "UserPassword123!",
    )

    ensure_admin_account(
        "AdminPassword123!"
    )

    user = get_user_by_username("normaluser")

    assert user is not None
    assert user["role"] == "user"

def test_get_login_security_returns_default_values():
    from database.manager import (
        create_user,
        get_login_security,
    )

    create_user(
        "securitytest",
        "TestPassword123!",
    )

    security = get_login_security(
        "securitytest"
    )

    assert security is not None
    assert security["username"] == "securitytest"
    assert security["failed_login_attempts"] == 0
    assert security["locked_until"] is None


def test_update_login_security():
    from database.manager import (
        create_user,
        get_login_security,
        update_login_security,
    )

    create_user(
        "securitytest",
        "TestPassword123!",
    )

    result = update_login_security(
        "securitytest",
        3,
        "2026-09-27 01:30:00",
    )

    assert result is True

    security = get_login_security(
        "securitytest"
    )

    assert security["failed_login_attempts"] == 3
    assert (
        security["locked_until"]
        == "2026-09-27 01:30:00"
    )


def test_update_login_security_unknown_user():
    from database.manager import (
        update_login_security,
    )

    result = update_login_security(
        "unknownuser",
        1,
    )

    assert result is False

def test_authenticate_user_increments_failed_attempts():
    from database.manager import (
        authenticate_user,
        create_user,
        get_login_security,
    )

    create_user(
        "locktest",
        "CorrectPassword123!",
    )

    result = authenticate_user(
        "locktest",
        "WrongPassword",
    )

    assert result is None

    security = get_login_security("locktest")

    assert security["failed_login_attempts"] == 1
    assert security["locked_until"] is None


def test_authenticate_user_resets_failed_attempts_on_success():
    from database.manager import (
        authenticate_user,
        create_user,
        get_login_security,
        update_login_security,
    )

    create_user(
        "resettst",
        "CorrectPassword123!",
    )

    update_login_security(
        "resettst",
        3,
        None,
    )

    result = authenticate_user(
        "resettst",
        "CorrectPassword123!",
    )

    assert result is not None

    security = get_login_security("resettst")

    assert security["failed_login_attempts"] == 0
    assert security["locked_until"] is None


def test_authenticate_user_locks_after_max_attempts():
    from database.manager import (
        authenticate_user,
        create_user,
        get_login_security,
    )
    from core.config import MAX_LOGIN_ATTEMPTS

    create_user(
        "lockuser",
        "CorrectPassword123!",
    )

    for _ in range(MAX_LOGIN_ATTEMPTS):
        result = authenticate_user(
            "lockuser",
            "WrongPassword",
        )

        assert result is None

    security = get_login_security("lockuser")

    assert (
        security["failed_login_attempts"]
        == MAX_LOGIN_ATTEMPTS
    )

    assert security["locked_until"] is not None


def test_locked_user_cannot_login_with_correct_password():
    from database.manager import (
        authenticate_user,
        create_user,
        get_login_security,
    )
    from core.config import MAX_LOGIN_ATTEMPTS

    create_user(
        "blockeduser",
        "CorrectPassword123!",
    )

    for _ in range(MAX_LOGIN_ATTEMPTS):
        authenticate_user(
            "blockeduser",
            "WrongPassword",
        )

    result = authenticate_user(
        "blockeduser",
        "CorrectPassword123!",
    )

    assert result is None

    security = get_login_security(
        "blockeduser"
    )

    assert security["locked_until"] is not None

def test_expired_lockout_allows_correct_password():
    from database.manager import (
        authenticate_user,
        create_user,
        get_login_security,
        update_login_security,
    )

    create_user(
        "expiredlock",
        "CorrectPassword123!",
    )

    update_login_security(
        "expiredlock",
        5,
        "2000-01-01T00:00:00",
    )

    result = authenticate_user(
        "expiredlock",
        "CorrectPassword123!",
    )

    assert result is not None

    security = get_login_security(
        "expiredlock"
    )

    assert security["failed_login_attempts"] == 0
    assert security["locked_until"] is None
