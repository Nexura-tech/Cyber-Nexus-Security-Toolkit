import sqlite3

from database.manager import get_connection


def test_database_connection(tmp_path, monkeypatch):
    database_file = tmp_path / "test.db"

    monkeypatch.setattr(
        "database.manager.DATABASE_FILE",
        database_file,
    )

    connection = get_connection()

    try:
        assert isinstance(connection, sqlite3.Connection)

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

        cursor = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name = 'app_metadata'
            """
        )

        result = cursor.fetchone()

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
