import sqlite3

from core.config import BASE_DIR

from core.passwords import hash_password
from core.utils import get_timestamp

DATABASE_FILE = BASE_DIR / "cyber_nexus.db"

REPORT_STATUSES = {
    "available",
    "deleted",
}


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

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1
            )
            """
        )

        columns = connection.execute(
            """
            PRAGMA table_info(report_history)
            """
        ).fetchall()

        column_names = {
            column["name"]
            for column in columns
        }

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
    try:
        limit = int(limit)
    except (TypeError, ValueError):
        limit = 50

    if limit < 1:
        limit = 50

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
    status = str(status).strip().lower()

    if status not in REPORT_STATUSES:
        return False

    try:
        report_id = int(report_id)
    except (TypeError, ValueError):
        return False

    if report_id < 1:
        return False

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
                status,
                report_id,
            ),
        )

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()

def get_report_by_file_path(file_path):
    """
    Retrieve a report history entry by file path.
    """
    if file_path is None:
        return None

    file_path = str(file_path).strip()

    if not file_path:
        return None

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
            WHERE file_path = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (file_path,),
        ).fetchone()

        if row is None:
            return None

        return dict(row)

    finally:
        connection.close()

def get_report_by_id(report_id):
    """
    Retrieve a single report history entry by ID.
    """
    try:
        report_id = int(report_id)
    except (TypeError, ValueError):
        return None

    if report_id < 1:
        return None

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
            (report_id,),
        ).fetchone()

        if row is None:
            return None

        return dict(row)

    finally:
        connection.close()

def create_user(username, password):
    """
    Create a new user with a securely hashed password.
    """
    username = str(username).strip()

    if not username:
        raise ValueError("Username cannot be empty.")

    if not isinstance(password, str) or not password:
        raise ValueError("Password cannot be empty.")

    initialize_database()

    password_hash = hash_password(password)

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO users (
                username,
                password_hash,
                created_at,
                is_active
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                username,
                password_hash,
                get_timestamp(),
                1,
            ),
        )

        connection.commit()

        return cursor.lastrowid

    except sqlite3.IntegrityError as error:
        connection.rollback()

        if "users.username" in str(error):
            raise ValueError(
                f"Username '{username}' already exists."
            ) from error

        raise

    finally:
        connection.close()


def get_user_by_username(username):
    """
    Retrieve a user by username.
    """
    if username is None:
        return None

    username = str(username).strip()

    if not username:
        return None

    initialize_database()

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT
                id,
                username,
                password_hash,
                created_at,
                is_active
            FROM users
            WHERE username = ?
            """,
            (username,),
        ).fetchone()

        if row is None:
            return None

        return dict(row)

    finally:
        connection.close()


def set_user_active(username, is_active):
    """
    Activate or deactivate a user account.
    """
    if username is None:
        return False

    username = str(username).strip()

    if not username:
        return False

    is_active = 1 if bool(is_active) else 0

    initialize_database()

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            UPDATE users
            SET is_active = ?
            WHERE username = ?
            """,
            (
                is_active,
                username,
            ),
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
