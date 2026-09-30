import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

from core.config import (
    ADMIN_USERNAME,
    BASE_DIR,
    LOGIN_LOCKOUT_SECONDS,
    MAX_LOGIN_ATTEMPTS,
)
from core.passwords import hash_password, verify_password


# ============================================================
# Database Configuration
# ============================================================

DATABASE_FILE = BASE_DIR / "cyber_nexus.db"

VALID_REPORT_STATUSES = {
    "available",
    "completed",
    "failed",
    "deleted",
    "pending",
}


# ============================================================
# Connection
# ============================================================

def get_connection():
    """
    Return a SQLite database connection with Row objects.
    """

    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# ============================================================
# Database Initialization
# ============================================================

def initialize_database():
    """
    Create required tables if they do not already exist.

    Existing database data is preserved.
    """

    DATABASE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
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
                is_active INTEGER NOT NULL DEFAULT 1,
                role TEXT NOT NULL DEFAULT 'user',
                failed_login_attempts INTEGER NOT NULL DEFAULT 0,
                locked_until TEXT
            )
            """
        )

        # ----------------------------------------------------
        # Safe migrations for older databases
        # ----------------------------------------------------

        report_columns = {
            row["name"]
            for row in connection.execute(
                "PRAGMA table_info(report_history)"
            ).fetchall()
        }

        if "status" not in report_columns:
            connection.execute(
                """
                ALTER TABLE report_history
                ADD COLUMN status TEXT NOT NULL DEFAULT 'available'
                """
            )

        user_columns = {
            row["name"]
            for row in connection.execute(
                "PRAGMA table_info(users)"
            ).fetchall()
        }

        if "role" not in user_columns:
            connection.execute(
                """
                ALTER TABLE users
                ADD COLUMN role TEXT NOT NULL DEFAULT 'user'
                """
            )

        if "failed_login_attempts" not in user_columns:
            connection.execute(
                """
                ALTER TABLE users
                ADD COLUMN failed_login_attempts INTEGER NOT NULL DEFAULT 0
                """
            )

        if "locked_until" not in user_columns:
            connection.execute(
                """
                ALTER TABLE users
                ADD COLUMN locked_until TEXT
                """
            )

        connection.commit()

    finally:
        connection.close()


# ============================================================
# Metadata
# ============================================================

def set_metadata(key, value):
    """
    Create or update application metadata.
    """

    if key is None:
        raise ValueError("Metadata key cannot be empty.")

    key = str(key).strip()

    if not key:
        raise ValueError("Metadata key cannot be empty.")

    value = None if value is None else str(value)

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
            (key, value),
        )

        connection.commit()

    finally:
        connection.close()


def get_metadata(key, default=None):
    """
    Retrieve application metadata.
    """

    if key is None:
        return default

    key = str(key).strip()

    if not key:
        return default

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


# ============================================================
# Report History
# ============================================================

def add_report_history(
    report_name,
    report_type,
    file_path,
    created_at=None,
    status="available",
):
    """
    Add a report to report history.
    """

    if not report_name:
        raise ValueError("Report name cannot be empty.")

    if not report_type:
        raise ValueError("Report type cannot be empty.")

    if not file_path:
        raise ValueError("File path cannot be empty.")

    status = str(status).strip().lower()

    if status not in VALID_REPORT_STATUSES:
        raise ValueError(
            f"Invalid report status: {status}"
        )

    if created_at is None:
        created_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    initialize_database()

    connection = get_connection()

    try:
        cursor = connection.execute(
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
                status,
            ),
        )

        connection.commit()

        return cursor.lastrowid

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


def get_report_by_id(report_id):
    """
    Retrieve a report history entry by ID.
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


def update_report_status(report_id, status):
    """
    Update the status of an existing report.
    """

    try:
        report_id = int(report_id)
    except (TypeError, ValueError):
        return False

    if report_id < 1:
        return False

    if status is None:
        return False

    status = str(status).strip().lower()

    if status not in VALID_REPORT_STATUSES:
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
            (status, report_id),
        )

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()


