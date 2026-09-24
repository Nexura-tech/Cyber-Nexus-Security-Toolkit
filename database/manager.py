import sqlite3

from core.config import BASE_DIR


DATABASE_FILE = BASE_DIR / "cyber_nexus.db"


def get_connection():
    """
    Create and return a SQLite database connection.
    """
    connection = sqlite3.connect(DATABASE_FILE)

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """
    Create the initial database structure
    and apply lightweight schema migrations.
    """
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

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS report_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_name TEXT NOT NULL,
                report_type TEXT NOT NULL,
                file_path TEXT NOT NULL,
                created_at TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'available'
            )
            """
        )

        # Check whether the existing database
        # already has the status column.
        columns = connection.execute(
            """
            PRAGMA table_info(report_history)
            """
        ).fetchall()

        column_names = {
            column["name"]
            for column in columns
        }

        # Add status column to older databases.
        if "status" not in column_names:
            connection.execute(
                """
                ALTER TABLE report_history
                ADD COLUMN status TEXT NOT NULL
                DEFAULT 'available'
                """
            )

        connection.commit()

    finally:
        connection.close()


def set_metadata(key, value):
    """
    Create or update an application metadata value.
    """
    initialize_database()

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO app_metadata (key, value)
            VALUES (?, ?)
            ON CONFLICT(key)
            DO UPDATE SET value = excluded.value
            """,
            (
                str(key),
                str(value),
            ),
        )

        connection.commit()

    finally:
        connection.close()


def get_metadata(key, default=None):
    """
    Retrieve an application metadata value.
    """
    initialize_database()

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT value
            FROM app_metadata
            WHERE key = ?
            """,
            (str(key),),
        ).fetchone()

        if row is None:
            return default

        return row["value"]

    finally:
        connection.close()


def delete_metadata(key):
    """
    Delete an application metadata value.
    """
    initialize_database()

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            DELETE FROM app_metadata
            WHERE key = ?
            """,
            (str(key),),
        )

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()


def add_report_history(
    report_name,
    report_type,
    file_path,
    created_at,
):
    """
    Store generated report information
    in the database.
    """
    initialize_database()

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO report_history (
                report_name,
                report_type,
                file_path,
                created_at,
                status
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                str(report_name),
                str(report_type),
                str(file_path),
                str(created_at),
                "available",
            ),
        )

        connection.commit()

    finally:
        connection.close()


def get_report_history(limit=50):
    """
    Return recent report history.
    """
    initialize_database()

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                id,
                report_name,
                report_type,
                file_path,
                created_at,
                status
            FROM report_history
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

        return [
            dict(row)
            for row in rows
        ]

    finally:
        connection.close()


def update_report_status(
    report_id,
    status,
):
    """
    Update the status of a report history entry.
    """
    initialize_database()

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            UPDATE report_history
            SET status = ?
            WHERE id = ?
            """,
            (
                str(status),
                int(report_id),
            ),
        )

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()


def get_report_by_id(report_id):
    """
    Retrieve a single report history entry by ID.
    """
    initialize_database()

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT
                id,
                report_name,
                report_type,
                file_path,
                created_at,
                status
            FROM report_history
            WHERE id = ?
            """,
            (int(report_id),),
        ).fetchone()

        if row is None:
            return None

        return dict(row)

    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()

    print(
        f"Database initialized: {DATABASE_FILE}"
    )
