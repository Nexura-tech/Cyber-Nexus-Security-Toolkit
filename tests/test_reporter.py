import json

from core.reporter import (
    generate_filename,
    sanitize_name,
    save_json,
    save_text,
)


def disable_report_history(monkeypatch):
    """
    Prevent reporter tests from modifying
    the real application database.
    """
    monkeypatch.setattr(
        "core.reporter.add_report_history",
        lambda **kwargs: None,
    )


def test_sanitize_name():
    assert sanitize_name("Password Analyzer") == "password_analyzer"
    assert sanitize_name("URL Analyzer!") == "url_analyzer"
    assert sanitize_name("  Test Report  ") == "test_report"


def test_generate_filename():
    file_path = generate_filename(
        "json",
        "Password Analyzer",
    )

    assert file_path.parent.name == "reports"
    assert file_path.suffix == ".json"
    assert "password_analyzer_" in file_path.name


def test_save_json(tmp_path, monkeypatch):
    disable_report_history(monkeypatch)

    monkeypatch.setattr(
        "core.reporter.REPORT_DIR",
        tmp_path,
    )

    data = {
        "module": "Test Module",
        "status": "success",
    }

    file_path = save_json(data)

    assert file_path.exists()
    assert file_path.suffix == ".json"

    saved_data = json.loads(
        file_path.read_text(
            encoding="utf-8"
        )
    )

    assert saved_data == data


def test_save_text(tmp_path, monkeypatch):
    disable_report_history(monkeypatch)

    monkeypatch.setattr(
        "core.reporter.REPORT_DIR",
        tmp_path,
    )

    data = {
        "Module": "Test Module",
        "Status": "success",
    }

    file_path = save_text(
        "Test Report",
        data,
    )

    assert file_path.exists()
    assert file_path.suffix == ".txt"

    content = file_path.read_text(
        encoding="utf-8"
    )

    assert "Test Report" in content
    assert "Module: Test Module" in content
    assert "Status: success" in content


def test_unique_report_filenames():
    first = generate_filename(
        "json",
        "test",
    )

    second = generate_filename(
        "json",
        "test",
    )

    assert first != second
