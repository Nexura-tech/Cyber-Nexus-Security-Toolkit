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
    Create the initial database structure.
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
            (key, str(value)),
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
            (key,),
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
            (key,),
        )

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()

    print(
        f"Database initialized: {DATABASE_FILE}"
    )
