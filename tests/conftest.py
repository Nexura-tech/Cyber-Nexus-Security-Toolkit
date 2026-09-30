import sqlite3

import pytest

import database.manager as database_manager


@pytest.fixture(autouse=True)
def isolated_database(tmp_path, monkeypatch):
    """
    Give every test its own temporary SQLite database.
    """

    test_database = tmp_path / "test_cyber_nexus.db"

    monkeypatch.setattr(
        database_manager,
        "DATABASE_FILE",
        test_database,
    )

    database_manager.initialize_database()

    yield

    if test_database.exists():
        test_database.unlink()
