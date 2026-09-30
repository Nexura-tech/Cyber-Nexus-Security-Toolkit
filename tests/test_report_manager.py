from pathlib import Path

from modules.report_manager.manager import (
    REPORT_DIR,
    clear_reports,
    delete_report,
)


def test_reports_directory_exists():
    assert REPORT_DIR.exists()
    assert REPORT_DIR.is_dir()


def test_clear_reports_updates_report_status(
    tmp_path,
    monkeypatch,
):
    report_one = tmp_path / "report_one.txt"
    report_two = tmp_path / "report_two.txt"

    report_one.write_text(
        "Report One",
        encoding="utf-8",
    )

    report_two.write_text(
        "Report Two",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "modules.report_manager.manager.get_reports",
        lambda: [report_one, report_two],
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt="": "y",
    )

    updated_reports = []

    def fake_update_report_status(
        report_id,
        status,
    ):
        updated_reports.append(
            (report_id, status)
        )

    monkeypatch.setattr(
        "modules.report_manager.manager.get_report_by_file_path",
        lambda file_path: {
            "id": 1
        } if file_path == str(report_one.resolve()) else {
            "id": 2
        },
    )

    monkeypatch.setattr(
        "modules.report_manager.manager.update_report_status",
        fake_update_report_status,
    )

    clear_reports()

    assert not report_one.exists()
    assert not report_two.exists()

    assert updated_reports == [
        (1, "deleted"),
        (2, "deleted"),
    ]

def test_delete_report_updates_report_status(
    tmp_path,
    monkeypatch,
):
    report = tmp_path / "security_report.txt"

    report.write_text(
        "Security Report",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "modules.report_manager.manager.get_reports",
        lambda: [report],
    )

    inputs = iter(["1", "y"])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt="": next(inputs),
    )

    updated_reports = []

    def fake_update_report_status(
        report_id,
        status,
    ):
        updated_reports.append(
            (report_id, status)
        )

    monkeypatch.setattr(
        "modules.report_manager.manager.get_report_by_file_path",
        lambda file_path: {
            "id": 10
        },
    )

    monkeypatch.setattr(
        "modules.report_manager.manager.update_report_status",
        fake_update_report_status,
    )

    delete_report()

    assert not report.exists()

    assert updated_reports == [
        (10, "deleted"),
    ]

def test_delete_report_cancelled(
    tmp_path,
    monkeypatch,
):
    report = tmp_path / "security_report.txt"

    report.write_text(
        "Security Report",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "modules.report_manager.manager.get_reports",
        lambda: [report],
    )

    inputs = iter(["1", "n"])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt="": next(inputs),
    )

    updated_reports = []

    def fake_update_report_status(
        report_id,
        status,
    ):
        updated_reports.append(
            (report_id, status)
        )

    monkeypatch.setattr(
        "modules.report_manager.manager.update_report_status",
        fake_update_report_status,
    )

    delete_report()

    assert report.exists()
    assert updated_reports == []

def test_delete_report_invalid_selection(
    tmp_path,
    monkeypatch,
):
    report = tmp_path / "security_report.txt"

    report.write_text(
        "Security Report",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "modules.report_manager.manager.get_reports",
        lambda: [report],
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt="": "99",
    )

    delete_report()

    assert report.exists()
