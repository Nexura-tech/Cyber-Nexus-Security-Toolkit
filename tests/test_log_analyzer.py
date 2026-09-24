from modules.log_analyzer.analyzer import analyze_log


def test_log_analysis(tmp_path):
    log_file = tmp_path / "test.log"

    log_file.write_text(
        "Failed password for user from 192.168.1.10\n"
        "Failed login from 192.168.1.10\n"
        "Accepted password for user from 192.168.1.20\n",
        encoding="utf-8",
    )

    result = analyze_log(log_file)

    assert result is not None
    assert result["total_lines"] == 3
    assert result["failed_logins"] == 2
    assert result["successful_logins"] == 1
    assert result["ip_counter"]["192.168.1.10"] == 2
    assert result["ip_counter"]["192.168.1.20"] == 1


def test_missing_log_file():
    result = analyze_log("missing_test.log")

    assert result is None