# ============================================================
# User Management
# ============================================================

def create_user(username, password):
    """
    Create a normal user.

    Normal users always receive the 'user' role.
    """

    if username is None:
        raise ValueError("Username cannot be empty.")

    username = str(username).strip()

    if not username:
        raise ValueError("Username cannot be empty.")

    if password is None or not str(password):
        raise ValueError("Password cannot be empty.")

    if username == ADMIN_USERNAME:
        raise ValueError(
            f"'{ADMIN_USERNAME}' is reserved for the administrator."
        )

    initialize_database()

    if get_user_by_username(username) is not None:
        raise ValueError(
            f"Username '{username}' already exists."
        )

    password_hash = hash_password(str(password))

    created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO users (
                username,
                password_hash,
                created_at,
                is_active,
                role,
                failed_login_attempts,
                locked_until
            )
            VALUES (?, ?, ?, 1, 'user', 0, NULL)
            """,
            (
                username,
                password_hash,
                created_at,
            ),
        )

        connection.commit()

        return cursor.lastrowid

    except sqlite3.IntegrityError as error:
        connection.rollback()
        raise ValueError(
            f"Could not create user: {error}"
        ) from error

    finally:
        connection.close()


def create_first_admin(username, password):
    """
    Create the first administrator account.

    Only ADMIN_USERNAME can become admin.
    """

    if username is None:
        raise ValueError("Username cannot be empty.")

    username = str(username).strip()

    if username != ADMIN_USERNAME:
        raise ValueError(
            f"Administrator username must be '{ADMIN_USERNAME}'."
        )

    if password is None or not str(password):
        raise ValueError("Password cannot be empty.")

    initialize_database()

    if get_admin_count() > 0:
        raise ValueError(
            "An administrator account already exists."
        )

    existing_user = get_user_by_username(username)

    if existing_user is not None:
        raise ValueError(
            f"Username '{username}' already exists."
        )

    password_hash = hash_password(str(password))

    created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO users (
                username,
                password_hash,
                created_at,
                is_active,
                role,
                failed_login_attempts,
                locked_until
            )
            VALUES (?, ?, ?, 1, 'admin', 0, NULL)
            """,
            (
                username,
                password_hash,
                created_at,
            ),
        )

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()


def ensure_admin_account(password):
    """
    Create the Sabbo administrator account if no admin exists.

    Returns True only when a new administrator account is created.
    Returns False if an administrator already exists.
    """

    if password is None or not str(password):
        return False

    initialize_database()

    # Admin already exists.
    if get_admin_count() > 0:
        return False

    admin = get_user_by_username(ADMIN_USERNAME)

    if admin is not None:
        return False

    try:
        create_first_admin(
            ADMIN_USERNAME,
            str(password),
        )
        return True
    except (ValueError, sqlite3.IntegrityError):
        return False


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
                is_active,
                role,
                failed_login_attempts,
                locked_until
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


# ============================================================
# Login Security
# ============================================================

def get_login_security(username):
    """
    Return login security information for a user.
    """

    user = get_user_by_username(username)

    if user is None:
        return None

    return {
        "username": user["username"],
        "failed_login_attempts": user["failed_login_attempts"],
        "locked_until": user["locked_until"],
        "is_active": user["is_active"],
    }


