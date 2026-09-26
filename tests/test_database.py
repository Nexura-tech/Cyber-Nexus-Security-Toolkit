from database.manager import (
    add_report_history,
    get_connection,
    get_report_by_id,
    get_report_history,
    update_report_status,
)


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
