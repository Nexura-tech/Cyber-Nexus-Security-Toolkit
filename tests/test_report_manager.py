from modules.report_manager.manager import REPORT_DIR


def test_reports_directory_exists():
    assert REPORT_DIR.exists()
    assert REPORT_DIR.is_dir()