def update_login_security(
    username,
    failed_login_attempts=0,
    locked_until=None,
):
    """
    Update failed-login and lockout information.
    """

    if username is None:
        return False

    username = str(username).strip()

    if not username:
        return False

    try:
        failed_login_attempts = int(
            failed_login_attempts
        )
    except (TypeError, ValueError):
        return False

    if failed_login_attempts < 0:
        failed_login_attempts = 0

    initialize_database()

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            UPDATE users
            SET
                failed_login_attempts = ?,
                locked_until = ?
            WHERE username = ?
            """,
            (
                failed_login_attempts,
                locked_until,
                username,
            ),
        )

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()


def authenticate_user(username, password):
    """
    Authenticate a user.

    Returns the user dictionary on success.
    Returns None on failure.
    """

    if username is None or password is None:
        return None

    username = str(username).strip()

    if not username:
        return None

    user = get_user_by_username(username)

    if user is None:
        return None

    if not user["is_active"]:
        return None

    # --------------------------------------------------------
    # Check lockout
    # --------------------------------------------------------

    locked_until = user["locked_until"]

    if locked_until:
        try:
            lock_time = datetime.fromisoformat(
                locked_until
            )

            if datetime.now() < lock_time:
                return None

            # Lock expired — reset security state.
            update_login_security(
                username,
                failed_login_attempts=0,
                locked_until=None,
            )

            user["failed_login_attempts"] = 0
            user["locked_until"] = None

        except ValueError:
            update_login_security(
                username,
                failed_login_attempts=0,
                locked_until=None,
            )

    # --------------------------------------------------------
    # Verify password
    # --------------------------------------------------------

    if verify_password(
        str(password),
        user["password_hash"],
    ):
        update_login_security(
            username,
            failed_login_attempts=0,
            locked_until=None,
        )

        user["failed_login_attempts"] = 0
        user["locked_until"] = None

        return user

    # --------------------------------------------------------
    # Failed login
    # --------------------------------------------------------

    failed_attempts = (
        user["failed_login_attempts"] or 0
    )

    failed_attempts += 1

    if failed_attempts >= MAX_LOGIN_ATTEMPTS:
        lock_time = datetime.now() + timedelta(
            seconds=LOGIN_LOCKOUT_SECONDS
        )

        locked_until = lock_time.isoformat(
            timespec="seconds"
        )

        update_login_security(
            username,
            failed_login_attempts=failed_attempts,
            locked_until=locked_until,
        )
    else:
        update_login_security(
            username,
            failed_login_attempts=failed_attempts,
            locked_until=None,
        )

    return None


# ============================================================
# User Queries
# ============================================================

def get_all_users():
    """
    Return all registered users.
    """

    initialize_database()

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                id,
                username,
                created_at,
                is_active,
                role,
                failed_login_attempts,
                locked_until
            FROM users
            ORDER BY id ASC
            """
        ).fetchall()

        return [
            dict(row)
            for row in rows
        ]

    finally:
        connection.close()


def set_user_active(username, is_active):
    """
    Activate or deactivate a user.
    """

    if username is None:
        return False

    username = str(username).strip()

    if not username:
        return False

    is_active = 1 if is_active else 0

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


def get_admin_count():
    """
    Return number of administrator accounts.
    """

    initialize_database()

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM users
            WHERE role = 'admin'
            """
        ).fetchone()

        return row["count"] or 0

    finally:
        connection.close()


def get_user_count():
    """
    Return total number of users.
    """

    initialize_database()

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM users
            """
        ).fetchone()

        return row["count"] or 0

    finally:
        connection.close()


def get_user_statistics():
    """
    Return basic user security statistics.
    """

    initialize_database()

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT
                COUNT(*) AS total_users,
                SUM(
                    CASE
                        WHEN is_active = 1 THEN 1
                        ELSE 0
                    END
                ) AS active_users,
                SUM(
                    CASE
                        WHEN is_active = 0 THEN 1
                        ELSE 0
                    END
                ) AS inactive_users,
                SUM(
                    CASE
                        WHEN role = 'admin' THEN 1
                        ELSE 0
                    END
                ) AS admin_users
            FROM users
            """
        ).fetchone()

        return {
            "total_users": row["total_users"] or 0,
            "active_users": row["active_users"] or 0,
            "inactive_users": row["inactive_users"] or 0,
            "admin_users": row["admin_users"] or 0,
        }

    finally:
        connection.close()


# ============================================================
# Automatic Initialization
# ============================================================

initialize_database()
